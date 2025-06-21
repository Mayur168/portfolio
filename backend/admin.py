from django.contrib import admin
from .models import project
from .models import contact,User
# from .models import user

@admin.register(project)
class projectAdmin (admin.ModelAdmin):
    list_display = ['id',"name","project_description","project_link","project_image"]
    
    
@admin.register(contact)
class ContactAdmin (admin.ModelAdmin):
    list_display = ["id","name","email","suggestion","rating"]


@admin.register(User)
class userAdmin (admin.ModelAdmin):
    list_display = ["email","first_name","last_name"]
    
