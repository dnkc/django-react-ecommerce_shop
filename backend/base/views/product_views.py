from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status



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

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user = request.user
    product = Product.objects.create(
        user= user,
        name='Sample Name',
        brand='Sample Brand',
        price=0,
        countInStock=0,
        category='Sample Category',
        description='',
    )
    serializer=ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProduct(request, pk):
    product=Product.objects.get(_id=pk)

    data = request.data
    #product.first_name = data['name']
    product.name = data['name']
    product.price = data['price']
    product.image = data['image']
    product.brand = data['brand']
    product.countInStock=data['countInStock']
    product.description=data['description']


    serializer = ProductSerializer(product, many=False)
    product.save()

    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response('Product was deleted')

@api_view(['POST'])
def uploadImage(request):
    data = request.data
    product_id = data['product_id']
    product = Product.objects.get(_id=product_id)

    product.image = request.FILES.get('image')

    product.save()
    return Response("image was uploaded!")