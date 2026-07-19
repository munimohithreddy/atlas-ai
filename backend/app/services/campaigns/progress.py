from app.repositories.campaign_task_repository import list_campaign_tasks, list_ready_tasks


class CampaignProgressService:
    def build_progress(self, db, campaign) -> dict:
        tasks = list_campaign_tasks(db, campaign.id)
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task.status == "completed")
        active_tasks = sum(1 for task in tasks if task.status in {"ready", "in_progress", "review"})
        blocked_tasks = sum(1 for task in tasks if task.status == "blocked")
        cancelled_tasks = sum(1 for task in tasks if task.status == "cancelled")
        executable = [task for task in tasks if task.status != "cancelled"]
        completion_percentage = round((completed_tasks / len(executable)) * 100) if executable else 0
        ready_tasks = list_ready_tasks(db, campaign.id)
        next_ready_task = ready_tasks[0] if ready_tasks else next((task for task in tasks if task.status == "ready"), None)
        has_blockers = blocked_tasks > 0
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "active_tasks": active_tasks,
            "blocked_tasks": blocked_tasks,
            "cancelled_tasks": cancelled_tasks,
            "completion_percentage": completion_percentage,
            "next_ready_task": (
                {
                    "id": next_ready_task.id,
                    "title": next_ready_task.title,
                    "status": next_ready_task.status,
                    "order_index": next_ready_task.order_index,
                }
                if next_ready_task
                else None
            ),
            "has_blockers": has_blockers,
        }
