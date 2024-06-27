from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from config import settings
from .ocr import ocr_to_dataframe, clean_ocr_data
from ..dependency.dependencies import get_db

router = APIRouter(prefix="/OCR", tags=["OCR"])

image_file = 'GustomateApp/OCR.jpeg'

# OCR 결과를 JSON 파일로 저장
@router.get("")
async def get_ocr_results(image_path: str = image_file, secret_key: str = settings.OCR_KEY, output_file: str = 'ocr_result.json'):
    try:
        ocr_data = ocr_to_dataframe(image_path, secret_key)
        if ocr_data is not None:
            cleaned_ocr_data = clean_ocr_data(ocr_data)
            print(cleaned_ocr_data)
            # Convert cleaned data to list of OCRResult objects
            ocr_results = [cleaned_ocr_data]
            print(ocr_results)
            return ocr_results
        else:
            raise HTTPException(status_code=404, detail="No OCR data found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))