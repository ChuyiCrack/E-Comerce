from django.db import models
from django.contrib.auth.models import UserManager,AbstractBaseUser , PermissionsMixin


class CustomUserManager(UserManager):
    def _create_user(self,name ,lastName,password,email,**extra_fields):
        print(name , lastName)
        if not email:
            raise ValueError("You didnt provide an email.")
        
        if not(name and lastName):
            raise ValueError("You didnt put name or lastname.")
        
        email = self.normalize_email(email)
        user = self.model(name = name , lastName = lastName, email = email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self,name,lastName , password,email, **extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(name,lastName,password,email,**extra_fields)
    
    def create_superuser(self,name,lastName , password ,email,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(name,lastName,password,email,**extra_fields)
    

class User(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=30,blank=False)
    lastName = models.CharField(max_length=30,blank=False)
    email = models.EmailField(blank=False , unique=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = ['name' , 'lastName']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    
    def get_full_name(self):
        return self.name + self.lastName
    
    def get_short_name(self):
        return self.name.split(' ')[0]
    
    def __str__(self):
        return self.email
    
    
    