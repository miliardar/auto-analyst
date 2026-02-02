import streamlit as st

def apply_custom_styles():
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    html, body, [data-testid="stapp"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Background with subtle gradient */
    .stApp {
        background: radial-gradient(circle at top right, #001a33, #000b1a);
        color: #e6f1ff;
    }

    /* Sidebar - Premium Dark */
    [data-testid="stSidebar"] {
        background-color: #000d1a !important;
        border-right: 1px solid rgba(24, 144, 255, 0.1);
    }

    /* Header Styling - Glassmorphism */
    .app-header {
        background: rgba(0, 21, 41, 0.7);
        backdrop-filter: blur(12px);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        border: 1px solid rgba(24, 144, 255, 0.2);
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        text-align: center;
    }
    
    .app-title {
        background: linear-gradient(135deg, #ffffff 0%, #1890ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0px;
        letter-spacing: -1px;
    }
    
    .app-subtitle {
        color: #1890ff;
        font-size: 1.1rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-top: 10px;
        letter-spacing: 3px;
        opacity: 0.8;
    }

    /* Metric Cards - Premium Glass */
    .metric-card {
        background: rgba(0, 39, 102, 0.3);
        backdrop-filter: blur(8px);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(24, 144, 255, 0.15);
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .metric-card:hover {
        transform: translateY(-8px);
        background: rgba(0, 39, 102, 0.5);
        border-color: #1890ff;
        box-shadow: 0 12px 30px rgba(24, 144, 255, 0.15);
    }
    .metric-label {
        color: #91d5ff;
        font-size: 0.75rem;
        margin-bottom: 10px;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .metric-value {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 800;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    /* Tabs - Modern Minimal */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        padding: 10px;
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent !important;
        border: none !important;
        color: #8c8c8c !important;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stTabs [aria-selected="true"] {
        color: #1890ff !important;
        border-bottom: 3px solid #1890ff !important;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #000b1a;
    }
    ::-webkit-scrollbar-thumb {
        background: #002766;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #1890ff;
    }

    /* Highlight Card */
    .highlight-card {
        background: radial-gradient(circle at center, rgba(24, 144, 255, 0.4), rgba(0, 39, 102, 0.6));
        backdrop-filter: blur(12px);
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #1890ff;
        text-align: center;
        box-shadow: 0 0 30px rgba(24, 144, 255, 0.3);
        margin-bottom: 2rem;
    }
    .highlight-title {
        color: #e6f1ff;
        font-size: 1.1rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 15px;
    }
    .highlight-value {
        color: #ffffff;
        font-size: 3.5rem;
        font-weight: 800;
        text-shadow: 0 0 20px rgba(24, 144, 255, 0.6);
        line-height: 1.2;
    }
    .highlight-secondary {
        margin-top: 10px;
        font-size: 1.2rem;
        color: #91d5ff;
        background: rgba(0,0,0,0.3);
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
    }

    /* Legend */
    .legend-box {
        background: rgba(0, 21, 41, 0.6);
        border-radius: 16px;
        padding: 25px 30px;
        margin-top: 40px;
        border: 1px solid rgba(24, 144, 255, 0.2);
    }
    .legend-title {
        color: #1890ff;
        font-weight: 700;
        margin-bottom: 20px;
        text-transform: uppercase;
        font-size: 0.9rem;
        letter-spacing: 2px;
    }
    .legend-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
    }
    .legend-item {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        padding: 14px 16px;
        border-left: 3px solid #1890ff;
    }
    .legend-term {
        color: #91d5ff;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 4px;
    }
    .legend-desc {
        color: #a0a0a0;
        font-size: 0.8rem;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

def render_header():
    st.markdown("""
        <div class="app-header">
            <div class="app-title">Jakub Kraľovanský Capital</div>
            <div class="app-subtitle">Automatická Analýza V 1.1</div>
        </div>
    """, unsafe_allow_html=True)

def metric_card(label, value):
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

def highlight_metric_card(label, value, secondary_text):
    st.markdown(f"""
        <div class="highlight-card">
            <div class="highlight-title">{label}</div>
            <div class="highlight-value">{value}</div>
            <div class="highlight-secondary">{secondary_text}</div>
        </div>
    """, unsafe_allow_html=True)

def render_legend():
    st.markdown("""
        <div class="legend-box">
            <div class="legend-title">📖 Vysvetlivky pojmov</div>
            <div class="legend-grid">
                <div class="legend-item">
                    <div class="legend-term">Fair Price (Vnútorná hodnota)</div>
                    <div class="legend-desc">Odhadovaná "skutočná" hodnota akcie na základe budúcich ziskov (DCF model). Ak je aktuálna cena nižšia, akcia môže byť lacná.</div>
                </div>
                <div class="legend-item">
                    <div class="legend-term">Market Cap (Trhová kapitalizácia)</div>
                    <div class="legend-desc">Celková hodnota všetkých akcií spoločnosti. Cena akcie × počet akcií. Hovorí o veľkosti firmy.</div>
                </div>
                <div class="legend-item">
                    <div class="legend-term">Revenue (Tržby)</div>
                    <div class="legend-desc">Celkový príjem firmy z predaja tovarov a služieb pred odpočítaním nákladov.</div>
                </div>
                <div class="legend-item">
                    <div class="legend-term">Gross Margin (Hrubá marža)</div>
                    <div class="legend-desc">Koľko percent z tržieb firme ostane po zaplatení priamych nákladov na výrobu. Vyššia = lepšia.</div>
                </div>
                <div class="legend-item">
                    <div class="legend-term">Operating Margin (Prevádzková marža)</div>
                    <div class="legend-desc">Koľko percent z tržieb ostane po zaplatení všetkých prevádzkových nákladov. Ukazuje efektivitu.</div>
                </div>
                <div class="legend-item">
                    <div class="legend-term">GAAP EPS (Zisk na akciu)</div>
                    <div class="legend-desc">Čistý zisk delený počtom akcií podľa účtovných štandardov. Zahŕňa všetky náklady.</div>
                </div>
                <div class="legend-item">
                    <div class="legend-term">Non-GAAP EPS (Forward)</div>
                    <div class="legend-desc">Upravený zisk na akciu bez jednorazových položiek. "Forward" = odhad do budúcnosti.</div>
                </div>
                <div class="legend-item">
                    <div class="legend-term">P/E Ratio (Pomer cena/zisk)</div>
                    <div class="legend-desc">Koľko dolárov platíte za 1 dolár zisku firmy. Vyššie číslo = drahšia akcia.</div>
                </div>
                <div class="legend-item">
                    <div class="legend-term">Forward P/E</div>
                    <div class="legend-desc">P/E ratio vypočítané na základe odhadovaných budúcich ziskov. Lepšie pre rastové firmy.</div>
                </div>
                <div class="legend-item">
                    <div class="legend-term">RPO (Deferred Revenue)</div>
                    <div class="legend-desc">Peniaze, ktoré firma dostala, ale ešte nezarobila (napr. predplatné). Signalizuje budúce tržby.</div>
                </div>
                <div class="legend-item">
                    <div class="legend-term">Beta</div>
                    <div class="legend-desc">Meria volatilitu akcie oproti trhu. Beta 1 = ako trh, &gt;1 = volatilnejšia, &lt;1 = stabilnejšia.</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

