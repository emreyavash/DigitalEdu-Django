from django.shortcuts import render,redirect
from account.models import User  
from .models import UploadFiles

# Create your views here.,

def userProfile_view(request):
    
    
    if request.user.is_authenticated:
        
        return render(request,"userPage/userProfile.html")

def userEdit_view(request,username):
    user = User.objects.get(username=username)
    if request.method == "POST":
        
    
        user.first_name=request.POST["name"]
        user.last_name=request.POST["surname"]
        user.email=request.POST["email"]
        user.birthday=request.POST["birthday"]
        user.gender=request.POST["genderInput"]
        user.userImage =request.FILES["images"] 
         
        user.save()
       
        return redirect("profile")
   
    return render(request,"userPage/userProfileEdit.html")