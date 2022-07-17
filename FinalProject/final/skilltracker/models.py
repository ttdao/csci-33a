from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE, unique=True, default=1)
    follower = models.ManyToManyField(User, blank=True, related_name="follower")
    following = models.ManyToManyField(User, blank=True, related_name="following")

    def __str__(self):
        return f"Profile: {self.user}"


class Tag(models.Model):
    # post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="tag_post")
    name = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return f"{self.name}"


class Post(models.Model):
    user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE, related_name='user_of_post')
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=255)
    tag = models.ManyToManyField(Tag, related_name="related_posts")
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')

    def __str__(self):
        return f"User: {self.id} posts {self.content} on {self.date} with a number of likes"

    @property
    def total_likes(self):
        return self.likes.count()

    # def is_liked(self, request):
    #     return self.likes.filter(id=request.user.id).exists()

    def is_liked(self, request):
        return self.likes.filter(id=request).exists()

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "tag": self.tag,
            "date": self.date,
            "likes": self.likes.count(),
        }


class Comment(models.Model):
    user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments_post")
    comment = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user} posted the comment {self.comment} on the post {self.post.id} on {self.date}"


# Remember to first run python3 manage.py makemigrations
# then python manage.py migrate
# to migrate those changes to your database
