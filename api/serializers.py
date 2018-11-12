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
    product_id = serializers.PrimaryKeyRelatedField(source="product.id", read_only=True)

    class Meta:
        model = models.RFE
        fields = ("id", "name", "product_id")


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"

    rfes = serializers.SerializerMethodField()

    def get_rfes(self, obj):
        rfes = models.RFE.objects.filter(product__in=self.get_parent_products(obj))
        serializer = SimpleRFESerializer(rfes, many=True)
        return serializer.data

    def get_parent_products(self, product):
        products = []
        products.append(product)
        if product.inherit:
            products.extend(self.get_parent_products(product.inherit))
        return products


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"

    rfes = SimpleRFESerializer(read_only=True, many=True)
    job_results = JobResultSerializer(read_only=True, many=True)
