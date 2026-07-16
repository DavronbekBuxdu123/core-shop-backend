from django.shortcuts import render
from .serializers import UserRegisterSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import User, PasswordResetToken
# Create your views here.

class UserRegisterApiView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        serializer=UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user=serializer.save()
            return Response({
                'message':"Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi!",
                'user':{
                    "id": user.id,
                    "email": user.email,
                    "role": user.role
                }
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "Agar ushbu email tizimda mavjud bo'lsa, parolni tiklash havolasi yuborildi."},
                status=status.HTTP_200_OK
            )
        
        PasswordResetToken.objects.filter(user=user, is_used=False).update(is_used=True)
        reset_token = PasswordResetToken.objects.create(user=user)

        reset_url = f"http://localhost:3000/reset-password?token={reset_token.token}"

        subject = "Parolni tiklash so'rovi"
        message = f"Salom! Parolingizni tiklash uchun quyidagi havolaga o'ting:\n{reset_url}\n\nUshbu havola 10 daqiqa davomida faol bo'ladi."
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False, 
        )
        
        return Response(
            {"message": "Parolni tiklash havolasi pochtangizga muvaffaqiyatli yuborildi!"},
            status=status.HTTP_200_OK
        )


class ResetPasswordView(APIView):
    def post(self, request):
        token_val = request.data.get('token')
        new_password = request.data.get('new_password')
        
        if not token_val or not new_password:
            return Response(
                {"error": "Token va yangi parol yuborilishi shart!"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            reset_token = PasswordResetToken.objects.get(token=token_val)
        except (PasswordResetToken.DoesNotExist, ValueError):
            return Response(
                {"error": "Yaroqsiz yoki xato xavfsizlik kaliti (token)!"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if not reset_token.is_valid():
            return Response(
                {"error": "Ushbu havola muddati tugagan yoki allaqachon ishlatilgan!"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = reset_token.user
        user.set_password(new_password) 
        user.save()
        
        reset_token.is_used = True
        reset_token.save()
        
        return Response(
            {"message": "Parolingiz daxshatli muvaffaqiyatli yangilandi! Yangi parol bilan kirishingiz mumkin."},
            status=status.HTTP_200_OK
        )