import factory

from api import models


class ProductFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Product

    name = "Product 1"
    url = "https://example.org/products/1"


class TestFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Test

    name = "Test 1"


class RFEFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.RFE

    name = "RFE 1"
    url = "https://example.org/rfes/1"
    product = factory.SubFactory(ProductFactory)

    @factory.post_generation
    def tests(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for test in extracted:
                self.tests.add(test)


class JobResultFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.JobResult

    url = "https://example.org/jobs/1"
    build = "2018-06-20.1"
    product = factory.SubFactory(ProductFactory)
