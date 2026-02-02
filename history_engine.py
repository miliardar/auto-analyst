import json
import os
import pandas as pd
from datetime import datetime

class HistoryEngine:
    def __init__(self, history_dir="history"):
        self.history_dir = history_dir
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)

    def save_analysis(self, ticker, data, ai_report):
        """
        Saves analysis data and AI report to a JSON file.
        Uses a robust strategy:
        1. Explicitly convert Pandas DataFrames to dicts (for nice structure).
        2. Use json.dump(default=str) to handle EVERYTHING else (Timestamps, Numpy types) by converting to string.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{ticker}_{timestamp}.json"
        filepath = os.path.join(self.history_dir, filename)
        
        def prepare_dataframes(obj):
            """Recursively finds DataFrames and converts them to dicts."""
            if isinstance(obj, pd.DataFrame):
                return obj.reset_index().to_dict(orient='records')
            if isinstance(obj, dict):
                return {k: prepare_dataframes(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [prepare_dataframes(i) for i in obj]
            return obj

        # 1. First pass: Handle DataFrames nicely
        clean_data = prepare_dataframes(data)

        payload = {
            "ticker": ticker,
            "timestamp": timestamp,
            "data": clean_data,
            "ai_report": ai_report
        }

        # 2. Final pass: Use default=str to catch Timestamps, NaT, Numpy ints, etc.
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=4, default=str)
        
        return filename






    def get_history_list(self):
        """
        Returns a list of saved analyses sorted by timestamp (newest first).
        """
        files = [f for f in os.listdir(self.history_dir) if f.endswith(".json")]
        history = []
        for f in files:
            path = os.path.join(self.history_dir, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    meta = json.load(file)
                    history.append({
                        "id": f,
                        "ticker": meta.get("ticker"),
                        "timestamp": meta.get("timestamp"),
                        "date_display": datetime.strptime(meta.get("timestamp"), "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M")
                    })
            except:
                continue
        
        return sorted(history, key=lambda x: x['timestamp'], reverse=True)

    def load_analysis(self, filename):
        """
        Loads a specific analysis by filename.
        """
        filepath = os.path.join(self.history_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
