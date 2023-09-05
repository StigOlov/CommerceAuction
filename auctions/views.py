from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, migrations, models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse
from .forms import CreateListingForm
from .models import Auction_listings, Category, Bid, Comments, Watchlist
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from django.utils import timezone
from django.contrib import messages

from .models import User


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
@login_required
def create_listing(request):
    if request.method == 'POST':
        form = CreateListingForm(request.POST, request.FILES)
        if form.is_valid():
            item_name = form.cleaned_data['item_name']
            item_price = form.cleaned_data['item_price']
            starting_bid = form.cleaned_data['starting_bid']
            closing_date = form.cleaned_data['closing_date']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            image = form.cleaned_data['image']

            category = Category.objects.get(name=category)

            new_listing = Auction_listings(
                user_id=request.user,
                item_name=item_name,
                item_price=item_price,
                starting_bid=starting_bid,
                closing_date=closing_date,
                description=description,
                category=category,
                image = image
            )
            new_listing.save()
            
            return redirect('display_listing', listing_id=new_listing.id)
        else:
            print("Form is invalid")
            print(form.errors)  # Print the form validation errors

    else:
        form = CreateListingForm()
    return render(request, 'auctions/create_listing.html', {'form': form})

def display_listing(request, listing_id):
    listing = get_object_or_404(Auction_listings, pk=listing_id)
    comments = Comments.objects.filter(listing_id=listing)
    current_highest_bid = Bid.objects.filter(listing_id=listing).order_by('-amount').first()
    highest_bidder_name = current_highest_bid.user_id.username if current_highest_bid else None
    
    print(highest_bidder_name)

    return render(request, 'auctions/display_listing.html', {
        'listing': listing,
        'comments': comments,
        'highest_bidder_username': highest_bidder_name
    })

def place_comment(request, listing_id):
    listing = get_object_or_404(Auction_listings, pk=listing_id)
    comment_text = request.POST['comment_text']

    comment = Comments(
    listing_id=listing,
    user_id=request.user,
    content=comment_text,
    timestamp=timezone.now()
    )
    comment.save()

    return HttpResponseRedirect(reverse('display_listing', kwargs={'listing_id': listing_id}))

def place_bid(request, listing_id):
    listing = get_object_or_404(Auction_listings, pk=listing_id)
    
    bid_amount = float(request.POST['bid_amount'])
    if bid_amount >= listing.starting_bid and bid_amount > listing.item_price:
        current_highest_bid = Bid.objects.filter(listing_id=listing, status="winning").order_by('-amount').first()

        if current_highest_bid:
            current_highest_bid.status = "losing"
            current_highest_bid.save()

        bid = Bid(
            listing_id=listing,
            user_id=request.user,
            item_name=listing.item_name,
            amount=bid_amount,
            timestamp=timezone.now(),
            status="winning"
        )
        bid.save()
        listing.item_price = bid_amount
        listing.save()
        messages.success(request, 'Your bid has been placed sucessfully')
        return redirect(reverse('display_listing', kwargs={'listing_id': listing_id}))
    else:
        messages.error(request, 'Your bid amount must be greater than the current price and starting bid.')
        return render(request, 'auctions/display_listing.html', {'listing': listing})
    
def my_bids(request):
    user = request.user
    listings_with_bids = Auction_listings.objects.filter(
        bid__user_id=user
    ).distinct()

    listing_data = []  # This will store (listing_id, item_name, status) tuples

    for listing in listings_with_bids:
        current_bid = Bid.objects.filter(listing_id=listing).order_by('-amount').first()
        if current_bid:
            if current_bid.status == "winning":
                status = 'Winning'
            elif current_bid.status == "losing":
                status = 'Losing'
            else:
                status = 'Unknown'
        else: 
            status = 'No Bids'

        listing_data.append((listing.id, listing.item_name, status))
        
        print(listing_data)

    return render(request, 'auctions/my_bids.html', {
        'listing_data': listing_data,
    })

   

def active_listings(request):
    active_listings = Auction_listings.objects.filter(closing_date__gte=timezone.now())
    return render(request, 'auctions/active_listings.html', {
        'active_listings': active_listings
    })


def my_listings(request):
    user = request.user
    listings = Auction_listings.objects.filter(user_id=user)
    return render(request, 'auctions/my_listings.html', {
        'listings': listings})


@login_required
def add_to_watchlist(request, listing_id):
    listing = get_object_or_404(Auction_listings, pk=listing_id)

    # Check if the item is already in the user's watchlist
    if Watchlist.objects.filter(user_id=request.user, listing_id=listing).exists():
        messages.info(request, 'Listing is already in your watchlist.')
    else:
        # Add the item to the watchlist
        watchlist_item = Watchlist(
            user_id=request.user,
            listing_id=listing,
        )
        watchlist_item.save()
        messages.success(request, 'Listing added to your watchlist.')

    # Redirect to the 'display_listing' view with the correct listing_id
    return redirect('display_listing', listing_id=listing.id)

@login_required
def remove_from_watchlist(request, listing_id):
    listing = get_object_or_404(Auction_listings, pk=listing_id)
    user_id = request.user

    watchlist_item = Watchlist.objects.filter(user_id=user_id, listing_id=listing).first()
    if watchlist_item:
        watchlist_item.delete()
    
    return redirect('display_listing', listing_id=listing_id)

@login_required
def display_watchlist(request):
    user_id = request.user
    watchlist_items = Watchlist.objects.filter(user_id=user_id)
    messages.info(request, 'This listing has been removed from your watchlist.')

    return render(request, 'auctions/display_watchlist.html', {
        'watchlist_items': watchlist_items})

