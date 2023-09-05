from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("display_listing/<int:listing_id>", views.display_listing, name="display_listing"),
    path("my_listing", views.my_listings, name="my_listings"),
    path("active_listings", views.active_listings, name="active_listings"),
    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("place_comment/<int:listing_id>", views.place_comment, name="place_comment"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("display_watchlist", views.display_watchlist, name="display_watchlist"),
    path("my_bids", views.my_bids, name="my_bids")
    
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

