import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import EmailVerification, User


@shared_task()
def send_verification_email(user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(days=1)
    record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    record.send_email_message()
