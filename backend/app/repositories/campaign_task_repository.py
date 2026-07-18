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


def list_campaign_tasks(db: Session, campaign_id: int) -> list[CampaignTask]:
    return (
        db.query(CampaignTask)
        .filter(CampaignTask.campaign_id == campaign_id)
        .order_by(CampaignTask.order_index.asc())
        .all()
    )
