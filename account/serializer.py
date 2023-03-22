from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.serializers import ModelSerializer
from BlogApiApp.serializer import (
    BlogSerializer,
    CommentSerializer
)

class RegisterSerializer(ModelSerializer):
    blogs = BlogSerializer(many=True, read_only=True)
    mycomments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "blogs",
            "mycomments"
        )

    def validate(self, data):
        request = self.context.get('request')
        current_user_id = request.user.id if request and request.user else None
        if User.objects.filter(username = data['username']).exclude(id=current_user_id).exists():
             raise serializers.ValidationError("user already exist")
        return data
    
    def create(self, validate_data):
        user = User.objects.create(
            username=validate_data["username"].lower(),
            first_name=validate_data["first_name"],
            last_name=validate_data["last_name"],
            password=validate_data["password"],
            
            
        )
        print("End User======================", user)
        #user.set_password(validate_data["password"])
        user.set_password(validate_data["password"])
        user.save()

        return validate_data
    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if not User.objects.filter(username = data['username']).exists():
             raise serializers.ValidationError("Account not found")
        return data
    
    def get_jwt_token(self, data):
        user = authenticate(username=data['username'], password=data['password'])

        if not user:
            return {
                'message':'invalid credentials',
                'data':{}
            }
        
        
        refresh = RefreshToken.for_user(user)
        return { 
                'message':'Login Success',
                'data':{
                    'token':{
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }

                }
            }
    


