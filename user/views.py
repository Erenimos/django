from django.shortcuts import render,HttpResponse,redirect
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout

# Create your views here.

def loginUser(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username,password=password)
        if user is None:
            messages.warning(request,"Kullanıcı Adı veya Parola Yanlış!!")
        else:
            login(request,user)
            messages.success(request,"Giriş Yapıldı..")
            return redirect("index")

    context = {
        "form":form
    }

    return render(request,"login.html",context)


def register(request):
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            newUser = User(username= username)
            newUser.set_password(password)
            newUser.save()
            login(request,newUser)
            messages.success(request,"Başarıyla Kayıt Oldunuz..")
            return redirect("index")

        form = RegisterForm()
        context = {
            "form" : form
        }
        return render(request,"register.html",context)
    
def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla Çıkış Yapıldı..")
    return render(request,"index.html")