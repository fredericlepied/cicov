from django import shortcuts
from rest_framework import viewsets, parsers, response, status
from api import models, serializers, junit_parser, stats


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class RFEViewSet(viewsets.ModelViewSet):
    queryset = models.RFE.objects.all()
    serializer_class = serializers.RFESerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = models.Test.objects.all()
    serializer_class = serializers.TestSerializer


class FileUploadView(viewsets.ViewSet):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser)

    def create(self, request):
        for key in ("url", "product", "file", "build"):
            if key not in request.data:
                return response.Response(status=400)
        product = shortcuts.get_object_or_404(
            models.Product, id=request.data["product"]
        )
        job_result, _ = models.JobResult.objects.get_or_create(
            product=product, url=request.data["url"], build=request.data["build"]
        )
        test_results = []
        for test in junit_parser.parse_tests(request.data["file"]):
            test_id, _ = models.Test.objects.get_or_create(name=test["name"])
            test_result, _ = models.TestResult.objects.get_or_create(
                job_result=job_result,
                test=test_id,
                result=(test["status"] == "success"),
            )
            test_results.append({"test": test_id.id, "result": test_result.result})

        while product:
            for rfe in models.RFE.objects.filter(product=product):
                tests = [{"id": t.id} for t in rfe.tests.all()]
                rfe_stats = stats.get_rfes_stats(tests, test_results)
                models.RFEResult.objects.update_or_create(
                    job_result=job_result,
                    rfe=rfe,
                    result=rfe_stats["result"],
                    percent=rfe_stats["percent"],
                )
            product = product.inherit
        return response.Response(status=status.HTTP_201_CREATED)
