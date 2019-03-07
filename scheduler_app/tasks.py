from datetime import datetime
from flask_mail import Message

import celery

from . import app, mail
from .config import MAIL_USERNAME
from .models import EmailSchedule


@celery.task()
def send_email(recipient, subject, body):
    with app.app_context():
        try:
            msg = Message(subject, sender=MAIL_USERNAME, recipients=[recipient])
            msg.body = body
            mail.send(msg)
        except Exception:
            return "Something went wrong, please check the config"
        return "Email sent to {}".format(recipient)


@celery.task()
def check_scheduled_emails():
    current_datetime_min = datetime.now().replace(second=0, microsecond=0)
    current_datetime_max = datetime.now().replace(second=59)

    # check for scheduled emails to be sent at current time
    queryset = EmailSchedule.query.filter(
        EmailSchedule.timestamp >= current_datetime_min,
        EmailSchedule.timestamp <= current_datetime_max
    ).all()

    for item in queryset:
        # push scheduled emails to queue to be sent
        send_email.delay(
            item.contact_email,
            item.email_subject,
            item.email_content
        )
    return "{} Email Pushed to queue at {}".format(len(queryset), current_datetime_min)
