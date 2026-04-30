from fastapi import APIRouter
from app.tasks.ai_tasks import process_ai_matching

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/match/{project_id}")
async def trigger_ai_matching(project_id: int):
    """Trigger AI matching në background."""
    task = process_ai_matching.delay(project_id)
    return {
        "message": "AI matching po procesohet",
        "task_id": task.id
    }

@router.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """Kontrollo statusin e task-ut."""
    from app.tasks.celery_app import celery_app
    task = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result
    }