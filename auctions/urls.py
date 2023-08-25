from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("display_listing/<int:listing_id>", views.display_listing, name="display_listing"),
    path("my_listing", views.my_listings, name="my_listings"),
    ]

