import csv
import sqlite3
from datetime import datetime
from scrapy.exceptions import DropItem

class NormalizarTextoPipeline:
    """Quita espacios extra y formatea la fecha."""
    def process_item(self, item, spider):
        # Campos de texto
        for field in ['titulo', 'resumen', 'autor']:
            if item.get(field):
                item[field] = item[field].strip()
            else:
                item[field] = ''

        # Fecha: intenta parsear ISO y formatear a YYYY-MM-DD
        raw = item.get('fecha')
        if raw:
            try:
                dt = datetime.fromisoformat(raw)
                item['fecha'] = dt.strftime('%Y-%m-%d')
            except ValueError:
                # Si falla, la dejamos tal cual
                spider.logger.warning(f"Fecha inválida: {raw}")
        else:
            item['fecha'] = ''

        # URL: validación básica
        if not item.get('url'):
            raise DropItem("Item sin URL, descartado")
        return item

class AlmacenarSQLitePipeline:
    """Guarda cada item en una tabla SQLite."""
    def open_spider(self, spider):
        self.conn = sqlite3.connect('noticias.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS noticias (
                titulo TEXT,
                resumen TEXT,
                autor TEXT,
                fecha TEXT,
                url TEXT UNIQUE
            )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("""
                INSERT INTO noticias (titulo, resumen, autor, fecha, url)
                VALUES (?, ?, ?, ?, ?)
            """, (
                item['titulo'],
                item['resumen'],
                item['autor'],
                item['fecha'],
                item['url']
            ))
            self.conn.commit()
        except sqlite3.IntegrityError:
            spider.logger.debug(f"URL duplicada: {item['url']}")
        return item

    def close_spider(self, spider):
        self.conn.close()

class AlmacenarCSVPL:
    def open_spider(self, spider):
        file_exists = os.path.exists('noticias.csv')
        self.file = open('noticias.csv', 'a', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        if not file_exists:
            # Cabecera actualizada: incluye sentiment_score, sentiment y topic
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
            item.get('sentiment_score',''),
            item.get('sentiment',''),
            item.get('topic','')
        ])
        return item
