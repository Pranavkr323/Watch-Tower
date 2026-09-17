from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Monitor
from app.schemas.monitor_schema import CreateMonitor, UpdateMonitor

def create_monitor(db: Session,
                   data: CreateMonitor):
    new_monitor = Monitor(
        product_link = data.product_link,
        threshold = data.threshold
    )

    db.add(new_monitor)
    db.commit()
    db.refresh(new_monitor)
    return new_monitor

