from rest_framework.test import APITestCase
from inventory.models import Product, Order


class ProductTest(APITestCase):
    def setUp(self):
        self.p1_data = {
            'name': 'p1',
            'description': 't',
            'price': 300,
            'quantity_available': 6
        }

        self.p2_data = {
            'name': 'p2',
            'description': 't',
            'price': 3245,
            'quantity_available': 1
        }
        self.p1 = Product.objects.create(**self.p1_data)
        self.p2 = Product.objects.create(**self.p2_data)

    def test_create(self):
        response = self.client.post(
            '/inventory/orders/', {
                'customer_email_address': 't@t.com',
                'products': [self.p1.id, self.p2.id]
            })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.first().customer_email_address,
                         't@t.com')
        self.assertEqual(
            Product.objects.get(id=self.p1.id).quantity_available,
            self.p1.quantity_available - 1)
        self.assertEqual(
            Product.objects.get(id=self.p2.id).quantity_available,
            self.p2.quantity_available - 1)

    def test_cancel(self):
        order = Order.objects.create_order(customer_email_address='a@a.com',
                                           products=[1])
        self.assertEqual(
            Product.objects.get(id=self.p1.id).quantity_available,
            self.p1.quantity_available - 1)
        response = self.client.put('/inventory/orders/%d/cancel/' % order.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Product.objects.get(id=self.p1.id).quantity_available,
            self.p1.quantity_available)

    def test_update(self):
        order = Order.objects.create_order(customer_email_address='a@a.com',
                                           products=[1, 2])
        self.assertEqual(
            Product.objects.get(id=self.p1.id).quantity_available,
            self.p1.quantity_available - 1)
        self.assertEqual(
            Product.objects.get(id=self.p2.id).quantity_available,
            self.p2.quantity_available - 1)
        response = self.client.put('/inventory/orders/%d/' % order.id, {
            "customer_email_address": "hh@aa.com",
            "products": [2]
        })
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            Order.objects.get(pk=order.pk).products.values_list(
                'id', flat=True),
            ['2'])
        self.assertEqual(
            Product.objects.get(id=self.p1.id).quantity_available,
            self.p1.quantity_available)
        self.assertEqual(
            Product.objects.get(id=self.p2.id).quantity_available,
            self.p2.quantity_available - 1)
