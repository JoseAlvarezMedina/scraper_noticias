import scrapy
from noticias.items import NoticiaItem

class MiSpider(scrapy.Spider):
    name = 'titulares'
    allowed_domains = [
        'larepublica.co',
        'cronicadelquindio.com',
        'elpilon.com.co',
        'lasillavacia.com',
        'eje21.com.co',
    ]
    start_urls = [
        'https://www.larepublica.co/rss',
        'https://www.cronicadelquindio.com/rss',
        'https://www.elpilon.com.co/rss',
        'https://lasillavacia.com/feed',
        'https://www.eje21.com.co/rss2',
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 1.0,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'AUTOTHROTTLE_ENABLED': True,
    }

    def parse(self, response):
        # Cada <item> de un feed RSS
        for entry in response.xpath('//item'):
            item = NoticiaItem()
            item['titulo']  = entry.xpath('title/text()').get(default='').strip()
            item['resumen'] = entry.xpath('description/text()').get(default='').strip()
            # autor puede venir en <author> o en dc:creator
            item['autor']   = (
                entry.xpath('author/text()').get()
                or entry.xpath('*[local-name()="creator"]/text()').get()
                or ''
            ).strip()
            # fecha en pubDate o en dc:date
            item['fecha']   = (
                entry.xpath('pubDate/text()').get()
                or entry.xpath('*[local-name()="date"]/text()').get()
                or ''
            ).strip()
            item['url']     = entry.xpath('link/text()').get(default='').strip()
            yield item

        # No hay paginación en RSS, así que acabamos aquí
