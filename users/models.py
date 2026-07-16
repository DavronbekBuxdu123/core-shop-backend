from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
import uuid
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('Email kiritilishi shart!')
        
        email=self.normalize_email(email)

        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
   
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('role','superadmin')

        return self.create_user(email,password,**extra_fields)

class User(AbstractBaseUser,PermissionsMixin): 
    class Role(models.TextChoices):
        SUPERADMIN='superadmin','Superadmin'
        ADMIN='admin','Admin',
        SELLER='seller','Seller',
        CUSTOMER='customer','Customer',

    email=models.EmailField(unique=True,max_length=255)
    first_name=models.CharField(max_length=255,blank=True,null=True)
    phone_number=models.CharField(max_length=255,blank=True,null=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    date_joined=models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    objects=UserManager()

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_tokens')
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        expiration_time = self.created_at + timedelta(minutes=10)
        return timezone.now() <= expiration_time and not self.is_used

    def __str__(self):
        return f"Reset token for {self.user.email}"