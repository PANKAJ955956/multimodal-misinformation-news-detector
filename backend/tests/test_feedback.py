from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_feedback_flow():
    # First create a prediction
    pred_resp = client.post("/api/analyze/text", json={"text": "Test claim text for feedback testing."})
    assert pred_resp.status_code == 200
    pred_data = pred_resp.json()
    prediction_id = pred_data["id"]

    # Submit human review feedback
    feedback_payload = {
        "prediction_id": prediction_id,
        "human_label": "REAL",
        "reviewer_comment": "Verified by official press release."
    }
    fb_resp = client.post("/api/feedback", json=feedback_payload)
    assert fb_resp.status_code == 200
    fb_data = fb_resp.json()
    assert fb_data["prediction_id"] == prediction_id
    assert fb_data["human_label"] == "REAL"

    # Verify prediction history detail returns human feedback
    hist_resp = client.get(f"/api/predictions/{prediction_id}")
    assert hist_resp.status_code == 200
    hist_data = hist_resp.json()
    assert len(hist_data["human_feedback"]) >= 1
    assert hist_data["human_feedback"][0]["human_label"] == "REAL"
