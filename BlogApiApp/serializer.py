from rest_framework.serializers import ModelSerializer
from .models import(
    Blog,
    Comment
)
from django.contrib.auth.models import (
    User
)


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class BlogSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Blog
        fields = "__all__"