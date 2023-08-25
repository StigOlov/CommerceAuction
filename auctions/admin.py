from django.contrib import admin

from .models import Auction_listings, Bid, Comments

# Register your models here.
admin.site.register(Auction_listings)
admin.site.register(Bid)
admin.site.register(Comments)


