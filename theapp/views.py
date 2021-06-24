from django.shortcuts import render, redirect
from django.views import generic
from .models import *
from .forms import *
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
import requests
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import json



class UserSignupView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')



class UpdateListingView(UpdateView):
    model = BusinessListing
    template_name = 'user/user_listing_edit.html'
    fields = '__all__'



def terms(request):
    return render(request, 'compliance/terms_of_service.html', {})



def privacy(request):
    return render(request, 'compliance/privacy_policy.html', {})



def spam(request):
    return render(request, 'compliance/anti_spam.html', {})



@login_required
def user_profile(request):
    nav_categories = BusinessCategory.objects.all()
    nav_locations = BusinessLocation.objects.all()

    context = {
        'nav_locations':nav_locations,
        'nav_categories':nav_categories,
    }

    return render(request, 'user/profile.html', context)



@login_required
def user_billing(request):
    nav_categories = BusinessCategory.objects.all()
    nav_locations = BusinessLocation.objects.all()

    context = {
        'nav_locations':nav_locations,
        'nav_categories':nav_categories,
    }

    return render(request, 'user/billing.html', context)



@login_required
def user_reports(request):
    nav_categories = BusinessCategory.objects.all()
    nav_locations = BusinessLocation.objects.all()

    context = {
        'nav_locations':nav_locations,
        'nav_categories':nav_categories,
    }

    return render(request, 'user/reports.html', context)



@login_required
def user_support(request):
    nav_categories = BusinessCategory.objects.all()
    nav_locations = BusinessLocation.objects.all()

    context = {
        'nav_locations':nav_locations,
        'nav_categories':nav_categories,
    }

    return render(request, 'user/support.html', context)



@login_required
def user_listings(request):
    nav_categories = BusinessCategory.objects.all()
    nav_locations = BusinessLocation.objects.all()

    try:
        listings = BusinessListing.objects.get(user=request.user.id)
    except:
        context = {
            'nav_locations':nav_locations,
            'nav_categories':nav_categories,
        }

        return render(request, 'user/listings.html', context)

    context = {
        'listings':listings,
        'nav_locations':nav_locations,
        'nav_categories':nav_categories,
    }

    return render(request, 'user/listings.html', context)



def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user-profile')
        else:
            messages.info(request,"Username or Password is not correct.")
    return render(request, 'registration/signin.html',{})



def signout(request):
    logout(request)
    return redirect('signin')



def contact(request):
    if request.method == "POST":

        message_name = request.POST['name']
        message_url = request.POST['url']
        message_email = request.POST['email']
        message = request.POST['message']


        send_mail(message_name + ' - You got a new contact form submission -' + message_url, message, message_email, ['ottomalerr@gmail.com'])

        nav_categories = BusinessCategory.objects.all()
        nav_locations = BusinessLocation.objects.all()

        context = {
        'nav_locations':nav_locations,
        'nav_categories':nav_categories,
        'message': message,
        'message_name':message_name
        }

        return render(request, 'contact.html', context)
    else:
        nav_categories = BusinessCategory.objects.all()
        nav_locations = BusinessLocation.objects.all()

        context = {
            'nav_locations':nav_locations,
            'nav_categories':nav_categories,
        }
        return render(request, 'contact.html', context)



@login_required(login_url='signup')
def submit_listing(request):
    if request.method == "POST":
        # Get the bulk of the info
        url = request.POST['website']
        address = request.POST['address']
        tagline = request.POST['tagline']
        title = request.POST['title']
        category_id_str = request.POST['category']
        description = request.POST['description']
        phone = request.POST['phone']
        plan = request.POST['pricePlan']

        # Get the opening hours
        mondayopen = request.POST['mondayopen']
        tuesdayopen = request.POST['tuesdayopen']
        wednesdayopen = request.POST['wednesdayopen']
        thursdayopen = request.POST['thursdayopen']
        fridayopen = request.POST['fridayopen']
        saturdayopen = request.POST['saturdayopen']
        sundayopen = request.POST['sundayopen']
        # Get the closing hours
        mondayclosed = request.POST['mondayclosed']
        tuesdayclosed = request.POST['tuesdayclosed']
        wednesdayclosed = request.POST['wednesdayclosed']
        thursdayclosed = request.POST['thursdayclosed']
        fridayclosed = request.POST['fridayclosed']
        saturdayclosed = request.POST['saturdayclosed']
        sundayclosed = request.POST['sundayclosed']

        # Get users info
        user = request.user

        # Get the category sorted out
        category_id_int = int(category_id_str)
        category = BusinessCategory.objects.get(id=category_id_int)

        # Store the listing
        new_listing = BusinessListing.objects.create(
        user=user,
        description=description,
        category=category,
        url=url,
        address=address,
        tagline=tagline,
        title=title,
        phone=phone,
        plan=plan,
        )

        # Store the hours
        new_hours = BusinessHours.objects.create(
        monday_open=mondayopen,
        monday_closed=mondayclosed,
        tuesday_open=tuesdayopen,
        tuesday_closed=tuesdayclosed,
        wednesday_open=wednesdayopen,
        wednesday_closed=wednesdayclosed,
        thursday_open=thursdayopen,
        thursday_closed=thursdayclosed,
        friday_open=fridayopen,
        friday_closed=fridayclosed,
        saturday_open=saturdayopen,
        saturday_closed=saturdayclosed,
        sunday_open=sundayopen,
        sunday_closed=sundayclosed,
        listing=new_listing,
        )

        # Store the image and associate with the listing
        # files = request.POST.getlist('pictures')
        # for f in files:
        #     Image.objects.create(listing=new_listing, image=f)

        # Store the faqs
        faqs = request.POST.getlist('faqs')
        faqanswers = request.POST.getlist('faqanswers')

        i = 0

        for faq in faqs:
            FrequentlyAskedQuestion.objects.create(listing=new_listing, question=faq, answer=faqanswers[i])
            i += 1


        nav_categories = BusinessCategory.objects.all()
        nav_locations = BusinessLocation.objects.all()


        context = {
        'new_listing':new_listing,
        'nav_locations':nav_locations,
        'nav_categories':nav_categories,
        }

        send_mail(title + '- Submitted a new Business Listing! - ' + phone, address, title, ['ottomalerr@gmail.com'])

        return render(request, 'submit-listing.html', context)
    else:
        nav_categories = BusinessCategory.objects.all()
        nav_locations = BusinessLocation.objects.all()

        context = {
            'nav_locations':nav_locations,
            'nav_categories':nav_categories,
        }
        return render(request, 'submit-listing.html', context)



def prices(request):
    nav_categories = BusinessCategory.objects.all()
    nav_locations = BusinessLocation.objects.all()

    context = {
        'nav_locations':nav_locations,
        'nav_categories':nav_categories,
    }

    return render(request, 'prices.html', context)



def category_detail(request, cats):
    if request.method == "POST":
        # Get the bulk of the info
        category_id = request.POST['catid']
        location = request.POST['location']

        # Get all listings that meet the post request category
        listings = BusinessListing.objects.all(category=int(category_id))

    # Get all listings that meet the page category
    listings = BusinessListing.objects.filter(category=cats)
    listing_count = listings.count()

    category = BusinessCategory.objects.get(id=cats)
    categories = BusinessCategory.objects.all()

    nav_categories = BusinessCategory.objects.all()
    nav_locations = BusinessLocation.objects.all()

    context = {
        'listings':listings,
        'listing_count':listing_count,
        'category': category,
        'categories': categories,
        'nav_locations':nav_locations,
        'nav_categories':nav_categories,
    }

    return render(request, 'category.html', context)



def location_detail(request, cats):
    # Get all listings that meet the page category

    category = BusinessCategory.objects.get(id=cats)
    categories = BusinessCategory.objects.all()

    nav_categories = BusinessCategory.objects.all()
    nav_locations = BusinessLocation.objects.all()

    listings = BusinessListing.objects.filter(state=cats)
    listing_count = listings.count()

    location = BusinessLocation.objects.get(id=cats)

    context = {
        'location':location,
        'listings':listings,
        'listing_count':listing_count,
        'category': category,
        'categories': categories,
        'nav_locations':nav_locations,
        'nav_categories':nav_categories,
    }

    return render(request, 'location.html', context)



def post_category_detail(request, cats):
    categories = Category.objects.all()
    most_recent = Post.objects.order_by('-timestamp')[:3]

    cat_posts = Post.objects.filter(categories=cats)
    posts = Post.objects.all()
    category = categories.get(id=cats)

    nav_categories = BusinessCategory.objects.all()
    nav_locations = BusinessLocation.objects.all()

    context = {
        'most_recent':most_recent,
        'categories':categories,
        'cat_posts':cat_posts,
        'posts': posts,
        'category':category,
        # 'categories': categories,
        'nav_locations':nav_locations,
        'nav_categories':nav_categories,
    }

    return render(request, 'post-category.html', context)



def listing_detail(request, pk):
    listing = BusinessListing.objects.get(id=pk)

    nav_categories = BusinessCategory.objects.all()
    nav_locations = BusinessLocation.objects.all()

    business_listings = BusinessListing.objects.all()

    images = Image.objects.filter(listing=listing)

    hours = BusinessHours.objects.get(listing=listing)

    header_image = images[0]

    faqs = FrequentlyAskedQuestion.objects.all().filter(listing=listing)

    context = {
        'faqs':faqs,
        'header_image':header_image,
        'images':images,
        'hours':hours,
        'business_listings':business_listings,
        'listing': listing,
        'nav_locations':nav_locations,
        'nav_categories':nav_categories,
    }

    return render(request, 'listing.html', context)



def listings(request):
    listings = BusinessListing.objects.all()

    nav_categories = BusinessCategory.objects.all()
    nav_locations = BusinessLocation.objects.all()

    context = {
        'listings': listings,
        'nav_locations':nav_locations,
        'nav_categories':nav_categories,
    }
    return render(request, 'all-listings.html', context)



def post_detail(request, pk):
    # category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = Post.objects.get(id=pk)
    categories = Category.objects.all()

    nav_categories = BusinessCategory.objects.all()
    nav_locations = BusinessLocation.objects.all()

    context = {
        'categories':categories,
        'post': post,
        'most_recent': most_recent,
        'nav_locations':nav_locations,
        'nav_categories':nav_categories,
        # 'category_count': category_count,
    }
    return render(request, 'post.html', context)



def posts(request):
    categories = Category.objects.all()
    posts = Post.objects.all()
    nav_categories = BusinessCategory.objects.all()
    nav_locations = BusinessLocation.objects.all()
    most_recent = Post.objects.order_by('-timestamp')[:3]

    context = {
        'most_recent':most_recent,
        'categories':categories,
        'posts': posts,
        'nav_locations':nav_locations,
        'nav_categories':nav_categories,
    }
    return render(request, 'blog.html', context)



# def search(request):
#     if request.method == 'POST': # check post
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             query = form.cleaned_data['query'] # get form input data
#             catid = form.cleaned_data['catid']
#             if catid==0:
#                 products=Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
#             else:
#                 products = Product.objects.filter(title__icontains=query,category_id=catid)

#             category = Category.objects.all()

#             nav_categories = BusinessCategory.objects.all()
#             nav_locations = BusinessLocation.objects.all()

#             context = {
#                 'products': products,
#                 'query':query,
#                 'category': category,
#                 'nav_locations':nav_locations,
#                 'nav_categories':nav_categories,
#                 }
#             return render(request, 'search_products.html', context)

#     return HttpResponseRedirect('/')


# def search_auto(request):
#     if request.is_ajax():
#         q = request.GET.get('term', '')
#         products = Product.objects.filter(title__icontains=q)

#         results = []
#         for rs in products:
#             product_json = {}
#             product_json = rs.title +" > " + rs.category.title
#             results.append(product_json)
#         data = json.dumps(results)
#     else:
#         data = 'fail'
#     mimetype = 'application/json'
#     return HttpResponse(data, mimetype)

# form = EmailSignupForm()



def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None



class SearchView(View):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(overview__icontains=query)
            ).distinct()

        nav_categories = BusinessCategory.objects.all()
        nav_locations = BusinessLocation.objects.all()

        context = {
            'queryset': queryset,
            'nav_locations':nav_locations,
            'nav_categories':nav_categories,
        }
        return render(request, 'search_results.html', context)



# category/location search
def index_search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location'] # get form input data
            catid = form.cleaned_data['catid']

            category = BusinessCategory.objects.filter(title__icontains=catid)  #SELECT * FROM product WHERE title LIKE '%query%'
            location = BusinessLocation.objects.filter(title__icontains=location)  #SELECT * FROM product WHERE title LIKE '%query%'


            context = {'category': category, 'location':location }
            return render(request, 'results.html', context)

    return HttpResponseRedirect('/')



# blog post search
def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()

    nav_categories = BusinessCategory.objects.all()
    nav_locations = BusinessLocation.objects.all()
    context = {
        'queryset': queryset,
        'nav_locations':nav_locations,
        'nav_categories':nav_categories,
    }
    return render(request, 'search_results.html', context)



def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset



class IndexView(View):
    # form = EmailSignupForm()

    def get(self, request, *args, **kwargs):
        nav_categories = BusinessCategory.objects.all()
        nav_locations = BusinessLocation.objects.all()

        business_categories = BusinessCategory.objects.all()
        business_locations = BusinessLocation.objects.all()

        business_listings = BusinessListing.objects.all()

        featured = Post.objects.filter(featured=True)
        latest = Post.objects.order_by('-timestamp')[0:3]

        context = {
            'nav_locations':nav_locations,
            'nav_categories':nav_categories,
            'business_listings':business_listings,
            'business_categories':business_categories,
            'business_locations':business_locations,
            'object_list': featured,
            'latest': latest,
        }
        return render(request, 'theapp/index.html', context)



    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
        messages.info(request, "Successfully subscribed")
        return redirect("home")



def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    nav_categories = BusinessCategory.objects.all()
    nav_locations = BusinessLocation.objects.all()

    business_listings = BusinessListing.objects.all()

    business_categories = BusinessCategory.objects.all()
    business_locations = BusinessLocation.objects.all()

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'business_listings':business_listings,
        'nav_locations':nav_locations,
        'nav_categories':nav_categories,
        'business_categories':business_categories,
        'business_locations':business_locations,
        'object_list': featured,
        'latest': latest,
    }
    return render(request, 'theapp/index.html', context)



def location_search(request):
    if request.method == "POST":
        category_id = request.POST['catid']
        location = request.POST['location']
        # Get all listings that meet the post request category
        category_listings = BusinessListing.objects.filter(category=category_id)
        # Filter just the ones in the location they chose
        location_listings = category_listings.filter(state=location)

        location_listing_count = location_listings.count()
        category_listing_count = category_listings.count()

        nav_categories = BusinessCategory.objects.all()
        nav_locations = BusinessLocation.objects.all()


        context = {
            # counts for each one
            'location_listing_count':location_listing_count,
            # nav data
            'nav_locations':nav_locations,
            'nav_categories':nav_categories,
            # both kinds of listng result
            'location_listings':location_listings,
        }

        return render(request, 'search_result_listings.html', context)



##################### MARKETING #####################
MAILCHIMP_API_KEY = settings.MAILCHIMP_API_KEY
MAILCHIMP_DATA_CENTER = settings.MAILCHIMP_DATA_CENTER
MAILCHIMP_EMAIL_LIST_ID = settings.MAILCHIMP_EMAIL_LIST_ID

api_url = 'https://{dc}.api.mailchimp.com/3.0'.format(dc=MAILCHIMP_DATA_CENTER)
members_endpoint = '{api_url}/lists/{list_id}/members'.format(
    api_url=api_url,
    list_id=MAILCHIMP_EMAIL_LIST_ID
)



def subscribe(email):
    data = {
        "email_address": email,
        "status": "subscribed"
    }
    r = requests.post(
        members_endpoint,
        auth=("", MAILCHIMP_API_KEY),
        data=json.dumps(data)
    )
    return r.status_code, r.json()



def email_list_signup(request):
    form = EmailSignupForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email_signup_qs = Signup.objects.filter(email=form.instance.email)
            if email_signup_qs.exists():
                messages.info(request, "You are already subscribed")
            else:
                subscribe(form.instance.email)
                form.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def custom_error_404(request, exception):
    return render(request, 'theapp/404.html', {})



def custom_error_500(request):
    return render(request, 'theapp/500.html', {})



def custom_error_403(request, exception):
    return render(request, 'theapp/403.html', {})
