import os
import time
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv(override=True)

class AIEngine:
    def __init__(self):
        # Try Streamlit secrets first (cloud), then fall back to .env (local)
        try:
            self.api_key = st.secrets.get("GOOGLE_API_KEY", None)
        except Exception:
            self.api_key = None
        
        if not self.api_key:
            self.api_key = os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in secrets or .env file")
        
        self.client = genai.Client(api_key=self.api_key)
        # Using gemini-2.0-flash which is available and supports grounding
        self.model_name = "gemini-2.0-flash"

    def analyze_ticker(self, ticker_symbol, max_retries=3):
        """
        Generates a financial analysis report using Gemini with Google Search Grounding.
        Includes retry logic with exponential backoff.
        """
        
        prompt = f"""
        Si skúsený finančný analytik špecializujúci sa na fundamentálnu analýzu spoločností. Tvojou úlohou je vytvoriť 
        profesionálnu, detailnú analýzu spoločnosti {ticker_symbol} pre investorov a zainteresovaných čitateľov.
        
        Použij svoje nástroje (Google Search) na nájdenie najnovších a overených informácií, vrátane:
        1. Posledného dostupného Earnings Call prepisu (Transcript) - čo hovoril CEO/CFO?
        2. Aktuálnych noviniek a sentimentu na trhu.
        3. Verejne dostupných finančných výkazov a správ.
        
        FORMÁTOVANIE A ŠTÝL:
        - Výstup musí byť vo formáte Markdown a v SLOVENSKOM JAZYKU.
        - Píš ako profesionálny analytik - používaj odborný, ale zrozumiteľný jazyk.
        - PREFERUJ SÚVISLÉ ODSTAVCE TEXTU pred odrážkami. Odrážky použi len tam, kde sú nevyhnutné (napr. zoznamy produktov, míľniky).
        - Každá sekcia by mala obsahovať 2-4 odstavce kvalitného analytického textu.
        - Analýza musí pôsobiť ako profesionálny výstup investičnej banky, nie ako Wikipedia článok.
        
        DÔLEŽITÉ: 
        - NEZAČÍNAJ žiadnym úvodným textom, pozdravom ani frázami ako "Rozumiem", "Tu je analýza", "Dobre" atď.
        - Začni PRIAMO prvou sekciou "## 🏢 O spoločnosti" bez akéhokoľvek textu pred ňou.
        - Výstup musí obsahovať IBA čistý report bez komentárov od teba.
        
        ŠTRUKTÚRA REPORTU:
        
        ## 🏢 O spoločnosti
        Napíš 2-3 odstavce všeobecných informácií o spoločnosti. Vysvetli čím sa firma zaoberá, aká je jej pozícia 
        na trhu, a aký má význam v rámci odvetvia. Zahrň informácie o sídle, počte zamestnancov a globálnom dosahu.
        
        ### 📅 História (Top 5-7 míľnikov)
        Stručne uveď v bodoch najdôležitejšie momenty histórie spoločnosti. Pre každý míľnik použi formát:
        **Rok** - Čo sa stalo (napr. založenie, IPO, významná akvizícia, uvedenie prelomového produktu).
        
        ### 👔 Vedenie spoločnosti
        Predstav kľúčových ľudí vo vedení firmy. Pre každú osobu napíš 2-3 vety - kto to je, odkiaľ prišiel, 
        aké má skúsenosti a čo priniesol do firmy. Zameraj sa na CEO a 2-3 ďalších kľúčových členov vedenia.
        
        ### 📦 Hlavné produkty a služby
        Uveď hlavné produkty/služby spoločnosti. Ku každému pridaj 1-2 vety čo to je a prečo je to dôležité 
        pre firmu. Použi odrážky len pre prehľadnosť, ale doplň aj súvislý text o produktovom portfóliu.
        
        ### 💰 Zdroj zisku (Cash Cow)
        Jasne identifikuj JEDNU hlavnú vec, na ktorej firma zarába najviac. Vysvetli prečo práve toto je 
        hlavný zdroj zisku a aký podiel tvorí na celkových príjmoch. Napíš 1-2 odstavce analytického textu.
        Príklady: AWS pre Amazon, iPhone pre Apple, Windows/Azure pre Microsoft.
        
        ## ⚔️ Analýza konkurencie
        Napíš 2-3 odstavce o konkurenčnom prostredí. Kto sú hlavní konkurenti? V čom je táto firma lepšia 
        alebo horšia? Aká je jej trhová pozícia v porovnaní s konkurenciou?
        
        ### TOP 3 konkurenčné výhody (Moat)
        Uveď tri najsilnejšie konkurenčné výhody spoločnosti. Pre každú napíš 2-3 vety vysvetlenia, 
        prečo je to výhoda a ako ju firma využíva.
        
        ## ⚠️ TOP 3 Riziká a výzvy
        Identifikuj tri najväčšie problémy alebo riziká, ktorým firma čelí. Pre každé riziko napíš 
        2-3 vety analytického komentára - prečo je to problém a aký môže mať dopad.
        
        ## 📞 Earnings Call Review (Názor CEO)
        Zhrň posledný hovor s investormi (earnings call). Aký bol celkový tón? Na čo sa manažment zameral? 
        Čoho sa boja? Čo chválili? Aké sú ich očakávania do budúcnosti? Napíš 2-3 odstavce.
        
        ## 🎯 Záverečný verdikt
        Uveď svoje analytické hodnotenie: "Buy", "Hold" alebo "Sell". Zdôvodni prečo v 2-3 odstavcoch.
        Na záver pridaj disclaimer: "Táto analýza nie je finančná rada. Investovanie nesie riziko straty."
        """

        last_error = None
        
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(
                            google_search=types.GoogleSearch()
                        )],
                        response_mime_type="text/plain"
                    )
                )
                
                if not response or not response.text:
                    return "Chyba: AI nevrátila žiadny text. Skúste to prosím znova."
                    
                return response.text
                
            except Exception as e:
                last_error = str(e)
                
                # Check if it's a rate limit error (429)
                if "429" in last_error or "rate" in last_error.lower() or "quota" in last_error.lower():
                    if attempt < max_retries - 1:
                        # Wait with exponential backoff: 10s, 20s, 40s
                        wait_time = 10 * (2 ** attempt)
                        time.sleep(wait_time)
                        continue
                
                # For other errors, don't retry
                break
        
        # Return detailed error for debugging
        if "404" in last_error:
            return f"Chyba: Model {self.model_name} nebol nájdený alebo nie je podporovaný."
        if "429" in last_error or "rate" in last_error.lower() or "quota" in last_error.lower():
            return f"Chyba: Prekročený limit požiadaviek (Rate limit) aj po {max_retries} pokusoch. Skúste neskôr."
        if "403" in last_error or "permission" in last_error.lower():
            return f"Chyba: Prístup zamietnutý. Skontrolujte API kľúč. Detail: {last_error}"
        
        return f"Chyba pri generovaní analýzy: {last_error}"

