import hashlib
from django.shortcuts import render,redirect
from . import models
from . import forms
from .forms import UserForm,RegisterForm

# Create your views here.

def hash_code(s, hk='lxf'):
    h = hashlib.sha256()
    s += hk
    h.update(s.encode())
    return h.hexdigest()

def login(request):
    if request.session.get('is_login') == True:
        return redirect('/index/')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "please check in the content！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.LoginUser.objects.get(username=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.username
                    return redirect('/index/')
                else:
                    message = "uncorrect passwd！"
            except:
                message = "uncorrect user！"
        return render(request, 'login/login.html', locals())
    login_form = UserForm()
    return render(request,'login/login.html', locals())

def register(request):
    if request.session.get('is_login') == True:
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "please check in the content！"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:
                message = "Enter the password twice is different!"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.LoginUser.objects.filter(username=username)
                if same_name_user:
                    message = "User already exists, please re-select username"
                    return render(request, 'login/register.html', locals())
                same_email_user = models.LoginUser.objects.filter(email=email)
                if same_email_user: 
                    message = "The email address has been registered, please use another email address"
                    return render(request, 'login/register.html', locals())
                new_user = models.LoginUser()
                new_user.username = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.save()
                return redirect('/login/')
    register_form = RegisterForm()
    return render(request,'login/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    request.session.flush()
    return redirect('/index/')

def HomePage(request):
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    user = request.session['user_name']
    user_model = models.LoginUser.objects.get(username=user)
    form = forms.HomeForm()
    user_form = forms.HomeForm(instance=user_model)
    return render(request, 'login/homepage.html', locals())

def ModUser(request):
    if request.session.get('is_login') == None:
        return render(request, 'LoginWarning.html', locals())
    user = request.session['user_name']
    user_model = models.LoginUser.objects.get(username=user)
    if request.method == "POST":
        change_form = forms.ChangePassForm(request.POST, instance=user_model)
        message = "please check in the content!"
        if change_form.is_valid():
            old_password = change_form.cleaned_data['password']
            new_password1 = change_form.cleaned_data['new_password1']
            new_password2 = change_form.cleaned_data['new_password2']
            if user_model.password == old_password:
                if new_password1 == new_password2:
                    user_model.password = hash_code(new_password1)
                    user_model.save()
                    return render(request, 'login/homepage.html', locals())
                else:
                    message = '两次输入密码不一致'
                    return render(request, 'login/moduser.html', locals())
            else:
                message = '原密码不对'
                return render(request, 'login/moduser.html', locals())
    else:
        change_form = forms.ChangePassForm(request.POST, instance=user_model)
    return render(request, 'login/moduser.html', locals())

def WebHome(request):
    return render(request,'login/webhome.html', locals())
