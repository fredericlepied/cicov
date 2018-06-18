from django.db import models


class Product(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    inherit = models.ForeignKey('self', models.SET_NULL, blank=True, null=True)
    url = models.URLField()

    class Meta:
        ordering = ('created',)


class RFE(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    testid = models.ManyToManyField('TestId')

    class Meta:
        ordering = ('created',)


class TestId(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)


class JobResult(models.Model):
    product = models.ForeignKey(Product, models.CASCADE)
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()

    class Meta:
        ordering = ('created',)


class TestResult(models.Model):
    job = models.ForeignKey(JobResult, models.CASCADE)
    test = models.ForeignKey(TestId, models.CASCADE)
    result = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
