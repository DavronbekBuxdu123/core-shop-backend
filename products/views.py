from django.shortcuts import render
from .models import Category,Product
from .serializers import CategorySerializer,ProductSerializer
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.filter(parent__isnull=True)
    serializer_class=CategorySerializer
    permission_classes=AllowAny

class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all()    
    serializer_class=ProductSerializer
    permission_classes=AllowAny