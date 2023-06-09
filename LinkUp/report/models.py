from django.db import models
from post.models import Post
from users.models import user

# Create your models here.

class Report(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    reporting_user = models.ForeignKey(user,on_delete=models.CASCADE,related_name="reprting_user")
    reported_user = models.ForeignKey(user,on_delete=models.CASCADE,related_name="reported_user")
    reason = models.TextField()
    resolved = models.BooleanField(default=False)