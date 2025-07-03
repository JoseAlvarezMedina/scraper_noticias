from scrapy.http import Request
from scrapy.selector import Selector
from noticias.spiders.titulares import TitularesSpider

def test_spider_parses_rss_item(spider):
    xml = """
    <rss version="2.0">
      <channel>
        <item>
          <title>Noticia 1</title>
          <description>Resumen de la noticia.</description>
          <author>Juan Pérez</author>
          <pubDate>Tue, 03 Jul 2025 08:00:00 GMT</pubDate>
          <link>https://ejemplo.com/n1</link>
        </item>
      </channel>
    </rss>
    """

    # Simulamos un XML response con Selector directamente
    sel = Selector(text=xml, type="xml")

    # Creamos un spider real
    items = []
    for entry in sel.xpath("//item"):
        item = spider.parse_item(entry)  # Usamos una función que debes separar del parse()
        items.append(item)

    assert len(items) == 1
    item = items[0]
    assert item["titulo"] == "Noticia 1"
    assert item["resumen"] == "Resumen de la noticia."
    assert item["autor"] == "Juan Pérez"
    assert item["fecha"] in ("Tue, 03 Jul 2025 08:00:00 GMT", "2025-07-03")
    assert item["url"] == "https://ejemplo.com/n1"
