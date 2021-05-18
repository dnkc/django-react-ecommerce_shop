from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from base.serializer import ProductSerializer

from base.models import Product, Review

@api_view(['GET'])
def getProducts(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    products = Product.objects.filter(
        name__icontains=query).order_by('-createdAt')

    page = request.query_params.get('page')
    paginator = Paginator(products, 5)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    print('Keyword: ', query)
    serializer = ProductSerializer(products, many=True)
    return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})

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

@api_view(['GET'])
def getTopProducts(request):
    product = Product.objects.all().order_by('rating')[:3]
    serializer=ProductSerializer(product, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    data = request.data
    product = Product.objects.get(_id=pk)
    print(request.data)
    #1 - review already exists (do not allow multiple reviews by same user)
    alreadyExists = product.review_set.filter(user=user).exists()
    if alreadyExists:
        content = {'detail': 'Product already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    #2 - customer submits a review with no rating or zero
    elif data and data['rating'] == 0:
        return Response({'detail': 'Please select a rating'}, status=status.HTTP_400_BAD_REQUEST)
               # return Response({'detail':'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST) 
    #3 - create review 
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment']
        )
        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating
        
        product.rating = total / len(reviews)
        product.save()


        return Response('Review added')