from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, OrderSerializer

from .models import Product, Order

@api_view(['GET'])
def product_list(request):
    products= Product.objects.all()
    serializer= ProductSerializer(products, many= True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def product_detail(request, pk):
    product= Product.objects.get(pk= pk)
    serializer= ProductSerializer(product)
    return Response(serializer.data, status=201)

@api_view(['GET'])
def orders_list(request):
    orders= Order.objects.all()
    serializer= OrderSerializer(orders, many= True)
    return Response(serializer.data, status=200)