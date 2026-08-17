from fastapi.testclient import TestClient
from app.main import app
import io
from PIL import Image

client = TestClient(app)

def test_analyze_text():
    response = client.post("/api/analyze/text", json={"text": "Breaking news: Miracle cure discovered for all ailments."})
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert data["prediction"] in ["REAL", "FAKE", "MISLEADING", "SATIRE", "MANIPULATED"]
    assert "confidence" in data
    assert "explainability" in data
    assert data["input_type"] == "text"

def test_analyze_image():
    # Create simple 10x10 RGB test image
    img = Image.new("RGB", (10, 10), color="red")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_bytes = img_byte_arr.getvalue()

    response = client.post(
        "/api/analyze/image",
        files={"file": ("test.png", img_bytes, "image/png")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["input_type"] == "image"
    assert "prediction" in data
    assert data["image_analysis"]["width"] == 10

def test_analyze_multimodal():
    img = Image.new("RGB", (10, 10), color="blue")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_bytes = img_byte_arr.getvalue()

    response = client.post(
        "/api/analyze/multimodal",
        data={"text": "A photo of an official scientific laboratory test."},
        files={"file": ("test.png", img_bytes, "image/png")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["input_type"] == "multimodal"
    assert "multimodal_analysis" in data
    assert "alignment_score" in data["multimodal_analysis"]
