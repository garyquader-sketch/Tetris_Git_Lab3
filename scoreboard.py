import json
import os
from datetime import datetime

SCORE_FILE = "high_scores.json"


class ScoreBoard:
    def __init__(self):
        self.scores = []
        self.load_scores()

    def load_scores(self):
        """Загружает рекорды из файла"""
        if os.path.exists(SCORE_FILE):
            try:
                with open(SCORE_FILE, 'r', encoding='utf-8') as f:
                    self.scores = json.load(f)
            except:
                self.scores = []
        else:
            self.scores = []

    def save_scores(self):
        """Сохраняет рекорды в файл"""
        with open(SCORE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.scores[:10], f, ensure_ascii=False, indent=2)

    def add_score(self, name, score):
        """Добавляет новый рекорд"""
        now = datetime.now()
        new_record = {
            "name": name[:15],  # ограничиваем длину имени
            "score": score,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S")
        }

        self.scores.append(new_record)
        # Сортируем по убыванию очков
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        # Оставляем только 10 лучших
        self.scores = self.scores[:10]
        self.save_scores()

    def get_top_scores(self, limit=10):
        """Возвращает список лучших рекордов"""
        return self.scores[:limit]

    def is_high_score(self, score):
        """Проверяет, попадает ли результат в топ-10"""
        if len(self.scores) < 10:
            return True
        return score > self.scores[-1]["score"]
