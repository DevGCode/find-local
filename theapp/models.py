from django.db import models
from datetime import datetime, date
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()



class BusinessLocation(models.Model):
    state = models.CharField(max_length=20)
    thumbnail = models.ImageField()


    def __str__(self):
        return self.state



class BusinessCategory(models.Model):
    title = models.CharField(max_length=20)
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title

DEFAULT_LOCATION_ID = 1



class BusinessListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(BusinessCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=220)
    tagline = models.CharField(max_length=200)
    description = RichTextField(default=False)
    # address used for full address
    address = models.CharField(max_length=200)
    # city/state used for filtering
    state = models.ForeignKey(BusinessLocation, on_delete=models.CASCADE, default=DEFAULT_LOCATION_ID)
    phone = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    # added manually on approval
    thumbnail = models.ImageField()
    published = models.BooleanField(default=False)
    claimed = models.BooleanField(default=False)
    # plan type is saved for billing purposes
    plan = models.CharField(max_length=100)


    @property
    def imageURL(self):
        try:
            url = self.thumbnail.url
        except:
            url = ''
        return url


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('listing-detail', kwargs={
            'pk': self.pk
        })



class BusinessHours(models.Model):
    m_f_open = models.CharField(max_length=220)
    m_f_closed = models.CharField(max_length=220)
    saturday_open = models.CharField(max_length=220)
    saturday_closed = models.CharField(max_length=220)
    sunday_open = models.CharField(max_length=220)
    sunday_closed = models.CharField(max_length=220)
    listing = models.ForeignKey(BusinessListing, on_delete=models.CASCADE)

    def __str__(self):
        return self.listing.title



class Image(models.Model):
    listing = models.ForeignKey(BusinessListing, on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return self.image.url



class FrequentlyAskedQuestion(models.Model):
    listing = models.ForeignKey(BusinessListing, on_delete=models.CASCADE)
    question = models.CharField(max_length=320)
    answer = models.CharField(max_length=1520)

    def __str__(self):
        return self.listing.title



class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username



class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title



class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = RichTextField(default=False)
    # view_count = models.IntegerField(default = 0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'pk': self.pk
        })

    def get_update_url(self):
        return reverse('post-update', kwargs={
            'pk': self.pk
        })

    def get_delete_url(self):
        return reverse('post-delete', kwargs={
            'pk': self.pk
        })

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()



class Lead(models.Model):
    # Save the time the lead became a customer
    customer = models.BooleanField(default=False)
    # This will remove the lead from all lists
    call_list = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    business_name = models.CharField(max_length=100)
    business_type = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=50)
    note = models.TextField(help_text='Notes')
    # Time they became a lead
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '#{0} - {1}'.format(self.id, self.name)

    def get_absolute_url(self):
        return reverse('dashboard')



class Signup(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
