from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token

from .models import User
from todo.models import Todo


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):

        username_exist = User.objects.filter(username=attrs['username']).exists()
        if username_exist:
            raise ValidationError({"error": "Username already exist"})

        email_exist = User.objects.filter(email=attrs['email']).exists()
        if email_exist:
            raise ValidationError({"error": "Email already exist"})
        return super().validate(attrs)

    def save(self):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise ValidationError({'password':'Password do not match'})

        user.set_password(password)
        user.save()

        #create API Token for the user
        Token.objects.create(user=user)
        return user

class AddTodoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Todo
        fields = ['name', 'description']


class TodoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Todo
        fields = ['id','name', 'description', 'status', 'created']

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'email','fullname', 'address', 'phone', 'avatar']


class UpdateUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['fullname', 'address', 'phone', 'avatar']