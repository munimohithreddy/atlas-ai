from app.models.campaign_task import CampaignTask


class CampaignTaskDependencyService:
    def is_ready(self, task: CampaignTask, all_tasks: list[CampaignTask]) -> bool:
        if task.depends_on_task_id is None:
            return True
        dependency = next((item for item in all_tasks if item.id == task.depends_on_task_id), None)
        if dependency is None:
            return False
        return dependency.status in {"completed", "cancelled"}

    def validate(self, task: CampaignTask, all_tasks: list[CampaignTask]) -> None:
        if task.depends_on_task_id == task.id:
            raise ValueError("A task cannot depend on itself.")
        dependency = next((item for item in all_tasks if item.id == task.depends_on_task_id), None)
        if dependency is None and task.depends_on_task_id is not None:
            raise ValueError("Task dependency must belong to the same campaign.")

    def detect_circular_dependency(self, task: CampaignTask, all_tasks: list[CampaignTask]) -> None:
        seen: set[int] = set()
        current = task
        while current.depends_on_task_id is not None:
            if current.depends_on_task_id in seen:
                raise ValueError("Circular task dependency detected.")
            seen.add(current.depends_on_task_id)
            dependency = next((item for item in all_tasks if item.id == current.depends_on_task_id), None)
            if dependency is None:
                break
            current = dependency
