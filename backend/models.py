from django.db import models
# from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager



class project (models.Model):
    name = models.CharField  (max_length=50)
    project_description = models.TextField()
    project_link = models.URLField(max_length=200, blank=True, null=True)
    project_image = models.ImageField(upload_to='project_images/', blank=True, null=True)

    
    def __str__(self):
        return self.name
    

class contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField() 
    suggestion = models.TextField(blank=True, null=True)
    
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)

    def __str__(self):
        return f"{self.name} - {self.rating}/5"
    
    
    
class User(AbstractBaseUser, PermissionsMixin):
    """User"""
    first_name = models.CharField(
        max_length=255, verbose_name="First Name", blank=True, null=True
    )
    last_name = models.CharField(
        max_length=255, verbose_name="Last Name", blank=True, null=True
    )
    email = models.EmailField(
        unique=True, verbose_name="Email"
    )
    
    is_staff = models.BooleanField(
        default=False, verbose_name="Staff"
    )
    is_superuser = models.BooleanField(
        default=False, verbose_name="Admin"
    )
    is_active = models.BooleanField(
        default=True, verbose_name="Active"
    )
    mobile = models.CharField(
        max_length=255, verbose_name="Mobile Number",
        null=True, blank=True, db_index=True
    )
   
    # user_role = models.ForeignKey(
    #     "Roles", verbose_name="Roles", on_delete=models.CASCADE, null=True
    #     )
    # user_role = models.ManyToManyField(
    #     "Roles", verbose_name="Roles"
    # )
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name="Created Date"
    )
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="Updated Date"
    )
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        """Meta Arguments"""
        db_table = 'users'

    def __str__(self):
        return str(self.email)



    
    
    
    
