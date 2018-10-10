from django.db import models


class Product(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    inherit = models.ForeignKey('self', models.SET_NULL, blank=True, null=True)
    url = models.URLField()

    class Meta:
        ordering = ('created',)


class RFE(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, models.CASCADE, related_name='rfes')
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    testid = models.ManyToManyField('TestId', blank=True)

    class Meta:
        ordering = ('created',)


class TestId(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)


class JobResult(models.Model):
    product = models.ForeignKey(Product, models.CASCADE,
                                related_name='job_results')
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    build = models.CharField(max_length=100)

    class Meta:
        ordering = ('created',)


class TestResult(models.Model):
    job = models.ForeignKey(JobResult, models.CASCADE,
                            related_name='test_results')
    test = models.ForeignKey(TestId, models.CASCADE)
    result = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)


class RFEResult(models.Model):
    job = models.ForeignKey(JobResult, models.CASCADE,
                            related_name='rfe_results')
    rfe = models.ForeignKey(RFE, models.CASCADE)
    result = models.BooleanField()
    percent = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
