from datetime import datetime, timezone

from app.repositories.campaign_repository import update_campaign
from app.repositories.campaign_task_repository import (
    get_campaign_task,
    list_campaign_tasks,
    list_downstream_tasks,
    update_campaign_task,
)
from app.services.campaigns.task_dependencies import CampaignTaskDependencyService


class CampaignTaskService:
    def __init__(self, dependency_service: CampaignTaskDependencyService | None = None) -> None:
        self.dependency_service = dependency_service or CampaignTaskDependencyService()

    def get_task(self, db, campaign_id: int, task_id: int):
        return get_campaign_task(db, campaign_id, task_id)

    def update_task(self, db, campaign, task, payload):
        if campaign.status == "archived":
            raise ValueError("Archived campaigns cannot be modified.")
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        self._recalculate_readiness(db, campaign, task)
        return update_campaign_task(db, task)

    def start(self, db, campaign, task):
        self._require_startable(campaign, task)
        self._ensure_dependencies_ready(db, task)
        task.status = "in_progress"
        task.started_at = task.started_at or datetime.now(timezone.utc)
        self._set_campaign_building(db, campaign)
        return update_campaign_task(db, task)

    def block(self, db, campaign, task, blocked_reason: str):
        self._require_modifiable(campaign)
        if not blocked_reason.strip():
            raise ValueError("Blocked reason is required.")
        task.status = "blocked"
        task.blocked_reason = blocked_reason
        return update_campaign_task(db, task)

    def unblock(self, db, campaign, task):
        self._require_modifiable(campaign)
        task.blocked_reason = None
        task.status = "ready" if self.dependency_service.is_ready(task, list_campaign_tasks(db, campaign.id)) else "pending"
        return update_campaign_task(db, task)

    def review(self, db, campaign, task):
        self._require_modifiable(campaign)
        task.status = "review"
        return update_campaign_task(db, task)

    def complete(
        self,
        db,
        campaign,
        task,
        completion_notes: str | None = None,
        actual_hours: float | None = None,
    ):
        self._require_modifiable(campaign)
        task.status = "completed"
        task.completed_at = datetime.now(timezone.utc)
        task.completion_notes = completion_notes
        task.actual_hours = actual_hours
        update_campaign_task(db, task)
        self._recalculate_downstream(db, campaign, task)
        self._recalculate_campaign_status(db, campaign)
        return task

    def cancel(self, db, campaign, task):
        self._require_modifiable(campaign)
        task.status = "cancelled"
        update_campaign_task(db, task)
        self._recalculate_downstream(db, campaign, task)
        self._recalculate_campaign_status(db, campaign)
        return task

    def reopen(self, db, campaign, task, reason: str):
        self._require_modifiable(campaign)
        if campaign.status in {"ready", "approved"}:
            campaign.status = "building"
            update_campaign(db, campaign)
        task.status = "in_progress" if campaign.status == "building" else "ready"
        task.blocked_reason = reason
        task.completed_at = None
        return update_campaign_task(db, task)

    def recalculate_initial_readiness(self, db, campaign):
        tasks = list_campaign_tasks(db, campaign.id)
        self.recalculate_campaign_readiness(db, campaign, tasks)
        return tasks

    def recalculate_campaign_readiness(self, db, campaign, tasks=None):
        all_tasks = tasks if tasks is not None else list_campaign_tasks(db, campaign.id)
        for task in all_tasks:
            if task.status == "cancelled":
                continue
            if task.depends_on_task_id is None:
                if campaign.status in {"approved", "building"} and task.status == "pending":
                    task.status = "ready"
                    update_campaign_task(db, task)
                continue
            dependency = next((item for item in all_tasks if item.id == task.depends_on_task_id), None)
            if dependency and dependency.status == "completed" and task.status == "pending":
                task.status = "ready"
                update_campaign_task(db, task)
            elif dependency and dependency.status != "completed" and task.status == "ready":
                task.status = "pending"
                update_campaign_task(db, task)
        return all_tasks

    def _require_modifiable(self, campaign):
        if campaign.status == "archived":
            raise ValueError("Archived campaigns cannot be modified.")
        if campaign.status == "paused":
            raise ValueError("Paused campaigns cannot be modified until resumed.")

    def _require_startable(self, campaign, task):
        self._require_modifiable(campaign)
        if campaign.status == "planning":
            raise ValueError("Campaign tasks cannot start while the campaign is planning.")
        if task.status not in {"ready", "blocked"}:
            raise ValueError("Task cannot be started from its current status.")

    def _set_campaign_building(self, db, campaign):
        if campaign.status == "approved":
            campaign.status = "building"
            update_campaign(db, campaign)

    def _recalculate_downstream(self, db, campaign, task):
        tasks = list_campaign_tasks(db, campaign.id)
        for downstream in list_downstream_tasks(db, task):
            if self.dependency_service.is_ready(downstream, tasks) and downstream.status == "pending":
                downstream.status = "ready"
                update_campaign_task(db, downstream)
            elif not self.dependency_service.is_ready(downstream, tasks) and downstream.status == "ready":
                downstream.status = "pending"
                update_campaign_task(db, downstream)

    def _recalculate_campaign_status(self, db, campaign):
        tasks = list_campaign_tasks(db, campaign.id)
        executable = [task for task in tasks if task.status != "cancelled"]
        if executable and all(task.status == "completed" for task in executable):
            if campaign.status != "published":
                campaign.status = "ready"
                update_campaign(db, campaign)

    def _ensure_dependencies_ready(self, db, task):
        if task.depends_on_task_id is None:
            return
        tasks = list_campaign_tasks(db, task.campaign_id)
        dependency = next((item for item in tasks if item.id == task.depends_on_task_id), None)
        if dependency is not None and dependency.status != "completed":
            raise ValueError("Task dependencies are not ready.")

    def _recalculate_readiness(self, db, campaign, task):
        tasks = list_campaign_tasks(db, campaign.id)
        if self.dependency_service.is_ready(task, tasks) and task.status == "pending":
            task.status = "ready"
