from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Volunteer
from django.urls import reverse

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_organizer', 'request_organizer')
    list_filter = ('is_organizer', 'request_organizer')
    actions = ['approve_organizer']

    def approve_organizer(self, request, queryset):
        queryset.update(is_organizer=True, request_organizer=False)
        self.message_user(request, "Selected users are now organizers.")

    approve_organizer.short_description = "Approve selected users as Organizers"

class MyAdminSite(admin.AdminSite):
    site_header = 'Vishnu Admin'
    site_title = "Commuinity Connect Admin Panel"  # Title for browser tab
    index_title = "Greatings"  # Dashboard title
     

    def each_context(self, request):
        context = super().each_context(request)
        context["site_url"] = reverse('projects:project_list')  # Dynamically set "View Site" URL
        return context

admin.site = MyAdminSite(name='customadmin')
admin.site.register(User)
admin.site.register(Volunteer, VolunteerAdmin)