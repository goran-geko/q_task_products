import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from products.models import Product, Rating


class BaseTest(APITestCase):
    """
    Base test class that will be inherited by every test class in this file
    """
    def setUp(self):
        self.user1 = User.objects.create(username='tester1')
        self.user2 = User.objects.create(username='tester2')
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        self.auth_header1 = {'HTTP_AUTHORIZATION': f'Token {self.token1.key}'}
        self.auth_header2 = {'HTTP_AUTHORIZATION': f'Token {self.token2.key}'}
        self.product1 = Product.objects.create(name="Product 1", price=10.2)
        self.product2 = Product.objects.create(name="Product 2", price=100)
        self.product3 = Product.objects.create(name="Product 3", price=15.15)


class ProductListCreateAPIViewTest(BaseTest):
    def setUp(self):
        super(ProductListCreateAPIViewTest, self).setUp()
        self.url = reverse('product_list_create')

    def test_get(self):
        """
        Ensure we can list products
        """
        # Assert unauthorized access
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Assert authorized access
        response = self.client.get(self.url, **self.auth_header1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert records are returned
        data = json.loads(response.content)
        self.assertEqual(data.get('count'), 3)
        self.assertEqual(data.get('results')[0].get('name'), self.product1.name)

    def test_post(self):
        """
        Ensure we can create a product
        """
        payload_invalid = {
            "name": "Product 4",
            "rating": 0.0
        }
        payload_valid = {
            "name": "Product 4",
            "price": 12.12,
            "rating": 0.0
        }

        # Assert unauthorized access
        response = self.client.post(self.url, data=json.dumps(payload_valid), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Assert bad request
        response = self.client.post(self.url, data=json.dumps(payload_invalid), content_type='application/json',
                                    **self.auth_header1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert authorized access
        response = self.client.post(self.url, data=json.dumps(payload_valid), content_type='application/json',
                                    **self.auth_header1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert record is created
        self.assertEqual(Product.objects.all().count(), 4)
        self.assertEqual(Product.objects.last().name, payload_valid.get('name'))

        # Assert duplicate `name` field
        payload_valid['name'] = self.product1.name
        response = self.client.post(self.url, data=json.dumps(payload_valid), content_type='application/json',
                                    **self.auth_header1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Product.objects.all().count(), 4)


class ProductRetrieveUpdateDestroyAPIViewTest(BaseTest):
    def setUp(self):
        super(ProductRetrieveUpdateDestroyAPIViewTest, self).setUp()
        self.url = reverse('product_retrieve_update_destroy', kwargs={'pk': self.product1.pk})

    def test_get(self):
        """
        Ensure we can get a product
        """
        # Assert unauthorized access
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Assert authorized access
        response = self.client.get(self.url, **self.auth_header1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert record is returned
        data = json.loads(response.content)
        self.assertEqual(data.get('name'), self.product1.name)

    def test_put(self):
        """
        Ensure we can update a product using put method
        """
        payload_invalid = {
            "name": "Updated Product 1",
            "rating": 0.0
        }
        payload_valid = {
            "name": "Updated Product 1",
            "price": 50.15,
            "rating": 0.0
        }

        # Assert unauthorized access
        response = self.client.put(self.url, data=json.dumps(payload_valid), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Assert bad request
        response = self.client.put(self.url, data=json.dumps(payload_invalid), content_type='application/json',
                                   **self.auth_header1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert authorized access
        response = self.client.put(self.url, data=json.dumps(payload_valid), content_type='application/json',
                                   **self.auth_header1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert record is updated
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, payload_valid.get('name'))

    def test_patch(self):
        """
        Ensure we can update a product using patch method
        """
        payload = {
            "name": "Updated Product 1",
            "price": 50.15,
            "rating": 0.0
        }

        # Assert unauthorized access
        response = self.client.patch(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Assert authorized access
        response = self.client.patch(self.url, data=json.dumps(payload), content_type='application/json',
                                     **self.auth_header1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert record is updated
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, payload.get('name'))

    def test_delete(self):
        """
        Ensure we can delete a product
        """
        # Assert unauthorized access
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Assert authorized access
        response = self.client.delete(self.url, **self.auth_header1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Assert record is deleted
        with self.assertRaises(Product.DoesNotExist):
            self.product1.refresh_from_db()
        self.assertEqual(Product.objects.all().count(), 2)


class ProductCreateAPIViewTest(BaseTest):
    def setUp(self):
        super(ProductCreateAPIViewTest, self).setUp()
        self.url = reverse('product_create', kwargs={'pk': self.product1.pk})

    def test_post(self):
        payload1 = {'rating': 4.1}
        payload2 = {'rating': 3.9}

        # Assert unauthorized access
        response = self.client.post(self.url, data=json.dumps(payload1), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Assert authorized access
        response = self.client.post(self.url, data=json.dumps(payload1), content_type='application/json',
                                    **self.auth_header1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert rating is stored
        ratings = Rating.objects.all()
        self.assertEqual(ratings.count(), 1)

        # Assert Rating data
        rating = ratings.first()
        self.assertEqual(rating.user, self.user1)
        self.assertEqual(rating.product, self.product1)
        self.assertEqual(rating.rating, payload1.get('rating'))

        # Assert average rating on Product is calculated
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.rating, payload1.get('rating'))
        self.client.post(self.url, data=json.dumps(payload2), content_type='application/json', **self.auth_header2)
        self.product1.refresh_from_db()
        average = (payload1.get('rating') + payload2.get('rating')) / 2
        self.assertEqual(self.product1.rating, average)
