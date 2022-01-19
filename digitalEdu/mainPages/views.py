from django.shortcuts import redirect, render
from .models import Category, ContactMessage, Course
# Create your views here.
def home_view(request):
    context={
        "courses":Course.objects.all()
    }
    return render(request,"main/index.html",context)

def about_view(request):
    return render(request,"main/about.html")

def contact_view(request):
    if request.method=="POST":
        name=request.POST["name"]
        email=request.POST["email"]
        subject=request.POST["subject"]
        message=request.POST["message"]
        contact=ContactMessage.objects.create(name=name,email=email,subject=subject,message=message)
        contact.save()
        return redirect("contact")

    return render(request,"main/contact.html")

def courses_view(request):
    context={
        "courses":Course.objects.all(),
        "category":Category.objects.all()
    }
    return render(request,"main/services.html",context)
def coursebycategory_view(request,slug):
    context={
        "courses":Category.objects.get(slug=slug).course_set.filter(is_active=True),
        # "courses":Course.objects.filter(is_active=True,categoryId__slug=slug),
        "category":Category.objects.all(),
        "selected_category":slug

    }
    return render(request,"main/services.html",context) 

def courseDetail_view(request,slug):
    context={
        "courses":Course.objects.get(slug=slug)
    }
    return render(request,"main/courseDetail.html",context)
    

