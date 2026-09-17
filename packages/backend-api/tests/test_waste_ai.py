import pytest
try:
    from packages.ai_engine.inference.predictor import MobileNetWastePredictor
except ModuleNotFoundError:
    import sys
    from pathlib import Path
    root_dir = str(Path(__file__).resolve().parents[3])
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
    from packages.ai_engine.inference.predictor import MobileNetWastePredictor

def test_mobilenet_waste_predictor():
    predictor = MobileNetWastePredictor()
    dummy_image_bytes = b"FFD8FFE000104A46494600010101006000600000FFD9"  # Minimal JPEG header
    
    result = predictor.predict_image_bytes(dummy_image_bytes)
    assert "primary_label" in result
    assert "category" in result
    assert "confidence_score" in result
    assert result["confidence_score"] >= 0.70
    assert result["carbon_saved_kg"] > 0.0
