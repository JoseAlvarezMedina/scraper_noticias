import os
import csv
import sqlite3
from datetime import datetime
from scrapy.exceptions import DropItem
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline


class NormalizarTextoPipeline:
    """Quita espacios extra y formatea la fecha."""
    def process_item(self, item, spider):
        # Campos de texto
        for field in ['titulo', 'resumen', 'autor']:
            item[field] = item.get(field, '').strip()

        # Fecha: intenta parsear ISO y formatear a YYYY-MM-DD
        raw = item.get('fecha')
        if raw:
            try:
                dt = datetime.fromisoformat(raw)
                item['fecha'] = dt.strftime('%Y-%m-%d')
            except ValueError:
                spider.logger.warning(f"Fecha inválida: {raw}")
        else:
            item['fecha'] = ''

        # URL: validación básica
        if not item.get('url'):
            raise DropItem("Item sin URL, descartado")
        return item


class SentimentPipeline:
    """Añade campo 'sentiment' y 'sentiment_score'."""
    def open_spider(self, spider):
        self.analyzer = SentimentIntensityAnalyzer()

    def process_item(self, item, spider):
        text = (item.get('resumen') or '')[:500]
        scores = self.analyzer.polarity_scores(text)
        compound = scores['compound']
        if compound > 0.05:
            label = 'positive'
        elif compound < -0.05:
            label = 'negative'
        else:
            label = 'neutral'
        item['sentiment_score'] = compound
        item['sentiment'] = label
        return item


class TopicPipeline:
    """Clasifica cada ítem en un topic usando Zero-Shot Classification."""
    def open_spider(self, spider):
        self.classifier = pipeline(
            "zero-shot-classification",
            model="valhalla/distilbart-mnli-12-1"
        )
        self.candidate_labels = [
            "Economía", "Política", "Tecnología",
            "Salud", "Entretenimiento", "Deportes", "Medio ambiente"
        ]

    def process_item(self, item, spider):
        text = (item.get('resumen') or '').strip()[:512]
        if not text:
            item['topic'] = 'Sin resumen'
        else:
            out = self.classifier(text, candidate_labels=self.candidate_labels)
            item['topic'] = out['labels'][0]
        return item


class AlmacenarSQLitePipeline:
    """Guarda cada item en una tabla SQLite, creando esquema si no existe."""
    def open_spider(self, spider):
        self.conn = sqlite3.connect('noticias.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS noticias (
                titulo TEXT,
                resumen TEXT,
                autor TEXT,
                fecha TEXT,
                url TEXT UNIQUE,
                sentiment_score REAL,
                sentiment TEXT,
                topic TEXT
            )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """
                INSERT INTO noticias (
                  titulo, resumen, autor, fecha, url,
                  sentiment_score, sentiment, topic
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item.get('titulo',''),
                    item.get('resumen',''),
                    item.get('autor',''),
                    item.get('fecha',''),
                    item.get('url',''),
                    item.get('sentiment_score',0.0),
                    item.get('sentiment',''),
                    item.get('topic','')
                )
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            spider.logger.debug(f"URL duplicada: {item.get('url')}")
        return item

    def close_spider(self, spider):
        self.conn.close()


class AlmacenarCSVPL:
    """Guarda cada item en un CSV incluyendo sentimiento y topic en modo append."""
    def open_spider(self, spider):
        file_exists = os.path.exists('noticias.csv')
        self.file = open('noticias.csv', 'a', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        if not file_exists:
            self.writer.writerow([
                'titulo', 'resumen', 'autor', 'fecha', 'url',
                'sentiment_score', 'sentiment', 'topic'
            ])

    def process_item(self, item, spider):
        self.writer.writerow([
            item.get('titulo',''),
            item.get('resumen',''),
            item.get('autor',''),
            item.get('fecha',''),
            item.get('url',''),
            item.get('sentiment_score', ''),
            item.get('sentiment', ''),
            item.get('topic', '')
        ])
        return item

    def close_spider(self, spider):
        self.file.close()
