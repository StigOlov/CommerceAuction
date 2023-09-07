from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import admin


class User(AbstractUser):
    pass

class Category(models.Model):
    Furniture = 'Furniture'
    Toys = 'Toys'
    Clothes = 'Clothes'
    Sports = 'Sports'
    Technology = 'Technology'
    Kitchen = 'Kitchen'
    Other = 'Other'

    CATEGORY_CHOICES = [
        (Furniture, 'Furniture'),
        (Toys, 'Toys'),
        (Clothes, 'Clothes'),
        (Sports, 'Sports'),
        (Technology, 'Technology'),
        (Kitchen, 'Kitchen'),
        (Other, 'Other'),
    ]

    def __str__(self):
        return self.name

    name = models.CharField(max_length=50)

class Auction_listings(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=500)
    closing_date = models.DateTimeField()
    image = models.ImageField(upload_to='auction_images/', null=True, blank=True)

    def __str__(self):
        return self.item_name

class Bid(models.Model):
    listing_id = models.ForeignKey(Auction_listings, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField()
    BID_STATUS_CHOICES = [
        ('win', 'Won'),
        ('lost', 'Lost'),
        ('winning', 'Winning'),
        ('losing', 'Losing'),
    ]
    status = models.CharField(max_length=10, choices=BID_STATUS_CHOICES)

    def __str__(self):
        return self.item_name
    
class Comments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Auction_listings, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    timestamp = models.DateTimeField()

class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Auction_listings, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Watchlist entry for User: {self.user_id.username}, Listing: {self.listing_id.item_name}'




    


