from sqlalchemy.orm import Session

from app.models.campaign_task import CampaignTask


def create_campaign_tasks(db: Session, tasks: list[CampaignTask]) -> list[CampaignTask]:
    previous_task: CampaignTask | None = None
    for task in tasks:
        if previous_task is not None:
            task.depends_on_task_id = previous_task.id
        db.add(task)
        db.flush()
        db.refresh(task)
        previous_task = task
    db.commit()
    return tasks


def get_campaign_task(db: Session, campaign_id: int, task_id: int) -> CampaignTask | None:
    return (
        db.query(CampaignTask)
        .filter(CampaignTask.campaign_id == campaign_id, CampaignTask.id == task_id)
        .first()
    )


def list_campaign_tasks(db: Session, campaign_id: int) -> list[CampaignTask]:
    return (
        db.query(CampaignTask)
        .filter(CampaignTask.campaign_id == campaign_id)
        .order_by(CampaignTask.order_index.asc())
        .all()
    )


def update_campaign_task(db: Session, task: CampaignTask) -> CampaignTask:
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_downstream_tasks(db: Session, task: CampaignTask) -> list[CampaignTask]:
    return (
        db.query(CampaignTask)
        .filter(CampaignTask.campaign_id == task.campaign_id, CampaignTask.depends_on_task_id == task.id)
        .order_by(CampaignTask.order_index.asc())
        .all()
    )


def count_tasks_by_status(db: Session, campaign_id: int) -> dict[str, int]:
    counts = {status: 0 for status in ["pending", "ready", "in_progress", "blocked", "review", "completed", "cancelled"]}
    for task in list_campaign_tasks(db, campaign_id):
        counts[task.status] = counts.get(task.status, 0) + 1
    return counts


def list_ready_tasks(db: Session, campaign_id: int) -> list[CampaignTask]:
    tasks = (
        db.query(CampaignTask)
        .filter(CampaignTask.campaign_id == campaign_id, CampaignTask.status == "ready")
        .all()
    )
    rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return sorted(tasks, key=lambda task: (rank.get(task.priority, 99), task.order_index))
