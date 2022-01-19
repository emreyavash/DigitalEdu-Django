from django.urls import path
from . import views
urlpatterns = [
    path("login",views.login_view,name="login"),
    path("register",views.register_view,name="register"),
    path("logout",views.logout_view,name="logout"),
    path("activate-user/<uidb64>/<token>",views.activate_user,name="activate"),
    path("forget-password-email",views.forgetPasswordEmail_view,name="forgetPasswordEmail"),
    path("forget-password/<username>",views.forgetPassword_view,name="forgetPassword"),
    path("forget-password/<uidb64>/<token>",views.forgetPasswordLink,name="forgetPasswordLink"),
]
