from django.db import models
from users.models import user
from cloudinary.models import CloudinaryField


class Post(models.Model):
    MEDIA_CHOICES = (
        ('Image', 'Image'),
        ('Video', 'Video'),
    )

    post_id = models.AutoField(primary_key=True)
    likes = models.ManyToManyField(
        user, related_name='liked_posts', blank=True)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    caption = models.TextField(blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES)
    media_url = CloudinaryField(resource_type='auto')
    created_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
