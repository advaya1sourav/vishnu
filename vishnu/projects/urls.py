
from django.urls import path
from .views import project_list_view, project_detail_view, create_project_view , approve_project, approve_organizer, delete_project
from . import views
from .views import update_project 

app_name = 'projects'


urlpatterns = [
    path('', project_list_view, name='project_list'),
    path('<int:project_id>/', project_detail_view, name='project_detail'),
    path('create/', create_project_view, name='create_project'),
    path('projects/<int:project_id>/join/', views.join_project_view, name='join_project'),
    path('projects/<int:project_id>/update/', views.update_project, name='update_project'),  # Use 'project_id' consistently
    # path('delete/<int:project_id>/', views.delete_project, name='delete_project'),
    path('projects/delete/<int:pk>/', delete_project, name='delete_project'),

   


    path('<int:project_id>/leave/', views.leave_project_view, name='leave_project'),
    path('approve_project/<int:project_id>/', approve_project, name='approve_project'),
    path('approve_organizer/<int:volunteer_id>/', approve_organizer, name='approve_organizer'),
]

