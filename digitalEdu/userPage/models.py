from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin,BaseUserManager

from account.models import User

# Create your models here

class UploadFiles(User):
    image = User.userImage
