from app.tasks.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="process_ai_matching")
def process_ai_matching(project_id: int):
    """Proceson AI matching në background."""
    logger.info(f"Duke procesuar AI matching për projektin {project_id}")
    return {"status": "completed", "project_id": project_id}

@celery_app.task(name="update_freelancer_rating")
def update_freelancer_rating(freelancer_id: int):
    """Përditëso rating-un e freelancerit në background."""
    logger.info(f"Duke përditësuar rating-un e freelancerit {freelancer_id}")
    return {"status": "completed", "freelancer_id": freelancer_id}