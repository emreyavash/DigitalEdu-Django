from django.urls import path
from . import views
urlpatterns = [
    path("profile",views.userProfile_view,name="profile"),
    path("profile/<str:username>",views.userEdit_view,name="profileEdit"),
]
