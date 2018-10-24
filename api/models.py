from django.db import models


class Base(models.Model):
    class Meta:
        abstract = True

    id = models.BigAutoField(primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)


class Product(Base):
    name = models.CharField(max_length=100)
    url = models.URLField()
    inherit = models.ForeignKey("self", models.SET_NULL, blank=True, null=True)


class Test(Base):
    name = models.CharField(max_length=255)


class RFE(Base):
    name = models.CharField(max_length=100)
    url = models.URLField()
    product = models.ForeignKey(Product, models.CASCADE, related_name="rfes")
    tests = models.ManyToManyField(Test, blank=True)


class JobResult(Base):
    url = models.URLField()
    build = models.CharField(max_length=100)
    product = models.ForeignKey(Product, models.CASCADE,
                                related_name="job_results")
    result = models.CharField(max_length=100)


class TestResult(Base):
    result = models.BooleanField()
    test = models.ForeignKey(Test, models.CASCADE)
    job_result = models.ForeignKey(
        JobResult, models.CASCADE, related_name="test_results"
    )


class RFEResult(Base):
    result = models.BooleanField()
    percent = models.FloatField()
    rfe = models.ForeignKey(RFE, models.CASCADE)
    job_result = models.ForeignKey(
        JobResult, models.CASCADE, related_name="rfe_results"
    )
