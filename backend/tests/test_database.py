from app.database.database import SessionLocal
from app.database import crud

def test_database_crud():
    db = SessionLocal()
    try:
        # Create prediction
        pred = crud.create_prediction(db, {
            "input_type": "text",
            "text_content": "Unit test database claim",
            "prediction": "REAL",
            "confidence": 0.95,
            "text_score": 0.95,
            "model_version": "0.1.0"
        })
        assert pred.id is not None

        # Retrieve prediction
        fetched = crud.get_prediction_by_id(db, pred.id)
        assert fetched is not None
        assert fetched.text_content == "Unit test database claim"

        # Analytics check
        analytics = crud.get_analytics_summary(db)
        assert analytics["total_analyses"] >= 1
    finally:
        db.close()
