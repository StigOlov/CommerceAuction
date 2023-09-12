from datetime import datetime
from .models import Auction_listings, Bid
from celery import shared_task

@shared_task
def check_closing_listing():
    now = datetime.now()
    closing_listings = Auction_listings.objects.filter(closing_date__lt=now)

    for listing in closing_listings:
        bids = Bid.objects.filter(listing_id=listing)

        for bid in bids:
            if bid.status == "Winning":
                bid.status = "Won"
            else:
                bid.status = "Lost"        
            bid.save()
            print("listing closed")

        listing.is_closed = True
        listing.save() 