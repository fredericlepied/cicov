from rest_framework import serializers
from cicovapp.models import (Product, RFE, TestId, JobResult, TestResult,
                             RFEResult)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'created', 'name', 'inherit', 'url', 'rfes',
                  'job_results')


class DetailedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'created', 'name', 'inherit', 'url', 'rfes',
                  'job_results')


class RFESerializer(serializers.ModelSerializer):
    class Meta:
        model = RFE
        fields = ('id', 'created', 'name', 'product', 'url', 'testid')


class TestIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestId
        fields = ('id', 'created', 'name')


class JobResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResult
        fields = ('id', 'created', 'product', 'build', 'url', 'rfe_results')


class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ('id', 'created', 'job', 'test', 'result')


class RfeResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFEResult
        fields = ('id', 'rfe', 'created', 'job', 'percent', 'result')
