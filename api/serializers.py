from rest_framework import serializers

from api import models


class RFESerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RFE
        fields = "__all__"


class JobResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobResult
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"

    rfes = RFESerializer(read_only=True, many=True)
    job_results = JobResultSerializer(read_only=True, many=True)


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Test
        fields = "__all__"

