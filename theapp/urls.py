from .views import *
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin



urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('index-search/', index_search, name='index-search'),
    path('search/', search, name='search'),
    path('user-profile/', user_profile, name='user-profile'),
    path('user-listings/', user_listings, name='user-listings'),
    # blog
    path('search/', search, name='search'),
    path('blog/', posts, name='post-list'),
    path('post/<str:pk>/', post_detail, name='post-detail'),
    path('listing/<pk>/', listing_detail, name='listing-detail'),
    path('listings', listings, name='listings'),
    path('contact/', contact, name='contact'),
    path('all-listings/', all_listings, name='all-listings'),
    # new listing
    path('prices/', prices, name='prices'),
    path('submit-listing/', submit_listing, name='submit-listing'),
    # website categories/locations
    path('category/<str:cats>/', category_detail, name='category-detail'),
    path('post-category/<str:cats>/', post_category_detail, name='post-category-detail'),
    path('location/<str:cats>/', location_detail, name='location-detail'),
    path('location-search/', location_search, name='location-search'),
    # marketing
    path('email-signup/', email_list_signup, name='email-list-signup'),
    # login
    path("signin/", signin, name="signin"),
    path("signout/", signout, name="signout"),
    # user listing
    path('update-listing/<int:pk>/', UpdateListingView.as_view(), name="update-listing"),
]
