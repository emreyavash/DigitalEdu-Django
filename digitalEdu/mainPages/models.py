from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.text import slugify
from ckeditor.fields import RichTextField

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50)
    slug=models.SlugField(null=False,blank=True,unique=True,db_index=True,editable=False)
    def __str__(self) :
        return f"{self.name}"
    def save(self,*args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Course(models.Model):
    courseName = models.CharField(max_length=50)
    image = models.ImageField(upload_to="course")
    description = RichTextField()
    courseNumber=models.CharField(max_length=50)
    lessonNumber=models.CharField(max_length=50)
    coursePrice=models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    is_home = models.BooleanField(default=False)
    slug = models.SlugField(null=False,blank=True,unique=True,db_index=True,editable=False)
    categoryId=models.ManyToManyField(Category,blank=True)

    def __str__(self) :
        return f"{self.courseName}"
    def save(self,*args, **kwargs):
        self.slug = slugify(self.courseName)
        super().save(*args, **kwargs)

class Instructor(models.Model):
    name=models.CharField(max_length=50)
    surname=models.CharField(max_length=50)
    image = models.CharField(max_length=50)

    def __str__(self) :
        return f"{self.name} {self.surname}"



class UserInfo(models.Model):
    name=models.CharField(max_length=50)
    surname=models.CharField(max_length=50)
    
class ContactMessage(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    subject=models.CharField(max_length=100)
    message=models.TextField(max_length=500)

    def __str__(self):
        return f"{self.name} - {self.subject}"

