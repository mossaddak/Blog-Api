from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('profile/', views.Profile.as_view()),
]

