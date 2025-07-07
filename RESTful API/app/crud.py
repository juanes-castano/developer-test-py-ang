from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models

def get_or_create_device(db: Session, device_name: str):
    device = db.query(models.Device).filter_by(device_name=device_name).first()
    if not device:
        device = models.Device(device_name=device_name)
        db.add(device)
        db.commit()
        db.refresh(device)
    return device

def create_result(db: Session, id: str, data: list[list[int]], device_name: str):
    flat_data = [int(num) for row in data for num in row]
    avg_before = sum(flat_data) / len(flat_data)
    max_val = max(flat_data)
    normalized = [x / max_val for x in flat_data]
    avg_after = sum(normalized) / len(normalized)
    device = get_or_create_device(db, device_name)

    result = models.ResultEntry(
        id=id,
        device_id=device.id,
        average_before=avg_before,
        average_after=avg_after,
        data_size=len(flat_data)
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result

def get_filtered_results(db: Session,
    created_date_gt, created_date_lt,
    avg_before_gt, avg_before_lt,
    avg_after_gt, avg_after_lt,
    size_gt, size_lt
):
    filters = []
    if created_date_gt: filters.append(models.ResultEntry.created_date >= created_date_gt)
    if created_date_lt: filters.append(models.ResultEntry.created_date <= created_date_lt)
    if avg_before_gt: filters.append(models.ResultEntry.average_before >= avg_before_gt)
    if avg_before_lt: filters.append(models.ResultEntry.average_before <= avg_before_lt)
    if avg_after_gt: filters.append(models.ResultEntry.average_after >= avg_after_gt)
    if avg_after_lt: filters.append(models.ResultEntry.average_after <= avg_after_lt)
    if size_gt: filters.append(models.ResultEntry.data_size >= size_gt)
    if size_lt: filters.append(models.ResultEntry.data_size <= size_lt)

    return db.query(models.ResultEntry).filter(and_(*filters)).all()

def get_result_by_id(db: Session, result_id: str):
    return db.query(models.ResultEntry).filter_by(id=result_id).first()

def update_result_device(db: Session, result_id: str, new_device_name: str):
    result = get_result_by_id(db, result_id)
    if not result:
        return None
    device = get_or_create_device(db, new_device_name)
    result.device_id = device.id
    db.commit()
    db.refresh(result)
    return result

def delete_result(db: Session, result_id: str):
    result = get_result_by_id(db, result_id)
    if not result:
        return False
    db.delete(result)
    db.commit()
    return True
