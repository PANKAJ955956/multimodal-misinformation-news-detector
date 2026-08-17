from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database.database import get_db
from app.schemas.prediction import PredictionRequestText, PredictionRequestURL, PredictionResponse
from app.services.prediction_service import prediction_service
from app.services.url_service import url_service
from app.utils.security import validate_image_file

router = APIRouter()

@router.post("/analyze/text", response_model=PredictionResponse)
def analyze_text(payload: PredictionRequestText, db: Session = Depends(get_db)):
    if not payload.text or len(payload.text.strip()) < 3:
        raise HTTPException(status_code=400, detail="Text must be at least 3 characters long.")
        
    result = prediction_service.predict(
        db=db,
        input_type="text",
        text_content=payload.text.strip()
    )
    return result

@router.post("/analyze/image", response_model=PredictionResponse)
async def analyze_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()
    validate_image_file(file, contents)
    
    result = prediction_service.predict(
        db=db,
        input_type="image",
        image_bytes=contents,
        image_filename=file.filename
    )
    return result

@router.post("/analyze/multimodal", response_model=PredictionResponse)
async def analyze_multimodal(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    if not text and not file:
        raise HTTPException(status_code=400, detail="Must provide at least text or an image file for multimodal analysis.")
        
    image_bytes = None
    filename = None
    if file:
        image_bytes = await file.read()
        validate_image_file(file, image_bytes)
        filename = file.filename

    result = prediction_service.predict(
        db=db,
        input_type="multimodal",
        text_content=text.strip() if text else None,
        image_bytes=image_bytes,
        image_filename=filename
    )
    return result

@router.post("/analyze/url", response_model=PredictionResponse)
async def analyze_url(payload: PredictionRequestURL, db: Session = Depends(get_db)):
    # 1. Fetch & extract content with SSRF defense
    extracted_data = await url_service.fetch_and_extract(payload.url)
    
    text_to_analyze = f"{extracted_data['title']}. {extracted_data['extracted_text']}"
    
    result = prediction_service.predict(
        db=db,
        input_type="url",
        text_content=text_to_analyze,
        url=payload.url
    )
    return result
