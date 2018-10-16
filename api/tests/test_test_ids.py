from rest_framework.test import APITestCase

from api import models, serializers
from api.tests import factories


class TestTestCase(APITestCase):

    def test_test_factory(self):
        test = factories.TestFactory(name="factory")
        self.assertEqual(test.name, "factory")

    def test_test_serializer(self):
        serializer = serializers.TestSerializer(data={"name": "serializer"})
        serializer.is_valid()
        test = serializer.save()
        test.refresh_from_db()
        self.assertEqual(test.name, "serializer")

    def test_create_test(self):
        self.assertEqual(0, models.Test.objects.count())
        request = self.client.post("/api/tests", {"name": "p1"})
        self.assertEqual(201, request.status_code)
        self.assertEqual(1, models.Test.objects.count())

    def test_get_no_tests(self):
        request = self.client.get("/api/tests")
        self.assertEqual(0, len(request.data))

    def test_get_tests(self):
        test = factories.TestFactory()
        request = self.client.get("/api/tests")
        self.assertEqual(1, len(request.data))
        self.assertEqual(test.name, request.data[0]["name"])

    def test_get_test(self):
        test = factories.TestFactory()
        request = self.client.get("/api/tests/%s" % test.id)
        self.assertEqual(test.name, request.data["name"])

    def test_update_test(self):
        test = factories.TestFactory()
        self.assertNotEqual("updated", test.name)
        request = self.client.put("/api/tests/%s" %
                                  test.id, {"name": "updated"})
        self.assertEqual(200, request.status_code)
        test_updated = models.Test.objects.get(id=test.id)
        self.assertEqual("updated", test_updated.name)

    def test_delete_test(self):
        test = factories.TestFactory()
        self.assertEqual(1, models.Test.objects.all().count())
        request = self.client.delete("/api/tests/%s" % test.id)
        self.assertEqual(204, request.status_code)
        self.assertEqual(0, models.Test.objects.all().count())
