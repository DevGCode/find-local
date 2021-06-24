from django.contrib import admin

from .models import *

#Leads/CRM
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_name', 'name')


admin.site.register(Lead, SupportTicketAdmin)

#Website
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostView)
admin.site.register(FrequentlyAskedQuestion)
admin.site.register(BusinessCategory)
admin.site.register(BusinessListing)
admin.site.register(Image)
admin.site.register(BusinessHours)
admin.site.register(BusinessLocation)
#Marketing
admin.site.register(Signup)
