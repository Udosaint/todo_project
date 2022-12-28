from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework import status, generics
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import AddTodoSerializer, RegisterSerializer, TodoSerializer, UserSerializer
from .models import User
from todo.models import Todo



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
                    "email":user.email
                    },
                "token": user.auth_token.key
            }
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

        print(user)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            data = {
                "message": "Login Successfully",
                "token": token.key
            }

            login(request, user)
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {"error": "Invalid email or Password"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


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
        return Response(data={"message": "Todo Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)


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

    def get(self, request:Request):

        profile = User.objects.get(pk=request.user.id)

        serializer = UserSerializer(instance=profile)
        return Response(serializer.data, status=status.HTTP_200_OK)