from app.tasks.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="send_welcome_email")
def send_welcome_email(user_email: str, username: str):
    """Send welcome email after registration."""
    logger.info(f"By sending a welcome email to {user_email}")
    # Email sending simulation
    logger.info(f"Email sent to {username} ({user_email})")
    return {"status": "sent", "email": user_email}

@celery_app.task(name="send_bid_notification")
def send_bid_notification(client_email: str, project_title: str, freelancer_name: str):
    """Notify the client when the freelancer sends an offer."""
    logger.info(f"Announcing {client_email} a new offer")
    logger.info(f"Project: {project_title} — Freelancer: {freelancer_name}")
    return {"status": "sent", "email": client_email}

@celery_app.task(name="send_contract_notification")
def send_contract_notification(freelancer_email: str, project_title: str):
    """Notify the freelancer when the contract is created."""
    logger.info(f"Announcing {freelancer_email} a new contract")
    return {"status": "sent", "email": freelancer_email}

@celery_app.task(name="send_payment_notification")
def send_payment_notification(freelancer_email: str, amount: float):
    """Notify the freelancer for payment."""
    logger.info(f"The payment {amount}$ was released to {freelancer_email}")
    return {"status": "sent", "amount": amount}