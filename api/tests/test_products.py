from rest_framework.test import APITestCase

from api import models, serializers
from api.tests import factories


class ProductTestCase(APITestCase):
    def test_product_factory(self):
        product = factories.ProductFactory(name="factory")
        self.assertEqual(product.name, "factory")

    def test_product_serializer(self):
        serializer = serializers.ProductSerializer(
            data={"name": "serializer", "url": "https://example.org/products/1"}
        )
        serializer.is_valid()
        product = serializer.save()
        product.refresh_from_db()
        self.assertEqual(product.name, "serializer")

    def test_create_product(self):
        self.assertEqual(0, models.Product.objects.count())
        request = self.client.post(
            "/api/products", {"name": "p1", "url": "https://example.org/products/1"}
        )
        self.assertEqual(201, request.status_code)
        self.assertEqual(1, models.Product.objects.count())

    def test_get_no_products(self):
        request = self.client.get("/api/products")
        self.assertEqual(0, len(request.data))

    def test_get_products(self):
        product = factories.ProductFactory()
        request = self.client.get("/api/products")
        self.assertEqual(1, len(request.data))
        self.assertEqual(product.name, request.data[0]["name"])

    def test_get_products_with_rfes_and_job_results(self):
        product = factories.ProductFactory()
        rfe = factories.RFEFactory(product=product)
        job_result = factories.JobResultFactory(product=product)
        request = self.client.get("/api/products")
        self.assertEqual(rfe.id, request.data[0]["rfes"][0]["id"])
        self.assertEqual(job_result.id, request.data[0]["job_results"][0]["id"])

    def test_get_product(self):
        product = factories.ProductFactory()
        request = self.client.get("/api/products/%s" % product.id)
        self.assertEqual(product.name, request.data["name"])

    def test_update_product(self):
        product = factories.ProductFactory()
        self.assertNotEqual("updated", product.name)
        request = self.client.put(
            "/api/products/%s" % product.id,
            {"name": "updated", "url": "https://example.org/products/1"},
        )
        self.assertEqual(200, request.status_code)
        product_updated = models.Product.objects.get(id=product.id)
        self.assertEqual("updated", product_updated.name)

    def test_partial_update_product(self):
        product = factories.ProductFactory()
        self.assertNotEqual("updated", product.name)
        request = self.client.patch(
            "/api/products/%s" % product.id, {"name": "updated"}
        )
        self.assertEqual(200, request.status_code)
        product_updated = models.Product.objects.get(id=product.id)
        self.assertEqual("updated", product_updated.name)

    def test_delete_product(self):
        product = factories.ProductFactory()
        self.assertEqual(1, models.Product.objects.all().count())
        request = self.client.delete("/api/products/%s" % product.id)
        self.assertEqual(204, request.status_code)
        self.assertEqual(0, models.Product.objects.all().count())

    def test_view_products(self):
        product = factories.ProductFactory()
        request = self.client.get("/api/view/products")
        self.assertEqual(product.name, request.data[0]['name'])
