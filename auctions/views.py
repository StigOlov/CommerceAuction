from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, migrations, models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import CreateListingForm
from .models import Auction_listings, Category
from django.contrib.auth.decorators import login_required

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
    
def create_listing(request):
    if request.method == 'POST':
        form = CreateListingForm(request.POST)
        if form.is_valid():
            item_name = form.cleaned_data['item_name']
            item_price = form.cleaned_data['item_price']
            starting_bid = form.cleaned_data['starting_bid']
            closing_date = form.cleaned_data['closing_date']
            description = form.cleaned_data['description']
            category_choice = form.cleaned_data['category']

            category_choice = Category.objects.get(name=category_choice)
        

            new_listing = Auction_listings(
                user_id=request.user,
                item_name=item_name,
                item_price=item_price,
                starting_bid=starting_bid,
                closing_date=closing_date,
                description=description,
                category=category_choice
            )
            new_listing.save()
            
            return redirect('display_listing', listing_id=new_listing.id)
    else:
        form = CreateListingForm()
    return render(request, 'auctions/create_listing.html', {'form': form})

def display_listing(request, listing_id):
    listing = get_object_or_404(Auction_listings, pk=listing_id)
    return render(request, 'auctions/display_listing.html', {
        'listing': listing
    })

def my_listings(request):
    user = request.user
    listings = Auction_listings.objects.filter(user_id=user)
    return render(request, 'auctions/my_listings.html', {
        'listings': listings})


