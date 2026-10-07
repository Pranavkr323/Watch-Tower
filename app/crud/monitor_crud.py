from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Monitor
from app.schemas.monitor_schema import CreateMonitor, UpdateMonitor
from app.enums import SortBy, SortOrder
from app.utils.redis import r
from app.schemas.monitor_schema import MonitorResponse

def create_monitor(db: Session,
                   data: CreateMonitor,
                   user_id: int):

    existing = get_monitor_by_link(db, str(data.product_link), user_id)
    if existing is not None:
        return None

    new_monitor = Monitor(
        product_link = str(data.product_link),
        threshold = data.threshold,
        user_id = user_id
    )

    db.add(new_monitor)
    db.commit()
    db.refresh(new_monitor)
    return new_monitor

def get_monitor_by_id(db: Session,
                      monitor_id: int,
                      user_id: int):
    key = f"monitor:{user_id}:{monitor_id}"
    cached = r.get(key)
    if cached:
        return MonitorResponse.model_validate_json(cached)

    statement = select(Monitor).where(Monitor.monitor_id == monitor_id,
                                      Monitor.user_id == user_id)
    monitor = db.execute(statement).scalar_one_or_none()
    if monitor:
        monitor_resp = MonitorResponse.model_validate(monitor)
        r.set(key, monitor_resp.model_dump_json(), ex= 300)
        return monitor_resp
    return None

def get_all_monitors(db: Session,
                     user_id: int,
                     sort_by: SortBy | None = None,
                     sort_order: SortOrder | None = None):
    statement = select(Monitor).where(Monitor.user_id == user_id)

    if sort_by is not None:
        if sort_by == SortBy.CREATED_AT:
            column = Monitor.created_at
        elif sort_by == SortBy.UPDATED_AT:
            column = Monitor.updated_at

        if sort_order == SortOrder.ASCENDING:
            statement = statement.order_by(column.asc())

        if sort_order == SortOrder.DESCENDING:
            statement = statement.order_by(column.desc())

    return db.execute(statement).scalars().all()

def get_monitor_by_link(
                        db: Session,
                        product_link: str,
                        user_id: int):

    statement = select(Monitor).where(
        Monitor.product_link == product_link,
        Monitor.user_id == user_id
    )

    return db.execute(statement).scalar_one_or_none()

def update_monitor(db: Session,
                   data: UpdateMonitor,
                   monitor_id: int,
                   user_id: int):

    statement = select(Monitor).where(
        Monitor.monitor_id == monitor_id,
        Monitor.user_id == user_id
    )
    requested_monitor = db.execute(statement).scalar_one_or_none()
    if requested_monitor is None:
        return None

    if data.product_link is not None:
        existing = get_monitor_by_link(db, str(data.product_link), user_id)

        if existing is not None and existing.monitor_id != monitor_id:
            return "duplicate"
        requested_monitor.product_link = str(data.product_link)
    if data.threshold is not None:
        requested_monitor.threshold = data.threshold

    db.commit()
    db.refresh(requested_monitor)
    key = f"monitor:{user_id}:{monitor_id}"
    r.delete(key)
    return requested_monitor


def delete_monitor(db: Session,
                   monitor_id: int,
                   user_id: int):
    statement = select(Monitor).where(
        Monitor.monitor_id == monitor_id,
        Monitor.user_id == user_id
    )
    requested_monitor = db.execute(statement).scalar_one_or_none()
    if requested_monitor is None:
        return None

    db.delete(requested_monitor)
    db.commit()
    key = f"monitor:{user_id}:{monitor_id}"
    r.delete(key)

    return True
