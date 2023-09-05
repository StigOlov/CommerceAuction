from django.contrib import admin

from .models import Auction_listings, Bid, Comments, Category, Watchlist

class BidAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'amount', 'timestamp', 'status')
    
# Register your models here.
admin.site.register(Auction_listings)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comments)
admin.site.register(Category)
admin.site.register(Watchlist)
