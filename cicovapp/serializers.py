from rest_framework import serializers
from cicovapp.models import Product, RFE, TestId, JobResult, TestResult

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'created', 'name', 'version', 'inherit', 'url')

class RFESerializer(serializers.ModelSerializer):
    class Meta:
        model = RFE
        fields = ('id', 'created', 'title', 'url')

class TestIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestId
        fields = ('id', 'created', 'name')

class JobResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResult
        fields = ('id', 'created', 'product', 'url')

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ('id', 'created', 'job', 'test', 'result')
