import os
from rest_framework.test import APITestCase

from api import models, serializers
from api.tests import factories


TEST_NAME = "tempest.api.compute.admin.test_simple_tenant_usage_negative.TenantUsagesNegativeTestJSON.test_get_usage_tenant_with_empty_tenant_id"


class UploadTestCase(APITestCase):
    def upload_file(self, product, fname):
        xmlfile = open(
            os.path.join(os.path.dirname(__file__), fname)
        )
        response = self.client.post(
            "/api/upload",
            {
                "product": product.id,
                "url": "https://example.org/jobs/1",
                "build": "2018-06-20.1",
                "file": xmlfile,
                "result": "SUCCESS",
            },
            format="multipart",
        )
        self.assertEqual(201, response.status_code)
        xmlfile.close()

    def test_upload(self):
        product = factories.ProductFactory()
        test = factories.TestFactory(
            name=TEST_NAME
        )
        rfe = factories.RFEFactory(product=product, tests=[test])
        test = models.Test.objects.get(
            name=TEST_NAME
        )
        self.upload_file(product, "tempest-results-full.1.xml")
        job_result = models.JobResult.objects.get(
            build="2018-06-20.1", url="https://example.org/jobs/1",
            product=product.id
        )
        self.assertEquals(job_result.jobname, "jobs")
        test_result = models.TestResult.objects.get(test=test,
                                                    job_result=job_result)
        self.assertTrue(test_result.result)
        rfe_result = models.RFEResult.objects.get(rfe=rfe)
        self.assertTrue(rfe_result.result)
        self.assertEquals(rfe_result.percent, 100.00)
        nb = models.TestResult.objects.filter(job_result=job_result).count()
        # change in tempest-results-full.2.xml is one test is failing
        self.upload_file(product, "tempest-results-full.2.xml")
        nb_job_result = models.JobResult.objects.all().count()
        self.assertEquals(nb_job_result, 1)
        nb2 = models.TestResult.objects.filter(job_result=job_result).count()
        self.assertEquals(nb, nb2)

    def test_upload_no_file(self):
        product = factories.ProductFactory()
        response = self.client.post(
            "/api/upload",
            {
                "product": product.id,
                "url": "https://example.org/jobs/1/",
                "build": "2018-06-20.1",
                "result": "FAILURE",
            },
            format="multipart",
        )
        self.assertEqual(201, response.status_code)
        job_result = models.JobResult.objects.get(
            build="2018-06-20.1", url="https://example.org/jobs/1/",
            product=product.id
        )
        self.assertEquals(job_result.jobname, "jobs")

    def test_upload_explicit_jobname(self):
        product = factories.ProductFactory()
        response = self.client.post(
            "/api/upload",
            {
                "product": product.id,
                "url": "https://example.org/jobs/1/",
                "build": "2018-06-20.1",
                "result": "FAILURE",
                "jobname": "myjob"
            },
            format="multipart",
        )
        self.assertEqual(201, response.status_code)
        job_result = models.JobResult.objects.get(
            build="2018-06-20.1", url="https://example.org/jobs/1/",
            product=product.id
        )
        self.assertEquals(job_result.jobname, "myjob")
