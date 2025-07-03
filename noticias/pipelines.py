import os
import csv
import sqlite3
from datetime import datetime
from scrapy.exceptions import DropItem
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class NormalizeTextPipeline:
    def process_item(self, item, spider):
        for field in ('titulo', 'resumen', 'autor'):
            value = item.get(field, '')
            item[field] = value.strip() if isinstance(value, str) else ''

        # Procesar la fecha: intenta múltiples formatos comunes
        raw_date = item.get('fecha', '')
        parsed_date = ''

        date_formats = [
        '%a, %d %b %Y %H:%M:%S %z',  # Thu, 03 Jul 2025 14:58:43 +0000
        '%Y-%m-%dT%H:%M:%S%z',       # 2025-07-03T14:58:43+0000
        '%Y-%m-%d %H:%M:%S',         # 2025-07-03 14:53:08  ✅ <-- Agrega esta
        '%Y-%m-%d'                   # 2025-07-03
        ]

        for fmt in date_formats:
            try:
                dt = datetime.strptime(raw_date, fmt)
                parsed_date = dt.strftime('%Y-%m-%d')
                break
            except (ValueError, TypeError):
                continue

        if not parsed_date:
            spider.logger.warning(f"Invalid date format: {raw_date}")

        item['fecha'] = parsed_date

        if not item.get('url'):
            raise DropItem("Missing URL in item, dropping")

        return item


class SentimentPipeline:
    def open_spider(self, spider):
        self.analyzer = SentimentIntensityAnalyzer()

    def process_item(self, item, spider):
        text = (item.get('resumen') or '')[:500]
        scores = self.analyzer.polarity_scores(text)
        compound = scores.get('compound', 0.0)

        if compound > 0.05:
            label = 'positive'
        elif compound < -0.05:
            label = 'negative'
        else:
            label = 'neutral'

        item['sentiment_score'] = compound
        item['sentiment'] = label
        return item


class SQLiteStorePipeline:
    def open_spider(self, spider):
        db_path = spider.settings.get('SQLITE_DB_PATH', 'noticias.db')
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS noticias (
                titulo TEXT,
                resumen TEXT,
                autor TEXT,
                fecha TEXT,
                url TEXT PRIMARY KEY,
                sentiment_score REAL,
                sentiment TEXT
            )
            """
        )
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """
                INSERT INTO noticias (
                    titulo, resumen, autor, fecha, url,
                    sentiment_score, sentiment
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item.get('titulo', ''),
                    item.get('resumen', ''),
                    item.get('autor', ''),
                    item.get('fecha', ''),
                    item.get('url', ''),
                    item.get('sentiment_score', 0.0),
                    item.get('sentiment', '')
                )
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            spider.logger.debug(f"Duplicate URL skipped: {item.get('url')}")
        return item

    def close_spider(self, spider):
        self.conn.close()



class CSVStorePipeline:
    """
    Append items to a CSV file while avoiding duplicates using the URL field.
    Configuration via Scrapy settings:
      - CSV_FILE_PATH: path to the CSV file (default: 'noticias.csv')
    """

    def open_spider(self, spider):
        self.csv_path = spider.settings.get('CSV_FILE_PATH', 'noticias.csv')
        self.fieldnames = [
            'titulo', 'resumen', 'autor', 'fecha', 'url',
            'sentiment_score', 'sentiment'
        ]
        self.existing_urls = set()

        # Leer URLs existentes si el archivo ya existe
        if os.path.isfile(self.csv_path):
            with open(self.csv_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.existing_urls.add(row['url'])

        # Abrir archivo en modo append y preparar el escritor
        self.file = open(self.csv_path, 'a', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)

        # Escribir encabezados si el archivo está vacío
        if os.stat(self.csv_path).st_size == 0:
            self.writer.writeheader()

    def process_item(self, item, spider):
        url = item.get('url', '')
        if url in self.existing_urls:
            spider.logger.debug(f"URL duplicada, no se escribe: {url}")
            raise DropItem(f"Duplicado encontrado: {url}")
        else:
            row = {key: item.get(key, '') for key in self.fieldnames}
            self.writer.writerow(row)
            self.existing_urls.add(url)
            return item

    def close_spider(self, spider):
        self.file.close()
