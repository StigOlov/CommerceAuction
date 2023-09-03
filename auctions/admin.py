from django.contrib import admin

from .models import Auction_listings, Bid, Comments, Category, Watchlist

# Register your models here.
admin.site.register(Auction_listings)
admin.site.register(Bid)
admin.site.register(Comments)
admin.site.register(Category)
admin.site.register(Watchlist)


