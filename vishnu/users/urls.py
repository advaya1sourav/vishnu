
from django.urls import path
from .views import volunteer_dashboard_view, organiser_dashboard_view, profile_view, contact_view, about_view , volunteer_profile_view , profile_update_view 



urlpatterns = [
    path('volunteer-dashboard/', volunteer_dashboard_view, name='volunteer_dashboard'),
    path('organiser-dashboard/', organiser_dashboard_view, name='organiser_dashboard'),
    path('profile/', profile_view, name='profile'),
    path('contact/', contact_view, name='contact'),
    path('about/', about_view, name='about'),
    path('volunteer-profile/<int:user_id>/', volunteer_profile_view, name='volunteer_profile'),
    path('profile_update/', profile_update_view, name='profile_update'),

    

    
]
