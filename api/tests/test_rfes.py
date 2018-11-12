from rest_framework.test import APITestCase

from api import models, serializers
from api.tests import factories
from api.stats import get_rfes_stats


class RFETestCase(APITestCase):
    def test_rfe_factory(self):
        rfe = factories.RFEFactory(name="factory")
        self.assertEqual(rfe.name, "factory")

    def test_rfe_serializer(self):
        product = factories.ProductFactory()
        serializer = serializers.RFESerializer(
            data={
                "name": "serializer",
                "url": "https://example.org/rfes/1",
                "product": product.id,
            }
        )
        serializer.is_valid()
        rfe = serializer.save()
        rfe.refresh_from_db()
        self.assertEqual(rfe.name, "serializer")

    def test_create_rfe(self):
        product = factories.ProductFactory()
        test1 = factories.TestFactory(name="test id 1")
        test2 = factories.TestFactory(name="test id 2")
        self.assertEqual(0, models.RFE.objects.count())

        data = {
            "name": "p1",
            "url": "https://example.org/rfes/1",
            "product": product.id,
            "tests": [test1.id, test2.id],
        }
        request = self.client.post(
            "/api/rfes",
            data,
        )
        self.assertEqual(201, request.status_code)
        self.assertEqual(1, models.RFE.objects.count())
        for key in data:
            self.assertIn(key, request.data)
            self.assertEqual(data[key], request.data[key])

    def test_get_no_rfes(self):
        request = self.client.get("/api/rfes")
        self.assertEqual(0, len(request.data))

    def test_get_rfes(self):
        rfe = factories.RFEFactory()
        request = self.client.get("/api/rfes")
        self.assertEqual(1, len(request.data))
        self.assertEqual(rfe.name, request.data[0]["name"])

    def test_get_rfe(self):
        rfe = factories.RFEFactory()
        request = self.client.get("/api/rfes/%s" % rfe.id)
        self.assertEqual(rfe.name, request.data["name"])

    def test_update_rfe(self):
        rfe = factories.RFEFactory()
        self.assertNotEqual("updated", rfe.name)
        request = self.client.put(
            "/api/rfes/%s" % rfe.id,
            {"name": "updated", "url": rfe.url, "product": rfe.product.id},
        )
        self.assertEqual(200, request.status_code)
        rfe_updated = models.RFE.objects.get(id=rfe.id)
        self.assertEqual("updated", rfe_updated.name)

    def test_partial_update_rfe(self):
        rfe = factories.RFEFactory()
        self.assertNotEqual("updated", rfe.name)
        request = self.client.patch("/api/rfes/%s" % rfe.id, {"name": "updated"})
        self.assertEqual(200, request.status_code)
        rfe_updated = models.RFE.objects.get(id=rfe.id)
        self.assertEqual("updated", rfe_updated.name)

    def test_delete_rfe(self):
        rfe = factories.RFEFactory()
        self.assertEqual(1, models.RFE.objects.all().count())
        request = self.client.delete("/api/rfes/%s" % rfe.id)
        self.assertEqual(204, request.status_code)
        self.assertEqual(0, models.RFE.objects.all().count())

    def test_rfe_stats(self):
        test_results = [
            {"test": 1, "result": True},
            {"test": 2, "result": True},
            {"test": 3, "result": False},
            {"test": 4, "result": False},
        ]
        tests = [{"id": 1}, {"id": 2}, {"id": 3}]
        self.assertDictEqual(
            get_rfes_stats(tests, test_results), {"count": 3, "percent": 66.67,
                                                  "result": False,
                                                  "tested": True}
        )

    def test_rfe_stats_result_true_if_100_per_100(self):
        test_results = [
            {"test": 1, "result": True},
            {"test": 2, "result": True},
            {"test": 3, "result": True},
        ]
        tests = [{"id": 1}, {"id": 2}, {"id": 3}]
        self.assertDictEqual(
            get_rfes_stats(tests, test_results), {"count": 3, "percent": 100.0,
                                                  "result": True,
                                                  "tested": True}
        )
