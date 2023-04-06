from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework import status, generics
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import IsAuthenticated

from todo.emails import *

from .serializers import AddTodoSerializer, OTPSerializer, RegisterSerializer, TodoSerializer, UpdateUserDetailsSerializer, UserSerializer
from .models import User
from todo.models import Otp, Todo

import random


#The list of all my api route
@permission_classes([])
# Create your views here.
class APIRoutes(APIView):

    def get(self, request):        
        
        todo = Todo.objects.all()[:3]

        serializer = TodoSerializer(todo, many=True)
        routes = {
            "Routes": "This is the list of available route for the TODO APP API",
            "user registration": "/api/auth/register",
            "user login": "/api/auth/login",
            "user create todo": "/api/todo/create",
            "user list all todo": "/api/todo/",
            "user todo by id": "/api/todo/1/",
            "example data": serializer.data,
        }

        return Response(routes, status=status.HTTP_200_OK)

@permission_classes([])
class ReisterView(APIView):

    def post(self, request:Request):
        serializer = RegisterSerializer(data=request.data)
        data = {}
    

        if serializer.is_valid():
            user = serializer.save()
            data = {
                'message': "User register Successfully",
                'user': {
                    "username":user.username,
                    "email":user.email,
                    },
                "token": user.auth_token.key
            }
            
            # sedn welcome mail
            send_welcome_mail(user.email, user.username)

            #send otp
            otp = send_otp(user.email)
            Otp.objects.create(user=user, pin=otp)
            
            return Response(data, status=status.HTTP_201_CREATED)
        
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)



@permission_classes([])
class LoginView(APIView):

    def post(self, request:Request):
        username = request.data.get('username').lower()
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        # print(user)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            userDetails = User.objects.get(username=username)

            
            data = {
                "message": "Login Successfully",
                "token": token.key,
                "userinfo": {
                    "username": userDetails.username,
                    "email": userDetails.email,
                    "avatar": userDetails.avatar.url,
                },
                "is_verified": userDetails.is_verified
            }

            if userDetails.is_verified:
                login(request, user)
                return Response(data, status=status.HTTP_200_OK)
            else:
                otp = send_otp(userDetails.email)
                Otp.objects.create(user=user, pin=otp)
                return Response(data, status=status.HTTP_200_OK)
        else:
            error = {"error": "Invalid email or Password"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class TodosView(APIView):

    # create a new todo
    def post(self, request:Request):

        myuser = Todo(user=request.user)
        serializer = AddTodoSerializer(myuser, data=request.data)

        if serializer.is_valid():
            serializer.save()
            data = {
                'message': "Todo Added Successfully",
                'todo': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    # get all todo for a particular user
    def get(self, request:Request):

        user = request.user
        
        try:
            user_todo = user.todo_set.all()
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TodoSerializer(user_todo, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class TodoView(APIView):

    #get todo by the id
    def get(self, request:Request, id):
        todo = Todo.objects.get(pk=id)

        serializer = TodoSerializer(instance=todo)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request:Request, id):

        todo = Todo.objects.get(pk=id)

        if todo is not None:

            serializer = TodoSerializer(instance=todo, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data={"message": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.error, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request:Request, id):

        todo = Todo.objects.get(pk=id)
        todo.delete()
        return Response(data={"message": "Todo Deleted Successfully"},status=status.HTTP_200_OK)


    def patch(self, request:Request, id):

        todo = Todo.objects.get(pk=id)
        serializer = TodoSerializer(instance=todo, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class ProfileView(APIView):
    #get the profile of the user
    def get(self, request:Request):

        profile = User.objects.get(username=request.user)


        serializer = UserSerializer(instance=profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Update the user details excluding the Profile Picture
    def put(self, request:Request):

        profile = User.objects.get(username=request.user)
        
        if profile is not None:

            serializer = UpdateUserDetailsSerializer(instance=profile, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data={"message": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    
@permission_classes([IsAuthenticated])
class ChangePasswordView(APIView):
    #change the user password
    def post(self, request:Request):

        user = request.user
        password = request.data['password']

        try:
            user = User.objects.get(username=user)
            user.set_password(password)
            user.save()
            password_success(user.email, user.username)
            data = {
                "res":True, 
                "message":"Password reset successful"
                }
            return Response(data,status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error":"The user does not exist"},status=status.HTTP_404_NOT_FOUND)

    # Get the list of completed task by the user
@permission_classes([IsAuthenticated])
class CompletedTaskView(APIView):
    def get(self, request:Request, complete):

        user = request.user
        
        try:
            user_todo = user.todo_set.all().filter(status=1)
        except Todo.DoesNotExist:
            return Response({"error":"No completed task yet"},status=status.HTTP_404_NOT_FOUND)

        serializer = TodoSerializer(user_todo, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@permission_classes([])
class VerifyEmailView(APIView):

    # verify the confirm the otp and then verify the user
    def post(self, request:Request):

        pin = request.data['pin']
        try:
            getPin = Otp.objects.get(pin=pin)
            user = getPin.user
            User.objects.filter(username=user).update(is_verified=1)
            userd = User.objects.get(username=user)
            account_success(userd.email, userd.username)
            data = {"res":True, "message":"Account Verification Successfull"}
            return Response(data,status=status.HTTP_200_OK)
        except Otp.DoesNotExist:
            return Response({"error":"The Pin is incorrect"},status=status.HTTP_404_NOT_FOUND)

        # serializer = TodoSerializer(user_todo, many=True)
        return Response(status=status.HTTP_200_OK)  

    # resend the verification PIN to the user eamil
    def get(self, request:Request, id):
        user = User.objects.get(username=id)
        otp = send_otp(user.email)
        Otp.objects.create(user=user, pin=otp)
        data = {
            "user": user.username,
            "Otp": otp
        }
        return Response(data, status=status.HTTP_201_CREATED)
    
@permission_classes([])
class PasswordForgetView(APIView):
    #user enter there email to get OTP to reset there password
    # since am returning the email and otp the confirmation will be done on server side 
    def get(self, request:Request, email):

        try:
            user = User.objects.get(email=email)
            otp = forgot_password_otp(email)
            Otp.objects.create(user=user, pin=otp)
            data = {
                "res":True, 
                "email": email,
                "Otp": otp
                }
            return Response(data,status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error":"Email not found"},status=status.HTTP_404_NOT_FOUND)
    
    # get the user email, and the new password and change the user password
    def post(self, request:Request):

        email = request.data['email']
        password = request.data['password']
        if email != "" and password != "":
            try:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                forgot_password_success(email, user.username)
                data = {
                    "res":True, 
                    "message":"Password reset successful"
                    }
                return Response(data,status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error":"The email does not exist"},status=status.HTTP_404_NOT_FOUND)
        return Response({"error":"There is an empty field"},status=status.HTTP_404_NOT_FOUND)
