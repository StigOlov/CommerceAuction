from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    FURNITURE = 'Furniture'
    TOYS = 'Toys'
    CLOTHES = 'Clothes'
    SPORTS = 'Sports'
    TECHNOLOGY = 'Technology'
    KITCHEN = 'Kitchen'
    OTHER = 'Other'

    CATEGORY_CHOICES = [
        (FURNITURE, 'Furniture'),
        (TOYS, 'Toys'),
        (CLOTHES, 'Clothes'),
        (SPORTS, 'Sports'),
        (TECHNOLOGY, 'Technology'),
        (KITCHEN, 'Kitchen'),
        (OTHER, 'Other'),
        # Add more categories as needed
    ]

    name = models.CharField(max_length=50)

class Auction_listings(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=500)
    closing_date = models.DateTimeField()

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

class Comments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Auction_listings, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    timestamp = models.DateTimeField()




    


