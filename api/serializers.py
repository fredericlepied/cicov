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
        fields = ("id", "name", "url", "product_id", "result")

    product_id = serializers.PrimaryKeyRelatedField(source="product.id", read_only=True)
    result = serializers.SerializerMethodField()

    def get_result(self, rfe):
        latest_job_result = self.context["latest_job_result"]
        result = models.RFEResult.objects.filter(job_result=latest_job_result, rfe=rfe)
        if len(result):
            serializer = RFEResultSerializer(result[0])
            return serializer.data
        return None


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"

    job_results = serializers.SerializerMethodField()
    rfes = serializers.SerializerMethodField()

    def get_job_results(self, product):
        job_results = models.JobResult.objects.filter(product=product)
        latest_job_result = None
        if job_results:
            latest_job_result = job_results.latest("created")
            job_results = models.JobResult.objects.filter(
                product=product,
                build=latest_job_result.build
            )
        serializer = JobResultSerializer(
            job_results, many=True
        )
        return serializer.data

    def get_rfes(self, product):
        job_result = models.JobResult.objects.filter(product=product)
        latest_job_result = None
        if job_result:
            latest_job_result = job_result.latest("created")
        rfes = models.RFE.objects.filter(
            product__in=self.get_parent_products(product)
        )
        serializer = SimpleRFESerializer(
            rfes, many=True, context={"latest_job_result": latest_job_result}
        )
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
