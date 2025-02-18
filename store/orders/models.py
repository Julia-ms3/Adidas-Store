from django.db import models

from users.models import User


class Order(models.Model):
    CREATED = 1
    ON_WAY = 2
    COMPLETED = 3

    STATUS_CHOICES = (
        (CREATED, 'Created'),
        (ON_WAY, 'On Way'),
        (COMPLETED, 'Completed'),
    )  # can change on Enum

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.TextField()
    basket_history = models.JSONField(default=dict)
    created_time = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUS_CHOICES)
    order_creator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order №{self.id} from {self.order_creator} to {self.first_name} {self.last_name}'
