import yfinance as yf
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataEngine:
    def __init__(self):
        pass

    def get_ticker_data(self, ticker_symbol):
        """
        Fetches 'Hard Data' for a given ticker symbol using yfinance.
        Returns a dictionary with formatted values.
        """
        try:
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info
            
            if not info or 'symbol' not in info and 'currentPrice' not in info:
                return {"error": f"Ticker {ticker_symbol} nenájdený alebo nemá dostupné dáta."}

            # 1. Basic Info & Price
            current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0.0)
            previous_close = info.get('previousClose', 0.0)
            
            if previous_close and current_price:
                change_percent = ((current_price - previous_close) / previous_close) * 100
            else:
                change_percent = 0.0

            # 2. Financials
            financials = ticker.financials
            balance_sheet = ticker.balance_sheet
            
            # Revenue
            total_revenue = info.get('totalRevenue')
            if not total_revenue and financials is not None and not financials.empty:
                revenue_labels = ['Total Revenue', 'TotalRevenue', 'Revenue']
                for label in revenue_labels:
                    if label in financials.index:
                        total_revenue = financials.loc[label].iloc[0]
                        break

            # EPS
            eps_gaap = info.get('trailingEps', "N/A")
            eps_non_gaap = info.get('forwardEps', "N/A")

            # 3. RPO Proxy (Deferred Revenue)
            rpo_proxy = "N/A"
            if balance_sheet is not None and not balance_sheet.empty:
                rpo_proxy_labels = ['Deferred Revenue', 'DeferredRevenue', 'Contract Liabilities']
                for label in rpo_proxy_labels:
                    if label in balance_sheet.index:
                        try:
                            val = balance_sheet.loc[label].iloc[0]
                            if pd.notnull(val):
                                rpo_proxy = val
                                break
                        except Exception as e:
                            logger.error(f"Error reading balance sheet label {label}: {e}")
                            continue
            
            if isinstance(rpo_proxy, (int, float)):
                rpo_proxy = f"${rpo_proxy / 1e9:.2f} B"

            # 4. Valuation
            pe_ratio = info.get('trailingPE')
            forward_pe = info.get('forwardPE')
            fair_price = info.get('targetMeanPrice', "N/A")
            
            # 5. Additional Metrics
            gross_margin = info.get('grossMargins')
            operating_margin = info.get('operatingMargins')
            beta = info.get('beta')
            market_cap = info.get('marketCap')
            
            # 6. History for Charts (1 Year)
            history = ticker.history(period="1y")
            
            return {
                "name": info.get('longName', ticker_symbol),
                "symbol": ticker_symbol,
                "current_price": current_price,
                "change_percent": change_percent,
                "total_revenue": total_revenue,
                "eps_gaap": eps_gaap,
                "eps_non_gaap": eps_non_gaap,
                "rpo_proxy": rpo_proxy,
                "pe_ratio": pe_ratio,
                "forward_pe": forward_pe,
                "fair_price": fair_price,
                "gross_margin": gross_margin,
                "operating_margin": operating_margin,
                "beta": beta,
                "market_cap": market_cap,
                "history": history,
                "currency": info.get('currency', 'USD')
            }

        except Exception as e:
            logger.exception(f"Unexpected error in DataEngine for {ticker_symbol}")
            return {"error": str(e)}

    def format_large_number(self, num):
        if num is None or isinstance(num, str):
            return "N/A" if num is None else num
        try:
            if num >= 1e12:
                return f"${num / 1e12:.2f} T"
            if num >= 1e9:
                return f"${num / 1e9:.2f} B"
            elif num >= 1e6:
                return f"${num / 1e6:.2f} M"
            else:
                return f"${num:,.2f}"
        except:
            return str(num)
