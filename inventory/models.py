from django.db import models
from django.db import IntegrityError, transaction
from django.db.models import F

CREATED = 'created'
CANCELED = 'canceled'
IN_PROCESSING = 'in_processing'
DELIVERED = 'delivered'
ORDER_STATUS = [
    (CREATED, 'Created'),
    (IN_PROCESSING, 'In Processing'),
    (CANCELED, 'Canceled'),
    (DELIVERED, 'Delivered'),
]


class Product(models.Model):
    name = models.TextField()
    description = models.TextField()
    price = models.IntegerField(help_text='cent')  # use as cent
    quantity_available = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderManager(models.Manager):
    def cancel_order(self, pk):
        with transaction.atomic():
            order = self.get(pk=pk)
            order.order_status = CANCELED
            for product in order.products.all():
                product.quantity_available += 1
                product.save()
            order.save()
            return order

    def update_order(self, instance, **kwargs):
        with transaction.atomic():
            products = kwargs.pop('products')
            self.filter(id=instance.id).update(**kwargs)

            #update products quantity
            existing_products = instance.products.all().values_list('id', flat=True)
            increase = [p for p in existing_products if p not in products]
            decrease = [p.id for p in products if p not in existing_products]
            instance.products.set(products)
            Product.objects.filter(id__in=increase).update(
                quantity_available=F('quantity_available') + 1)
            Product.objects.filter(id__in=decrease).update(
                quantity_available=F('quantity_available') - 1)
            return self.get(pk=instance.id)

    def create_order(self, **kwargs):
        with transaction.atomic():
            products = kwargs.pop('products')
            order = self.create(**kwargs)
            order.products.set(products)
            order.products.update(quantity_available=F('quantity_available') - 1)
            return order


class Order(models.Model):
    products = models.ManyToManyField(Product)
    customer_email_address = models.EmailField()
    date_order_placed = models.DateTimeField(auto_now_add=True)
    date_order_updated = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    objects = OrderManager()


class OrderLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
