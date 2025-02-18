from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    fields = (
        'order_creator', ('first_name', 'last_name', 'email'), 'basket_history', 'status',
        'address', 'created_time'

    )
    readonly_fields = ['created_time', 'order_creator']
