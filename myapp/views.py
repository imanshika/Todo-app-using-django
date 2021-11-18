from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime
from myapp.models import todo
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def index(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('loginUser')
    todoList = todo.objects.filter(user=user)
    if(not todoList):
        messages.info(request, "No Todos to display!! You can add todo if you want")
    return render(request, 'index.html', {"todoList": todoList})


def search(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('loginUser')
    todoList = todo.objects.filter(user=user)
    if(not todoList):
        messages.info(request, "No Todos to search!! You can add todo if you want")
    else:
        todoList = todoList.filter(title__icontains=request.POST.get('title'))
        if(not todoList):
            messages.info(request, "No matching todo found")
    return render(request, 'index.html', {"todoList": todoList})


def doneTodo(request, id):
    if not request.user.is_authenticated:
        return redirect('loginUser')
    todoItem = todo.objects.filter(id=id).first()
    if todoItem.isDone:
        todoItem.isDone = False
        todoItem.doneDate = None
        todoItem.updateDone = datetime.today()
        messages.success(request, 'Your todo is marked as pending')
    else:
        todoItem.isDone = True
        todoItem.doneDate = datetime.today()
        messages.success(request, 'Congrats, You have completed the task!!')
    todoItem.save()
    return redirect("/")


def deleteTodo(request, id):
    if not request.user.is_authenticated:
        return redirect('loginUser')
    print(request.path)
    todo.objects.filter(id=id).delete()
    messages.success(request, 'Todo deleted successfully')
    return redirect('/')


def editTodo(request, id):
    if not request.user.is_authenticated:
        return redirect('loginUser')
    todoItem = todo.objects.filter(id=id).first()
    if request.method == "POST":
        todoItem.title = request.POST.get('title')
        todoItem.descr = request.POST.get('descr')
        todoItem.updateDate = datetime.today()
        todoItem.save()
        messages.success(request, 'Todo Edit successfully')
    return render(request, 'editTodo.html', {"todo": todoItem})


def addTodo(request):
    user = request.user
    if request.method == "POST":
        if not user.is_authenticated:
            messages.warning(request, 'Please login/sign up to add todos')
        else:
            title = request.POST.get('title')
            descr = request.POST.get('descr')
            addtodo = todo(user = user, title = title, descr = descr, updateDate = datetime.today())
            addtodo.save()
            messages.success(request, 'Your todo has been added successfully')
    return render(request, 'addTodo.html')

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Incorrect username or password')
    return render(request, 'login.html')

def logoutUser(request):
    if not request.user.is_authenticated:
        redirect('loginUser')
    logout(request)
    messages.success(request, 'Logout successfully')
    return redirect('loginUser')

def signUp(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if len(username) > 20 or not username.isalnum():
            messages.error(request, 'Username cannot be more than 20 characters and it can include letters, digits and unserscore only')
            return redirect('signUp')
        if len(password1) < 8 or password1.isnumeric():
            messages.error(request, 'Password must contain atleast 8 characters and all digits cannot be numeric')
            return redirect('signUp')
        if password1 != password2:
            messages.error(request, 'Passwords does not match')
            return redirect('signUp')
        try:
            user= User.objects.get(username=username)
            messages.info(request, 'This username is already exists. Please try another one')
            return redirect('signUp')
        except User.DoesNotExist:
            user = User.objects.create_user(username, password = password1)
            user.first_name = request.POST.get('firstName').capitalize()
            user.last_name = request.POST.get('lastName').capitalize()
            user.save()
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('loginUser')
    return render(request, 'SignUp.html')

def deleteAccount(request):
    if request.user.is_authenticated:
        u = User.objects.get(username = request.user.get_username())
        u.delete()
        messages.success(request, "Your account deleted successfully")
    return redirect('loginUser')


def changePassword(request):
    if not request.user.is_authenticated:
        return redirect('loginUser')
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(old_password, password1, password2)
        if authenticate(username=request.user.get_username(), password=old_password) is None:
            messages.error(request, 'You have entered incorrect current password')
        elif len(password1) < 8 or password1.isnumeric():
            messages.error(request, 'Password must contain atleast 8 characters and all digits cannot be numeric')
        elif password1 != password2:
            messages.error(request, 'Passwords does not match')
        elif password1 == old_password:
            messages.info(request, 'Passwords must not match with your old password')
        else:
            u = User.objects.get(username=request.user.get_username())
            u.set_password(password1)
            u.save()
            messages.success(request, 'Password change successfully')
            login(request, u)
            return redirect('/')
    return render(request, 'changePassword.html')