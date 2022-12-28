from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from rest_framework.authtoken.models import Token

from api.models import User
from todo.models import Todo

from .emails import *
from todo.forms import TodoForm, UserProfile, UserRegisterForm

from django.core.mail import send_mail
from django.template.loader import render_to_string

from .tasks import test_func
# Create your views here.


def test(request):
    users = User.objects.all().exclude(username='admin') 
    todos =Todo.objects.all()
    for user in users:
        
        username = user.username
        todo = user.todo_set.all().filter(status=0)
        todo_count = user.todo_set.all().filter(status=0).count()
        html = render_to_string('todo/emails/uncomplete_todo.html',{
        'username':username,
        'todo_count':todo_count,
        'todo':todo
        })
        send_mail(
            'Uncompleted Task',
            f'Hi, {user.username}, you have {todo_count} uncompleted Todo',
            'noreply@tbnotes.com',
            [user.email],
            html_message=html
            )

        
    context = {'users':users, 'todos':todos}
    return render (request, 'todo/test.html', context)





def Index(request):

    #test_func.delay()
    #send_verify_link('udosaint@gmail.com', 'hfjsfjhgsgf8r234628946234234hsgdfhg')

    if request.user.is_authenticated:
        return redirect('todo')

    
    if request.method == "POST":
        message = None

        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            
        except:
            
            messages.warning(request, "Username not found" )

        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_verified:

                login(request,user)
                messages.success(request, "Login Successful" )
                return redirect('todo')
            else:
                messages.success(request, "Please verify your account, check your email for verification link" )
                return render(request, 'todo/index.html')
        else:
            messages.warning(request, "Username or Password not valid" )
            return render(request, 'todo/index.html')
    return render(request, 'todo/index.html')



def Signup(request):
    message = None
    form = UserRegisterForm()
    if request.method == "POST":
        user_name = request.POST.get('username')
        user_email = request.POST.get('email').lower()
        user_password1 = request.POST.get('password')
        user_password2 = request.POST.get('password2')


        if User.objects.filter(username=user_name).exists():
            messages.warning(request, "Username already exist" )

        elif User.objects.filter(email=user_email).exists():
           messages.warning(request, "Email already exist" )

        elif user_password1 != user_password2:
            messages.warning(request, "Password do not match" )
        else:
            user = User(
                email = user_email,
                username = user_name,
            )

            user.set_password(user_password1)
            user.save()

            #create API Token for the user
            token, created = Token.objects.get_or_create(user=user)
            
            send_verify_link(user_email, token)

            messages.success(request, "Registration Successful" )
            return redirect ('register-success')
       
    return render(request, 'todo/register.html', {'form':form})


@login_required(login_url='index')
def Todos(request):
    user = request.user
    todos = user.todo_set.all()

    context = {'todos':todos}
    return render(request, 'todo/todo.html', context)


@login_required(login_url='index')
def AddTodo(request):
    page = "Add"
    form = TodoForm()
    
    if request.method == "POST":
        form = TodoForm(request.POST)

        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, "Todo added successfully" )
            return redirect('todo')

    context = {'page':page, 'form':form}
    return render(request, 'todo/add_edit_todo.html', context)


@login_required(login_url='index')
def EditTodo(request, id):
    page = "Edit"
    todo = Todo.objects.get(id=id)
    form = TodoForm(instance=todo)
    
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)

        if form.is_valid():
            form.save()
            messages.success(request, "Todo updated successfully" )
            return redirect('todo')

    context = {'page':page, 'form':form}
    return render(request, 'todo/add_edit_todo.html', context)


@login_required(login_url='index')
def CompleteTodo(request, id):
   
    if request.method == "GET":
        Todo.objects.filter(id=id ).update(status=1)
        return redirect('todo')

    return render(request, 'todo/add_edit_todo.html')




@login_required(login_url='index')
def DeleteTodo(request, id):
    if request.method == "GET":
        todo = Todo.objects.get(id=id)
        todo.delete()
        messages.success(request, "Todo deleted successfully" )
        return redirect('todo')
    
    context = {}
    return render(request, 'todo/todo.html', context)



@login_required(login_url='index')
def Profile(request):
    user = request.user
    return render(request, 'todo/profile.html', {'user':user})

@login_required(login_url='index')
def UpdateProfile(request):
    form = UserProfile(instance=request.user)
    if request.method == "POST":
        form = UserProfile(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully" )
            return redirect('profile')

    return render(request, 'todo/edit_profile.html', {'form':form})


def RegisterSuccess(request):
    return render(request, 'todo/register_success.html')


def VerifyEmail(request, token):
    if User.objects.filter(auth_token=token).update(is_verified=1):
        messages.success(request, "Email verification successful" )
        return render(request, 'todo/verify_success.html')
    else:
        return redirect('index')
    

def VerifySuccess(request):
    return render(request, 'todo/verify_success.html')


def UserLogout(request):
    logout(request)
    return redirect('index')