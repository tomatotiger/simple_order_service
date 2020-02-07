from rest_framework.test import APITestCase
from inventory.models import Product


class ProductTest(APITestCase):
    p1 = {
        'name': 'p1',
        'description': 't',
        'price': 300,
        'quantity_available': 6
    }
    p2 = {
        'name': 'p2',
        'description': 't',
        'price': 3245,
        'quantity_available': 1
    }

    def test_create(self):
        response = self.client.post('/inventory/products/', self.p1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.get(**self.p1).name, self.p1['name'])

    def test_create_with_missing_field(self):
        required_fields = [
            'name', 'description', 'price', 'quantity_available'
        ]
        for field in required_fields:
            response = self.client.post(
                '/inventory/products/',
                dict((f, self.p1[f]) for f in self.p1 if f != field),
            )
            self.assertEqual(response.status_code, 400)

    def test_retrieve(self):
        Product.objects.create(**self.p1)
        response = self.client.get('/inventory/products/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], self.p1['name'])

    def test_retrieve_404(self):
        response = self.client.get('/inventory/products/111/')
        self.assertEqual(response.status_code, 404)

    def test_list(self):
        # no data
        response = self.client.get('/inventory/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

        # with data
        Product.objects.create(**self.p1)
        Product.objects.create(**self.p2)
        response = self.client.get('/inventory/products/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.data[0]['name'],
                      [self.p1['name'], self.p2['name']])
        self.assertIn(response.data[1]['name'],
                      [self.p1['name'], self.p2['name']])

    def test_update_product(self):
        p = Product.objects.create(**self.p1)
        update_items = {
            'name': 'new name',
            'price': 9999,
            'description': 'new story',
            'quantity_available': 99
        }

        for f, v in update_items.items():
            new_data = self.p1
            new_data[f]=v
            response = self.client.put('/inventory/products/%d/' % p.id,
                                       new_data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(getattr(Product.objects.get(id=p.id), f), v)

    def test_delete_product(self):
        p = Product.objects.create(**self.p1)
        response = self.client.delete('/inventory/products/%d/' % p.id)
        self.assertQuerysetEqual(Product.objects.all(), [])
