from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from store.settings import EMAIL_HOST_USER, MAIN_PATH


# Create your models here.

class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    expiration = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'email  to {self.user.email}'

    def send_email_message(self):
        link = reverse('users:verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{MAIN_PATH}{link}'
        formatted_expiration = self.expiration.strftime("%H:%M %d-%m-%Y")
        subject = f'Confirm Your Account Authorization, {self.user}'  # try with username
        message = f'''To confirm your authorization, please click the link below:

{verification_link}

The link is valid for {formatted_expiration}
        '''

        send_mail(subject=subject,
                  message=message,
                  from_email=EMAIL_HOST_USER,
                  recipient_list=[self.user.email]
                  )

    def is_expired(self):
        return True if self.expiration <= now() else False
