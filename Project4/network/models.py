from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    user_post = models.CharField(max_length=128)  # but TextArea
    posting_date = models.DateField(auto_now_add=True)
    posting_time = models.DateTimeField(default=timezone.now())
    num_likes = models.CharField(max_length=5)

    def __str__(self):
        return f"ID: {self.id} - {self.posting_date} {self.posting_time} - {self.username} posted " \
               f"{self.user_post}"


class Profile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    num_followers = models.CharField(max_length=5)
    prof_posts = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"ID: {self.id} has {self.num_followers} followers "

class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    post_comment = models.CharField(max_length=128)


# Remember to first run python manage.py makemigrations
# then python manage.py migrate
# to migrate those changes to your database

