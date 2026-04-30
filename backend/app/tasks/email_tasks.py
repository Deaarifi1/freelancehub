from app.tasks.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="send_welcome_email")
def send_welcome_email(user_email: str, username: str):
    """Dërgo email mirëseardhje pas regjistrimit."""
    logger.info(f"Duke dërguar email mirëseardhje te {user_email}")
    # Simulim i dërgimit të email-it
    logger.info(f"Email u dërgua te {username} ({user_email})")
    return {"status": "sent", "email": user_email}

@celery_app.task(name="send_bid_notification")
def send_bid_notification(client_email: str, project_title: str, freelancer_name: str):
    """Njofto klientin kur freelanceri dërgon ofertë."""
    logger.info(f"Duke njoftuar {client_email} për ofertë të re")
    logger.info(f"Projekti: {project_title} — Freelanceri: {freelancer_name}")
    return {"status": "sent", "email": client_email}

@celery_app.task(name="send_contract_notification")
def send_contract_notification(freelancer_email: str, project_title: str):
    """Njofto freelancerin kur kontrata është krijuar."""
    logger.info(f"Duke njoftuar {freelancer_email} për kontratë të re")
    return {"status": "sent", "email": freelancer_email}

@celery_app.task(name="send_payment_notification")
def send_payment_notification(freelancer_email: str, amount: float):
    """Njofto freelancerin për pagesë."""
    logger.info(f"Pagesa {amount}$ u lirua te {freelancer_email}")
    return {"status": "sent", "amount": amount}