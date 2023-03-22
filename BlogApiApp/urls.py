from django.contrib import admin
from .import views
from rest_framework.routers import DefaultRouter
from django.urls import path,include

router = DefaultRouter()
router.register(r"comment", views.Comment , basename="comment")

urlpatterns = [
    path("blog/", views.BlogView.as_view()),
    path("allblog/", views.PublicBlog.as_view()),
    path("allblog/<int:pk>/", views.BlogDetails.as_view()),
]+router.urls
