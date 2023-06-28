import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from src.config import settings
from src.tasks.celery import celery
from src.tasks.email_templates import create_booking_confirmation_template


@celery.task
def process_pic(path: str):
    im_path = Path(path)
    im = Image.open(path)
    im_resize_1000_500 = im.resize((1000, 500))
    im_resize_200_100 = im.resize((200, 100))
    im_resize_1000_500.save(f"src/static/images/resized_1000_500_{im_path.name}")
    im_resize_200_100.save(f"src/static/images/resized_200_100_{im_path.name}")


@celery.task
def send_booking_confirmation_email(booking: dict, email_to: EmailStr):
    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        # server.send_message(msg_content)
        server.send_message(
            msg_content, from_addr=settings.EMAIL_HOST_USER, to_addrs=email_to
        )
