import json
import os
from pathlib import Path
from datetime import datetime

# Store records beside this module regardless of the launch directory.
SCORE_FILE = Path(__file__).resolve().with_name("high_scores.json")


class ScoreBoard:
    def __init__(self):
        self.scores = []
        self.load_scores()

    def load_scores(self):
        """Загружает рекорды из файла"""
        if os.path.exists(SCORE_FILE):
            try:
                with open(SCORE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if not isinstance(data, list):
                        raise ValueError("Score file must contain a list")
                    self.scores = [r for r in data if isinstance(r, dict)
                                   and isinstance(r.get('name'), str)
                                   and type(r.get('score')) is int and r['score'] >= 0
                                   and isinstance(r.get('date'), str)
                                   and isinstance(r.get('time'), str)]
                    self.scores.sort(key=lambda r: r['score'], reverse=True)
                    self.scores = self.scores[:10]
            except:
                self.scores = []
        else:
            self.scores = []

    def save_scores(self):
        """Сохраняет рекорды в файл"""
        temporary = SCORE_FILE.with_suffix('.json.tmp')
        with open(temporary, 'w', encoding='utf-8') as f:
            json.dump(self.scores[:10], f, ensure_ascii=False, indent=2)
        os.replace(temporary, SCORE_FILE)

    def add_score(self, name, score):
        """Добавляет новый рекорд"""
        now = datetime.now()
        new_record = {
            "name": (name.strip() or "Player")[:15],  # ограничиваем длину имени
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
