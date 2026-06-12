import json
import os

RATING_FILE = "rating.json"
MAX_RECORDS = 6

class RatingTable:
    """Таблица рекордов — топ-6 игроков по очкам"""
    
    def __init__(self):
        self.records = []
        self.load()
    
    def load(self):
        if os.path.exists(RATING_FILE):
            try:
                with open(RATING_FILE, "r", encoding="utf-8") as f:
                    self.records = json.load(f)
            except:
                self.records = []
        else:
            self.records = []
    
    def save(self):
        with open(RATING_FILE, "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)
    
    def add_result(self, name, points):
        self.records.append({"name": name, "points": points})
        self.records.sort(key=lambda x: x["points"], reverse=True)
        if len(self.records) > MAX_RECORDS:
            self.records = self.records[:MAX_RECORDS]
        self.save()
    
    def get_records(self):
        return self.records