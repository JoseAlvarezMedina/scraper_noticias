import pytest
from scrapy.http import TextResponse, Request
from noticias.pipelines import NormalizeTextPipeline, SentimentPipeline
from noticias.spiders.titulares import TitularesSpider


@pytest.fixture
def sample_item():
    return {
        "titulo": "  Hola Mundo! ",
        "resumen": "Esta es una noticia neutral.",
        "autor": "Juan Pérez",
        "fecha": "2025-07-03T12:00:00",
        "url": "https://ejemplo.com/noticia"
    }

@pytest.fixture
def clean_pipeline():
    return NormalizeTextPipeline()

@pytest.fixture
def sentiment_pipeline():
    return SentimentPipeline()

@pytest.fixture
def spider():
    return TitularesSpider()
