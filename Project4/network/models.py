from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    user_post = models.CharField(max_length=128)
    # post_pic = models.CharField(max_length=128) #Link for img?
    posting_date = models.DateField(auto_now_add=True)
    posting_time = models.DateTimeField(default=timezone.now())
    num_likes = models.CharField(max_length=5)
    num_followers = models.CharField(max_length=5)

    def __str__(self):
        return f"ID: {self.id} - {self.posting_date} {self.posting_time} - {self.user} posted " \
               f"{self.user_post}"


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    username = models.CharField(max_length=64)
    prof_posts = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"ID: {self.id} {self.user} "


class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    post_comment = models.CharField(max_length=128)

    def __str__(self):
        return f"ID: {self.id} {self.username} {self.post_id} - {self.post_comment}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"ID: {self.id} {self.username} liked {self.post_id}"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"ID: {self.id} {self.username} followed {self.followed_user}"


# Remember to first run python manage.py makemigrations
# then python manage.py migrate
# to migrate those changes to your database

