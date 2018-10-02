from django.shortcuts import get_object_or_404
from junitparser import JUnitXml
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from cicovapp.models import (Product, RFE, TestId, JobResult, TestResult,
                             RFEResult)
from cicovapp.serializers import (ProductSerializer, RFESerializer,
                                  TestIdSerializer, JobResultSerializer,
                                  TestResultSerializer, RfeResultSerializer)


@api_view(['GET', 'POST'])
def product_list(request):
    """
    List all code products, or create a new product.
    """
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    """
    Retrieve, update or delete a product.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def rfe_list(request):
    """
    List all code rfes, or create a new rfe.
    """
    if request.method == 'GET':
        rfes = RFE.objects.all()
        serializer = RFESerializer(rfes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RFESerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def rfe_detail(request, pk):
    """
    Retrieve, update or delete a rfe.
    """
    try:
        rfe = RFE.objects.get(pk=pk)
    except RFE.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RFESerializer(rfe)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RFESerializer(rfe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        rfe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def test_id_list(request):
    """
    List all code TestIds, or create a new TestId.
    """
    if request.method == 'GET':
        TestIds = TestId.objects.all()
        serializer = TestIdSerializer(TestIds, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TestIdSerializer(data=request.data)
        if serializer.is_valid():
            try:
                test_id = TestId.objects.get(name=serializer.validated_data['name'])
                serializer = TestIdSerializer(test_id)
            except TestId.DoesNotExist:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def test_id_detail(request, pk):
    """
    Retrieve, update or delete a TestId.
    """
    try:
        test_id = TestId.objects.get(pk=pk)
    except TestId.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TestIdSerializer(test_id)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TestIdSerializer(test_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        test_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def job_result_list(request):
    """
    List all code job_results, or create a new job_result.
    """
    if request.method == 'GET':
        job_results = JobResult .objects.all()
        serializer = JobResultSerializer(job_results, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = JobResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def job_result_detail(request, pk):
    """
    Retrieve, update or delete a job_result.
    """
    try:
        job_result = JobResult.objects.get(pk=pk)
    except JobResult.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JobResultSerializer(job_result)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = JobResultSerializer(job_result, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        job_result.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def test_result_list(request):
    """
    List all code test_results, or create a new test_result.
    """
    if request.method == 'GET':
        test_results = TestResult .objects.all()
        serializer = TestResultSerializer(test_results, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TestResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def test_result_detail(request, pk):
    """
    Retrieve, update or delete a test_result.
    """
    try:
        test_result = TestResult.objects.get(pk=pk)
    except TestResult.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TestResultSerializer(test_result)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TestResultSerializer(test_result, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        test_result.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def testname(testcase):
    idx = testcase.name.find('[')
    if idx != -1:
        return testcase.classname + '.' + testcase.name[:idx]
    else:
        return testcase.classname + '.' + testcase.name


def teststatus(testcase):
    if testcase.result is None:
        return "success"
    else:
        return testcase.result._elem.tag


class FileUploadView(APIView):
    parser_classes = (FormParser, MultiPartParser,)

    def post(self, request):
        for key in ('url', 'product', 'file', 'build'):
            if key not in request.data:
                return Response(status=400)
        product = get_object_or_404(Product, name=request.data['product'])
        print('Ingesting %s %s from %s' % (request.data['product'], request.data['build'], request.data['url']))
        JobResult.objects.filter(product=product, url=request.data['url'],
                                 build=request.data['build']).delete()
        job_result = JobResult(product=product, url=request.data['url'],
                               build=request.data['build'])
        job_result.save()
        for file_ in request.data.pop('file'):
            xml = JUnitXml.fromfile(file_)
            for suite in xml:
                if suite.classname != '' and teststatus(suite) != 'skipped':
                    test_id = TestId.objects.get_or_create(
                        name=testname(suite))[0]
                    test_id.save()
                    test_result = TestResult(
                        job=job_result,
                        test=test_id,
                        result=(teststatus(suite) == 'success'))
                    test_result.save()
        # use a special test id for config settings
        if 'config' in request.data:
            for cfg in request.data.pop('config'):
                test_id = TestId.objects.get_or_create(
                    name='config.' + cfg)[0]
                test_id.save()
                test_result = TestResult(
                    job=job_result,
                    test=test_id,
                    result=True)
                test_result.save()
                print(test_result.test.name)
        while product:
            for rfe in RFE.objects.filter(product=product):
                testids = rfe.testid.all()
                count = 0
                success = 0
                for testid in testids:
                    try:
                        test_result = TestResult.objects.get(job=job_result,
                                                             test=testid)
                        if test_result.result:
                            success += 1
                        count += 1
                    except TestResult.DoesNotExist:
                        pass
                rfe_result = RFEResult(job=job_result, rfe=rfe,
                                       result=(success != 0 and
                                               testids.count() == success),
                                       percent=(success / count
                                                if (count != 0 and
                                                    testids.count() == count)
                                                else 0)
                                       )
                rfe_result.save()
            product = product.inherit
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def rfe_result_list(request):
    """
    List all rfe results.
    """
    rfes = RFEResult.objects.all()
    serializer = RfeResultSerializer(rfes, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def rfe_result_detail(request, pk):
    """
    Retrieve, update or delete a rfe result.
    """
    try:
        RfeResult = RFEResult.objects.get(pk=pk)
    except RFEResult.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RfeResultSerializer(RfeResult)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RfeResultSerializer(RfeResult, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        RFEResult.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
