from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from cicovapp.models import Product, RFE, TestId, JobResult, TestResult
from cicovapp.serializers import (ProductSerializer, RFESerializer,
                                  TestIdSerializer, JobResultSerializer,
                                  TestResultSerializer)


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
