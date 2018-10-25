from rest_framework import serializers

from api import models


class RFESerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RFE
        fields = "__all__"


class RFEResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RFEResult
        fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Test
        fields = "__all__"


class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestResult
        fields = "__all__"


class JobResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobResult
        fields = "__all__"

    test_results = TestResultSerializer(read_only=True, many=True)
    rfe_results = RFEResultSerializer(read_only=True, many=True)


class SimpleRFESerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RFE
        fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"

    rfes = SimpleRFESerializer(read_only=True, many=True)
    job_results = JobResultSerializer(read_only=True, many=True)
