from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Listing(models.Model):
    CATEGORY = [
        ('MOTORS', "Motors"),
        ('HOME', "Home"),
        ('SPORTINGGOOD', "Sporting Goods"),
        ('TOYSHOBBIES', "Toys & Hobbies"),
        ('HEALTHBEAUTY', "Health & Beauty"),
        ('BUSINESS', "Business"),
        ('ELECTRONICS', "Electronics"),
        ('FASHION', "Fashion"),
        ('COLLECTIBLES', "Collectibles"),
        ('OTHERS', "Others"),
    ]

    DURATION = [
        (1, "One day"),
        (3, "Three days"),
        (5, "Five Days"),
        (7, "Seven Days"),
        (10, "Ten Days"),
    ]

    item_name = models.CharField(max_length=64)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    asking_price = models.DecimalField(max_digits=6, decimal_places=2)
    posting_date = models.DateField(auto_now_add=True)
    posting_time = models.DateTimeField(default=timezone.now())
    description = models.CharField(max_length=64, default="description")
    category = models.CharField(max_length=15, choices=CATEGORY, default='HOME', blank=False)
    duration = models.PositiveSmallIntegerField(choices=DURATION, blank=False, default=1)
    img = models.CharField(max_length=64)
    watching = models.ManyToManyField(User, blank=True, related_name='watchlist')

    # img = models.ImageField(upload_to = "images/")

    def __str__(self):
        return f"ID: {self.id}: {self.posting_date} - {self.item_name} starting at {self.asking_price} "


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bidding_price = models.DecimalField(max_digits=6, decimal_places=2)
    bidding_date = models.DateTimeField(auto_now_add=True)

    # details = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.user} bid {self.bidding_price} on {self.listing} on {self.bidding_date}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default=1)
    # item_name = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_comment")
    comment_post = models.CharField(max_length=128)
    posting_date = models.DateField(auto_now_add=True)
    posting_time = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"Comment: {self.user} said '{self.comment_post}' on {self.listing}"

# Remember to first run python manage.py makemigrations
# then python manage.py migrate
# to migrate those changes to your database
