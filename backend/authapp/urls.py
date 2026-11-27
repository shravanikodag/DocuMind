from django.urls import path
from . import views
urlpatterns = [
    path("csrf/",views.csrf_view,name="csrf"),
    path("register/",views.register_view,name="register"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.login_view,name="logout"),
    path("me/",views.current_user,name="current_user")
]