from rest_framework import serializers
from .models import project,contact, User

class projectSerializers (serializers.ModelSerializer):
    class Meta:
        model = project
        fields = ['id',"name","project_description","project_link","project_image"]
        
        
class contactSerializers (serializers.ModelSerializer):
    class Meta:
        model = contact
        fields = ["id","name","email","suggestion","rating"]
        
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'password',
            'is_staff', 'is_superuser', 'is_active', 'mobile'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
