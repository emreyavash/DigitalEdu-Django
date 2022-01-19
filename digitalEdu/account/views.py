from django.core.checks import messages
from .models import User
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage,send_mail
from django.core import mail
from django.conf import settings
# Create your views here.

    
# current_site=get_current_site(request)
#  ,{
#         "user":user, 
#         "domain":current_site,
#         "uid":urlsafe_base64_encode(force_bytes(user.id)),
#         "token":generate_token.make_token(user)
#     }
def send_action_email():
    email_subject="Activate Your Account"
    email_body=render_to_string("account/activate.html")

    email=EmailMessage(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL ,
                ["phonewearing@gmail.com"],
                
                )
    
    email.send()


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method=="POST":
        name=request.POST["name"]
        surname=request.POST["surname"]
        email = request.POST["email"]
        username = request.POST["username"]
        birthday= request.POST["birthday"]
        gender = request.POST.get("genderInput")
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        if password == repassword:
            if User.objects.filter(user_name=username).exists():
                context={
                    "error":"Username is used",
                    "username":username,
                    "name":name,
                    "surname":surname,
                    "email":email
                }
                return render(request,"account/register.html",context)
            elif User.objects.filter(email=email).exists():
                context={
                    "error":"Email is used",
                    "username":username,
                    "name":name,
                    "surname":surname,
                    "email":email
                }
                return render(request,"account/register.html",context)
            else:
                user = User.objects.create_user(first_name=name,last_name=surname,email=email,password=password,user_name=username,username=username,gender=gender,birthday=birthday)
                user.save()
                current_site=get_current_site(request)
                send_mail(
                    'Activate Your Account',
                    render_to_string("account/activate.html",{
                        "user":user, 
                        "domain":current_site,
                        "uid":urlsafe_base64_encode(force_bytes(user.id)),
                        "token":generate_token.make_token(user)
                    }),
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )

                


                return redirect("home")
        else:
            context={
                    "error":"Passowrd doesn't match",
                    "username":username,
                    "name":name,
                    "surname":surname,
                    "email":email
                }
            return render(request,"account/register.html",context)
    return render(request,"account/register.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        
        user = authenticate(request,email=email,password=password)
        

        if user is not None:
            if user.is_staff :
                login(request,user)
                return redirect("home")
            else:
                 return render(request,"account/login.html",{
                "error":"Email is not verified,please check your email inbox",
                
            })  
                
        else:
            return render(request,"account/login.html",{
                "error":"Kullanıcı Adı veya Parola Yanlış",
                "user":user
            }) 
        
               
    return render(request,"account/login.html")

def logout_view(request):
    logout(request)
    return redirect("home")

def forgetPasswordEmail_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        user = User.objects.get(email=email)
        if user.email==email:
            current_site=get_current_site(request)
            send_mail(
                'Change Your Password',
                render_to_string("account/forgetPasswordLink.html",{
                    "user":user, 
                    "domain":current_site,
                    "uid":urlsafe_base64_encode(force_bytes(user.id)),
                    "token":generate_token.make_token(user)
                }),
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return redirect("home")
        else:
            return render(request,"account/forgetPasswordEmail.html",{
                "error":"Email is wrong"
            })
    return render(request,"account/forgetPasswordEmail.html")

def forgetPassword_view(request,username):
    if request.method == "POST":
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        if password == repassword:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            return redirect("login")
        else:
            return render(request,"account/forgetPassword.html",{
                "error":"Password doesn't match"
            })
    return render(request,"account/forgetPassword.html")

def forgetPasswordLink(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
        token=generate_token.make_token(user)
    except Exception as e:
        user=None
    if user and generate_token.check_token(user,token):
        username = user.username
        return redirect("forgetPassword",username=username)
    return render(request,"account/forgetPasswordEmail.html")


def activate_user(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
        token=generate_token.make_token(user)
    except Exception as e:
        user=None
    if user and generate_token.check_token(user,token):
        user.is_active=True
        user.is_staff=True
        user.save()

        return redirect("login")
    return render(request,"account/activate_failed.html",{
        "user":user
    })