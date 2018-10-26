from django import shortcuts
from rest_framework import viewsets, parsers, response, status
from api import models, serializers, junit_parser, stats
from url_filter.integrations.drf import DjangoFilterBackend


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class RFEViewSet(viewsets.ModelViewSet):
    queryset = models.RFE.objects.all()
    serializer_class = serializers.RFESerializer


class JobResultViewSet(viewsets.ModelViewSet):
    queryset = models.JobResult.objects.all()
    serializer_class = serializers.JobResultSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'product', 'build', 'jobname', 'result']


class TestViewSet(viewsets.ModelViewSet):
    queryset = models.Test.objects.all()
    serializer_class = serializers.TestSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id']


class FileUploadView(viewsets.ViewSet):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser)

    def create(self, request):
        for key in ("url", "product", "build", "result"):
            if key not in request.data:
                return response.Response(status=400)
        product = shortcuts.get_object_or_404(
            models.Product, id=request.data["product"]
        )
        if "jobname" in request.data:
            jobname = request.data["jobname"]
        else:
            # extract the job name from the URL:
            # http://<server>/<path>/<jobname>/<jobid>/
            parts = request.data["url"].split("/")
            if parts[-1] == "":
                jobname = parts[-3]
            else:
                jobname = parts[-2]
        try:
            job_result = models.JobResult.objects.get(
                product=product, url=request.data["url"],
                build=request.data["build"],
                jobname=jobname
            )
        except models.JobResult.DoesNotExist:
            job_result = models.JobResult(
                product=product, url=request.data["url"],
                build=request.data["build"],
                result=request.data["result"],
                jobname=jobname
            )
            job_result.save()
        test_results = []
        if "file" in request.data:
            for test in junit_parser.parse_tests(request.data["file"]):
                test_id, _ = models.Test.objects.get_or_create(name=test["name"])
                test_result, _ = models.TestResult.objects.get_or_create(
                    job_result=job_result,
                    test=test_id,
                    result=(test["status"] == "success"),
                )
                test_results.append({"test": test_id.id,
                                     "result": test_result.result})

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
