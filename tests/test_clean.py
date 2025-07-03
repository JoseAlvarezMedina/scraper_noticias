# tests/test_clean.py

def test_clean_pipeline_strips_and_normalizes(sample_item, clean_pipeline, fake_spider):
    item = clean_pipeline.process_item(dict(sample_item), spider=fake_spider)
    assert item['titulo'] == 'Hola Mundo!'  # <-- Ya no minúsculas
    assert item['resumen'] == 'Esta es una noticia neutral.'
    assert item['autor'] == 'Juan Pérez'
    assert item['fecha'] == '2025-07-03'
