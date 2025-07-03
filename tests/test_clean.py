# tests/test_clean.py

def test_clean_pipeline_strips_and_normalizes(sample_item, clean_pipeline):
    item = clean_pipeline.process_item(dict(sample_item), spider=None)
    assert item["titulo"] == "Hola Mundo!"
    assert item["fecha"] == "2025-07-03"
