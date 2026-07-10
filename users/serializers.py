from rest_framework import serializers
from django.contrib.auth import get_user_model

User=get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'password']

    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
           raise serializers.ValidationError("Bu email manzil tizimda allaqachon ro'yxatdan o'tgan!")
        return value
    
    def create(self,validated_data):
        password=validated_data.pop('password')
        user=User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user