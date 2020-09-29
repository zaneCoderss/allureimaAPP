"""allureimaAPP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signupuser, name = "signupuser"),
    path('login/', views.loginuser, name = "loginuser"),

    path('logout/', views.logoutuser, name = "logoutuser"),


    # User Home Page i.e. page they land on right after signing up
    path('', views.home, name = "home"),
    path('addTodo', views.addTodo, name = "addTodo"),
    path('uhome/', views.userhome, name = "userhome"),
    path('todo/<int:todo_pk>', views.viewtodo, name = "viewtodo"),
    path('todo/<int:todo_pk>/complete', views.completetodo, name = "completetodo"),
    path('todo/<int:todo_pk>/delete', views.deletetodo, name = "deletetodo"),
    path('completedtodos/', views.completedtodos, name = "completedtodos"),
    path('sofie/', views.sofie, name = "sofie"),
    path('stock/', views.stockhome, name = "stockhome"),
    path('stock/stocksumm/', views.stocksumm, name = "stocksumm"),
    path('stock/stocksummtab/', views.stocksummtab, name = "stocksummtab"),







]
