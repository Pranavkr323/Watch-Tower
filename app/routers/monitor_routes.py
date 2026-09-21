from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.monitor_schema import CreateMonitor, MonitorResponse, UpdateMonitor
from app.crud.monitor_crud import create_monitor, update_monitor, delete_monitor, get_all_monitors, get_monitor_by_id
from app.enums import SortBy, SortOrder
from typing import List

router = APIRouter(
    prefix= "/monitor",
    tags=["Monitor"]
)

@router.get("/all",
            response_model= List[MonitorResponse])
def all_monitors(sort_by: SortBy | None = None,
                 sort_order: SortOrder | None = None,
                 user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)
                 ):

    user_id = user.user_id
    list_of_monitors = get_all_monitors(db, user_id, sort_by, sort_order)
    return list_of_monitors

@router.get("/{monitor_id}",
            response_model= MonitorResponse)
def get_single_monitor(monitor_id: int,
                        user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):

    user_id = user.user_id
    requested_monitor = get_monitor_by_id(db, monitor_id, user_id)
    if requested_monitor is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= "Monitor not found!")

    return requested_monitor

@router.post("/new_monitor",
             response_model=MonitorResponse)
def monitor_create(data: CreateMonitor,
                   user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):

    user_id = user.user_id
    new_monitor = create_monitor(db, data, user_id)
    if new_monitor is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail= "Monitor already exists!")
    return new_monitor

@router.patch("/{monitor_id}",
              response_model= MonitorResponse)

def monitor_update(data: UpdateMonitor,
                   monitor_id: int,
                   user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):

    user_id = user.user_id
    requested_monitor = update_monitor(db, data, monitor_id, user_id)

    if requested_monitor is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= "Monitor not Found!")
    elif requested_monitor == "duplicate":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail= "This monitor already exists")
    return requested_monitor

@router.delete("/{monitor_id}")
def monitor_delete(monitor_id: int,
                   user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):

    user_id = user.user_id
    deleted = delete_monitor(db, monitor_id, user_id)

    if deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Monitor not found!")

    return {"message": "Monitor deleted successfully"}
