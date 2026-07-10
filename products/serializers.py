from rest_framework import serializers
from .models import Category,Product


class CategorySerializer(serializers.ModelSerializer):
    children=serializers.SerializerMethodField()

    class Meta:
            model=Category
            fields=['id','name','slug','parent','children','created_at']
    
    def get_children(self,obj):
          if obj.children.exists():
                return CategorySerializer(obj.children.all(),many=True).data
          return []
          
class ProductSerializer(serializers.ModelSerializer):
    category_details=CategorySerializer(source='category',read_only=True)
    class Meta:
          model=Product
          fields = [
            'id', 'category', 'category_details', 'name', 'slug', 
            'description', 'price', 'stock', 'low_stock', 
            'is_available', 'created_at', 'updated_at'
        ]
    read_only_fields=['slug','is_available']
