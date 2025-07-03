# tests/test_sentiment.py

from noticias.pipelines import SentimentPipeline

def test_sentiment_pipeline_adds_sentiment(sample_item):
    # Crear la instancia del pipeline
    pipeline = SentimentPipeline()
    
    # Inicializar el analizador llamando al método que Scrapy normalmente usaría
    pipeline.open_spider(spider=None)
    
    # Procesar el item de ejemplo
    item = pipeline.process_item(sample_item, spider=None)

    # Verificaciones
    assert "sentiment_score" in item
    assert "sentiment" in item
    assert isinstance(item["sentiment_score"], float)
    assert item["sentiment"] in ["positive", "neutral", "negative"]
