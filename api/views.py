from django import shortcuts
from django.db.models import Q
from rest_framework import viewsets, parsers, response, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api import models, serializers, junit_parser, stats
from url_filter.integrations.drf import DjangoFilterBackend


class ProductViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.ProductSerializer
        return serializers.ProductsSerializer

    queryset = models.Product.objects.all()


class RFEViewSet(viewsets.ModelViewSet):
    queryset = models.RFE.objects.all()
    serializer_class = serializers.RFESerializer


class JobResultViewSet(viewsets.ModelViewSet):
    queryset = models.JobResult.objects.all()
    serializer_class = serializers.JobResultSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["id", "product", "build", "jobname", "result"]


class TestViewSet(viewsets.ModelViewSet):
    queryset = models.Test.objects.all()
    serializer_class = serializers.TestSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["id"]


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
                product=product,
                url=request.data["url"],
                build=request.data["build"],
                jobname=jobname,
            )
        except models.JobResult.DoesNotExist:
            job_result = models.JobResult(
                product=product,
                url=request.data["url"],
                build=request.data["build"],
                result=request.data["result"],
                jobname=jobname,
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
                test_results.append({"test": test_id.id, "result": test_result.result})

        while product:
            for rfe in models.RFE.objects.filter(product=product):
                tests = [{"id": t.id} for t in rfe.tests.all()]
                rfe_stats = stats.get_rfes_stats(tests, test_results)
                models.RFEResult.objects.update_or_create(
                    job_result=job_result,
                    rfe=rfe,
                    tested=rfe_stats["tested"],
                    result=rfe_stats["result"],
                    percent=rfe_stats["percent"],
                )
            product = product.inherit
        return response.Response(status=status.HTTP_201_CREATED)


@api_view(["GET"])
def view_products(request, format=None):
    content = []
    products = models.Product.objects.all()
    for product in products:
        builds = list(set([jr.build for jr in product.job_results.all()]))
        if len(builds) > 0:
            builds.sort(reverse=True)
            last_build = builds[0]
        else:
            last_build = None
        rfe_results = {}
        for jr in product.job_results.filter(build=last_build):
            for rr in jr.rfe_results.all():
                if rr.rfe.id not in rfe_results or rr.result is True:
                    rfe_results[rr.rfe.id] = rr.result
        successful_rfes = sum(
            [1 if rfe_results[rfeid] is True else 0 for rfeid in rfe_results]
        )
        unsuccessful_rfes = sum(
            [1 if rfe_results[rfeid] is False else 0 for rfeid in rfe_results]
        )
        not_tested_rfes = sum(
            [1 if rfe_results[rfeid] is None else 0 for rfeid in rfe_results]
        )
        content.append(
            {
                "id": product.id,
                "name": product.name,
                "url": product.url,
                "inherit": product.inherit.id if product.inherit else None,
                "successful_jobs": product.job_results.filter(
                    result="SUCCESS", build=last_build
                ).count(),
                "unsuccessful_jobs": product.job_results.filter(
                    ~Q(result="SUCCESS"), build=last_build
                ).count(),
                "successful_rfes": successful_rfes,
                "unsuccessful_rfes": unsuccessful_rfes,
                "not_tested_rfes": not_tested_rfes,
                "builds": builds,
            }
        )
    return Response(content)
