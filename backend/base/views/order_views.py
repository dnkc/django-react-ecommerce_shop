from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from base.serializer import ProductSerializer, OrderSerializer

from base.models import Product, Order, OrderItem, ShippingAddress


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data
    
    #   orderItems sent from front end
    orderItems = data['orderItems']

    #check if orderItems exist
    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No order items found.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # create order
        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )
        # create shipping address
        shipping = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country']

        )
        # create order items (add them to the database)
        for i in orderItems:
            product = Product.objects.get(_id=i['product'])
        # set orderItem relationship
            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i['qty'],
                price=i['price'],
                image=product.image.url,
            )
            
            # update stock
            product.countInStock -= item.qty
            product.save()


        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)