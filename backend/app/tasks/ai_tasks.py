from app.tasks.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="process_ai_matching")
def process_ai_matching(project_id: int):
    """It processes AI matching in the background."""
    logger.info(f"Processing AI matching for the project {project_id}")
    return {"status": "completed", "project_id": project_id}

@celery_app.task(name="update_freelancer_rating")
def update_freelancer_rating(freelancer_id: int):
    """Update the freelancer's rating in the background."""
    logger.info(f"Updating the freelancer's rating {freelancer_id}")
    return {"status": "completed", "freelancer_id": freelancer_id}