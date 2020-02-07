from django.db import models


CREATED = 'created'
CANCELEU = 'canceled'
IN_PROCESSING = 'in_processing'
DELIVERED = 'delivered'
ORDER_STATUS = [
    (CREATED, 'Created'),
    (IN_PROCESSING, 'In Processing'),
    (CANCELEU, 'Canceled'),
    (DELIVERED, 'Delivered'),
]


class Product(models.Model):
    name = models.TextField()
    description = models.TextField()
    price = models.IntegerField(help_text='cent')  # use as cent
    quantity_available = models.IntegerField()


class Order(models.Model):
    products = models.ManyToManyField(Product)
    customer_email_address = models.EmailField()
    date_order_placed = models.DateTimeField(auto_now_add=True)
    date_order_updated = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)

