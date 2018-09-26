from os.path import dirname, join

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cicovapp.models import (Product, RFE, RFEResult, TestId)
from cicovapp.serializers import ProductSerializer
from cicovapp.views import (product_list, product_detail,
                            rfe_list, rfe_detail,
                            test_id_list, test_id_detail,
                            job_result_list, job_result_detail,
                            test_result_list, test_result_detail)

PRODUCT = "OSP10"


class SerializationTests(TestCase):
    def test_serialization(self):
        p = Product(name=PRODUCT, url="http://redhat.com/")
        p.save()
        s = ProductSerializer(p)
        self.assertEqual(len(s.data.keys()), 5, s.data)


class ApiTests(APITestCase):
    def setUp(self):
        self.p1 = {
            "name": PRODUCT,
            "url": "http://redhat.com/",
        }
        self.create_url = reverse(product_list)
        self.list_url = self.create_url

    def create_product(self):
        response = self.client.post(self.create_url, self.p1)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        return response

    def create_test_id(self, name="TEST_ID 1", url="http://bz.com/1"):
        response = self.client.post(reverse(test_id_list),
                                    {"name": name,
                                     "url": url})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        return response

    def create_rfe(self, id=1):
        res = self.create_test_id()
        res2 = self.create_test_id(name="TEST_ID 2", url="http://bz.com/2")
        response = self.client.post(reverse(rfe_list),
                                    {"name": "RFE 1",
                                     "product": id,
                                     "url": "http://bz.com/1",
                                     "testid": [res.data['id'],
                                                res2.data['id']]
                                     })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         response.data)
        self.assertIn('id', response.data)
        rfe = RFE.objects.get(pk=response.data['id'])
        self.assertEquals(len(rfe.testid.all()), 2, rfe.testid.all())
        response = self.client.get(reverse(rfe_detail, args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "RFE 1")

    def test_create_product(self):
        self.create_product()

    def test_create_product_inherited(self):
        response = self.create_product()
        self.p1['inherit'] = response.data['id']
        self.p1["product"] = "OSP11"
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
        self.assertIn('name', response.data, response)
        self.assertEqual(response.data['name'], PRODUCT)

    def test_create_rfe(self):
        res = self.create_product()
        self.create_rfe(res.data['id'])

    def test_create_test_id(self):
        self.create_test_id()
        response = self.client.get(reverse(test_id_detail, args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "TEST_ID 1")

    def test_create_job_result(self):
        response = self.create_product()
        response = self.client.post(reverse(job_result_list),
                                    {"product": response.data['id'],
                                     "build": "2018-06-20.1",
                                     "url": "http://jenkins.com/1"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        response = self.client.get(reverse(job_result_detail, args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['url'], "http://jenkins.com/1")

    def test_create_test_result(self):
        self.create_product()
        self.client.post(reverse(job_result_list),
                         {"product": 1,
                          "build": "2018-06-20.1",
                          "url": "http://jenkins.com/1"})
        self.client.post(reverse(test_id_list),
                         {"name": "TEST_ID 1",
                          "url": "http://bz.com/1"})
        response = self.client.post(reverse(test_result_list),
                                    {"job": 1,
                                     "test": 1,
                                     "result": True})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        response = self.client.get(reverse(test_result_detail, args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], True)

    def test_upload(self):
        xmlfile = open(join(dirname(__file__), 'tempest-results-full.1.xml'))
        res = self.create_product()
        self.create_rfe(res.data['id'])
        response = self.client.post("/upload/",
                                    {"product": PRODUCT,
                                     "url": "http://bz.com/1",
                                     "build": "2018-06-20.1",
                                     "file": xmlfile}, format='multipart')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(TestId.objects.filter(name="setUpClass (tempest.api.compute.admin.test_live_migration_negative.LiveMigrationNegativeTest)").count(), 0)
        self.assertEquals(TestId.objects.filter(name="tempest.api.compute.admin.test_simple_tenant_usage_negative.TenantUsagesNegativeTestJSON.test_get_usage_tenant_with_empty_tenant_id").count(), 1)
        rfe_results = RFEResult.objects.all()
        self.assertEquals(rfe_results.count(), 1)
        self.assertEquals(rfe_results[0].result, False)
        self.assertEquals(rfe_results[0].percent, 0)
        res = self.client.get("/rfe_results/")
        self.assertTrue(status.is_success(res.status_code))
        self.assertEquals(len(res.data), 1)
        self.assertEquals(res.data[0]["result"], False)
        self.assertEquals(res.data[0]["percent"], 0)
        res = self.client.get("/rfe_result/1/")
        self.assertEquals(res.data["result"], False)
        self.assertEquals(res.data["percent"], 0)
