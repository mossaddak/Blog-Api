from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Blog(models.Model):
    user = models.ForeignKey(User, related_name='blogs', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=250)
    desc = models.CharField(max_length=250)
    img = models.ImageField(null=True, blank=True)
    reactor = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.pk}.{self.title}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, related_name="mycomments", on_delete=models.CASCADE, null=True, blank=False)
    comment = models.TextField(blank=False, null=True)
    blog = models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return f"{self.pk}.{self.comment}"