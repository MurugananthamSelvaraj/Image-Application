from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from .forms import ImageForm
from django.db.models import Q
from .models import Image


def register(request):
    if (request.method == 'POST'):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "User Already Exist")
                return redirect(register)
            else:
                user = User.objects.create_user(
                    username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.set_password(password)
                user.save()
                return redirect('login_user')

    else:
        print("This is not post method")
        return render(request, "register.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            data = Image.objects.all()
            context = {
              'data': data
             }
            return render(request, "display.html", context)

        else:
            messages.info(request, "Invalid Username or Password")
            return redirect('login_user')
    else:
        return render(request, "login.html")


def logout_user(request):
    auth.logout(request)
    return redirect("login_user")


def upload(request):

    data = Image.objects.all()
    context = {
        'data': data
    }

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return render(request, "display.html", context)

    else:
        form = ImageForm()
    return render(request, 'upload.html', {'form': form})


def success(request):
    return HttpResponse('successfully uploaded')


def display(request):
    data = Image.objects.all()
    context = {
        'data': data
    }
    return render(request, "display.html", context)


def SearchImage(request):
    query = request.GET.get('q')
    images = Image.objects.filter(Q(image_file__icontains=query) | Q(title__icontains=query))
    context = {
        'data': images
    }
    return render(request, "display.html", context)
