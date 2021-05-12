from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from base.products import products

from base.serializer import ProductSerializer

from base.models import Product

@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    # many or single object to serialize required
    # serializer required for every model we want to return
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request, pk):
    product=None
    product = Product.objects.get(_id=pk)
    serializer=ProductSerializer(product, many=False)
    return Response(serializer.data)