from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import schemas, crud
from .logger import logger
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/api/elements", tags=["Elements"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_element(payload: dict, db: Session = Depends(get_db)):
    results = []
    for key, value in payload.items():
        try:
            id = value["id"]
            data_raw = value["data"]
            device_name = value["deviceName"]
            data = [list(map(int, row.split())) for row in data_raw]
        except Exception as e:
            logger.error(f"Error parsing input: {e}")
            raise HTTPException(status_code=422, detail=f"Invalid data for entry {key}: {str(e)}")
        result = crud.create_result(db, id=id, data=data, device_name=device_name)
        results.append(result.id)
    logger.info(f"Inserted records: {results}")
    return {"stored": results}

@router.get("/", response_model=List[schemas.ResultResponse])
def list_results(
    created_date_gt: Optional[datetime] = None,
    created_date_lt: Optional[datetime] = None,
    average_before_gt: Optional[float] = None,
    average_before_lt: Optional[float] = None,
    average_after_gt: Optional[float] = None,
    average_after_lt: Optional[float] = None,
    data_size_gt: Optional[int] = None,
    data_size_lt: Optional[int] = None,
    db: Session = Depends(get_db)
):
    results = crud.get_filtered_results(
        db, created_date_gt, created_date_lt,
        average_before_gt, average_before_lt,
        average_after_gt, average_after_lt,
        data_size_gt, data_size_lt
    )
    return results

@router.get("/{result_id}", response_model=schemas.ResultResponse)
def get_result(result_id: str, db: Session = Depends(get_db)):
    result = crud.get_result_by_id(db, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result

@router.put("/{result_id}", response_model=schemas.ResultResponse)
def update_result(result_id: str, update: schemas.DeviceBase, db: Session = Depends(get_db)):
    updated = crud.update_result_device(db, result_id, update.device_name)
    if not updated:
        raise HTTPException(status_code=404, detail="Result not found")
    return updated

@router.delete("/{result_id}")
def delete_result(result_id: str, db: Session = Depends(get_db)):
    deleted = crud.delete_result(db, result_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Result not found")
    return {"message": f"Result {result_id} deleted"}
