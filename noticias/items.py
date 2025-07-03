# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NoticiaItem(scrapy.Item):
    # Campos que vamos a extraer
    titulo = scrapy.Field()
    resumen = scrapy.Field()
    autor = scrapy.Field()
    fecha = scrapy.Field()
    url = scrapy.Field()
    # Campos añadidos por el pipeline de sentimiento
    sentiment_score = scrapy.Field()
    sentiment = scrapy.Field()
