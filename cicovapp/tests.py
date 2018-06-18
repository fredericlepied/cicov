from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cicovapp.models import Product
from cicovapp.serializers import ProductSerializer
from cicovapp.views import product_list, product_detail


class SerializationTests(TestCase):
    def test_serialization(self):
        p = Product(name="OSP", version="10", url="http://redhat.com/")
        p.save()
        s = ProductSerializer(p)
        self.assertEqual(len(s.data.keys()), 6, s.data)


class ApiTests(APITestCase):
    def setUp(self):
        self.p1 = {
            "name": "OSP",
            "url": "http://redhat.com/",
            "version": "10"
        }
        self.create_url = reverse(product_list)
        self.list_url = self.create_url

    def create_product(self):
        response = self.client.post(self.create_url, self.p1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        return response

    def test_create_product(self):
        self.create_product()

    def test_create_product_inherited(self):
        response = self.create_product()
        self.p1['inherit'] = response.data['id']
        self.p1["version"] = "11"
        response = self.create_product()
        self.assertNotEqual(response.data['id'], self.p1['inherit'])

    def test_list_products(self):
        self.create_product()
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 1)

    def test_product_detail(self):
        self.create_product()
        detail_url = reverse(product_detail, args=[1])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('version', response.data, response)
        self.assertEqual(response.data['version'], "10")
