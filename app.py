import streamlit as st
import pandas as pd
import importlib

from data_engine import DataEngine
from ai_engine import AIEngine
from history_engine import HistoryEngine
import ui_components as ui
importlib.reload(ui)
import time

# Page Config
st.set_page_config(
    page_title="JK Capital - Auto-Analyst",
    page_icon="💎",
    layout="wide"
)

# Initialize Engines (no caching to pick up code changes immediately)
data_engine = DataEngine()
ai_engine = AIEngine()
history_engine = HistoryEngine()


# Apply Custom Premium Blue Styles
ui.apply_custom_styles()

# State Management
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None

# Sidebar - History and Input
with st.sidebar:
    st.markdown("### 🔍 Nová Analýza")
    ticker_input = st.text_input("Zadaj Ticker (napr. TSLA)", value="").upper()
    analyze_btn = st.button("🚀 Spustiť Analýzu")
    
    st.divider()
    st.markdown("### 🕒 História")
    history_list = history_engine.get_history_list()
    
    if not history_list:
        st.info("Zatiaľ žiadna história.")
    else:
        for item in history_list:
            if st.button(f"📄 {item['ticker']} ({item['date_display']})", key=item['id']):
                # Load from history
                loaded = history_engine.load_analysis(item['id'])
                if loaded:
                    st.session_state.current_analysis = loaded
                    # Reconstruct history DF if present
                    if 'data' in loaded and 'history' in loaded['data']:
                        hist_data = loaded['data']['history']
                        if isinstance(hist_data, list):
                            df = pd.DataFrame(hist_data)
                            if 'Date' in df.columns:
                                df['Date'] = pd.to_datetime(df['Date'])
                                df.set_index('Date', inplace=True)
                            st.session_state.current_analysis['data']['history'] = df


# Main Logic
ui.render_header()

if analyze_btn and ticker_input:
    with st.spinner(f"Analyzujem {ticker_input}..."):
        # 1. Fetch Data
        hard_data = data_engine.get_ticker_data(ticker_input)
        
        if "error" in hard_data:
            st.error(f"Chyba pri získavaní dát: {hard_data['error']}")
        else:
            # 2. Call AI
            ai_report = ai_engine.analyze_ticker(ticker_input)
            
            # 3. Save to History (Deep copy to avoid modifying original during save)
            saved_id = history_engine.save_analysis(ticker_input, hard_data, ai_report)
            
            # Update session state to display
            st.session_state.current_analysis = {
                "ticker": ticker_input,
                "data": hard_data,
                "ai_report": ai_report
            }
            st.success(f"Analýza pre {ticker_input} bola úspešne dokončená a uložená.")
            st.rerun()

# Render Analysis if available
if st.session_state.current_analysis:
    analysis = st.session_state.current_analysis
    ticker = analysis['ticker']
    data = analysis['data']
    report = analysis['ai_report']
    
    # Hero Section (Ticker Info)
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(f"<h1 style='margin-bottom:0;'>{ticker}</h1>", unsafe_allow_html=True)
    with col2:
        name = data.get('name', ticker)
        price = data.get('current_price', 0.0)
        change = data.get('change_percent', 0.0)
        color = "#00ff00" if change >= 0 else "#ff4b4b"
        st.markdown(f"<h2 style='margin-top:0; color:#8c8c8c;'>{name}</h2>", unsafe_allow_html=True)
        st.markdown(f"<span style='font-size: 28px; font-weight: bold;'>${price:,.2f}</span> <span style='color: {color}; font-size: 20px;'>({change:+.2f}%)</span>", unsafe_allow_html=True)

    # Tabs
    tab_analysis, tab_data = st.tabs(["🧠 AI Analýza", "📊 Finančné Metriky"])

    with tab_analysis:
        st.markdown(report)

        st.divider()
        st.download_button(
            label="📥 Stiahnuť Report (Markdown)",
            data=report,
            file_name=f"{ticker}_analyza.md",
            mime="text/markdown"
        )

    with tab_data:
        # Hero Section: Fair Price
        fair_price_val = f"${data['fair_price']}" if isinstance(data.get('fair_price'), (int, float)) else "N/A"
        current_price_display = f"Aktuálna cena: ${price:,.2f}"
        
        ui.highlight_metric_card("Fair Price (Vnútorná Hodnota)", fair_price_val, current_price_display)
        
        st.write("")
        
        # Row 1: Basic Info
        m1, m2, m3, m4 = st.columns(4)
        with m1: ui.metric_card("Market Cap", data_engine.format_large_number(data.get('market_cap')))
        with m2: ui.metric_card("Revenue", data_engine.format_large_number(data.get('total_revenue')))
        with m3: ui.metric_card("Gross Margin", f"{data['gross_margin']*100:.1f}%" if data.get('gross_margin') else "N/A")
        with m4: ui.metric_card("Operating Margin", f"{data['operating_margin']*100:.1f}%" if data.get('operating_margin') else "N/A")
        
        st.write("")
        # Row 2: EPS & P/E Metrics
        m5, m6, m7, m8 = st.columns(4)
        with m5: ui.metric_card("GAAP EPS", data.get('eps_gaap', "N/A"))
        with m6: ui.metric_card("Non-GAAP (Fwd)", data.get('eps_non_gaap', "N/A"))
        with m7: ui.metric_card("P/E Ratio", f"{data['pe_ratio']:.2f}" if data.get('pe_ratio') else "N/A")
        with m8: ui.metric_card("Forward P/E", f"{data['forward_pe']:.2f}" if data.get('forward_pe') else "N/A")
        
        st.write("")
        # Row 3: Others
        m9, m10, m11, m12 = st.columns(4)
        with m9: ui.metric_card("RPO (Deferred)", data.get('rpo_proxy', "N/A"))
        with m10: ui.metric_card("Beta", f"{data['beta']:.2f}" if data.get('beta') else "N/A")
        with m11: st.empty()
        with m12: st.empty()

        # Legend
        ui.render_legend()



else:
    # Landing Page
    st.markdown("""
    ### 👋 Vitajte v analytickej platforme JK Capital
    Zadajte ticker vľavo pre spustenie automatickej analýzy. 
    
    **Čo nájdete v reportoch:**
    - Detailný profil spoločnosti
    - Analýza konkurencie a ich výhod (Moat)
    - Vyhodnotenie Earnings hovorov s pomocou Gemini AI
    - Výpočet kľúčových finančných metrík
    """)
    
    # Quick examples or info
    st.info("💡 Aplikácia si teraz pamätá vaše predchádzajúce výstupy v sekcii História.")
