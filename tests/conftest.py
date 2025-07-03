import pytest
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


import logging

class FakeSpider:
    def __init__(self):
        self.logger = logging.getLogger("test")
        if not self.logger.hasHandlers():
            self.logger.addHandler(logging.StreamHandler())

@pytest.fixture
def fake_spider():
    return FakeSpider()
