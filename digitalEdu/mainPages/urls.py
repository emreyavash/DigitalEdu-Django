from django.urls import path
from . import views
urlpatterns = [
    path("",views.home_view,name="home"),
    path("home",views.home_view),
    path("about",views.about_view,name="about"),
    path("contact",views.contact_view,name="contact"),
    path("courses",views.courses_view,name="courses"),
    path("category/<slug:slug>",views.coursebycategory_view,name="course_by_category"),
    path("course/<slug:slug>",views.courseDetail_view,name="courseDetail"),
    
]
