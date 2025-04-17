from django.shortcuts import render
from .models import Project
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from .models import Project, ProjectParticipation 

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect


User = get_user_model() 




@login_required(login_url='login')
def project_list_view(request):
    query = request.GET.get("q", "").strip()
    project_name = request.GET.get("project_name", "").strip()
    location = request.GET.get("location", "").strip()
    description = request.GET.get("description", "").strip()
    skills_required = request.GET.get("skills_required", "").strip()
    time_commitment = request.GET.get("time_commitment", None)

    projects = Project.objects.all()

    # Use Q objects to allow any filter to match
    filter_conditions = Q()

    if query:
        filter_conditions |= Q(title__icontains=query)
    if project_name:
        filter_conditions |= Q(title__icontains=project_name)
    if location:
        filter_conditions |= Q(location__icontains=location)
    if description:
        filter_conditions |= Q(description__icontains=description)
    if skills_required:
        filter_conditions |= Q(skills_required__icontains=skills_required)
    if time_commitment and time_commitment.isdigit():
        filter_conditions |= Q(time_commitment__lte=int(time_commitment))

    if filter_conditions:
        projects = projects.filter(filter_conditions)

    print("Filtered Projects:", projects)  # Debugging line
    print("Queryset Count:", projects.count())  # Debugging line

    return render(request, "projects/project_list.html", {"projects": projects})



# projects/views.py


#from django.shortcuts import render, get_object_or_404
#from .models import Project
#@login_required(login_url='login')
#def project_detail_view(request, project_id):
#    project = get_object_or_404(Project, id=project_id)  # Fetch the project by ID
#    return render(request, 'projects/project_detail.html', {'project': project})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def project_detail_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    events = project.events.all()
    comments = project.comments.all().order_by('-created_at')  # Fetch all comments
    unread_notifications = request.user.notification_set.filter(read=False)

    if request.method == 'POST':
        print("Received POST request:", request.POST)  # Debugging
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.user = request.user
            comment.save()
            print("Comment saved:", comment.content)  # Debugging
            return redirect('projects:project_detail', project_id=project.id)  # Redirect to the same page
        else:
            print("Form errors:", form.errors)  # Debugging
    else:
        form = CommentForm()

    context = {
        'project': project,
        'events': events,
        'comments': comments,
        'form': form,
        'unread_notifications': unread_notifications
    }

    return render(request, 'projects/project_detail.html', context)





from django.shortcuts import render, redirect
from .forms import ProjectForm
from .models import Project
from django.contrib.auth.decorators import login_required
from users.models import Volunteer

from django.shortcuts import render, redirect
from .forms import ProjectForm
from .models import Project
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm
from users.models import Volunteer
from django.contrib.admin.views.decorators import staff_member_required

@login_required(login_url='login')
def create_project_view(request):
    if not request.user.is_organizer or not request.user.is_approved:
        return redirect('projects:project_list')  # Redirect if user is not an approved organizer

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.is_approved = False  # Needs admin approval
            project.save()
            return redirect('projects:project_list')  # Redirect after submission
    else:
        form = ProjectForm()
    
    return render(request, 'projects/create_project.html', {'form': form})





@staff_member_required  # Only admin can approve projects
def approve_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.is_approved = True
    project.save()
    return redirect('admin_dashboard')

@staff_member_required  # Only admin can approve organizers
def approve_organizer(request, volunteer_id):
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)
    volunteer.is_approved = True
    volunteer.save()
    return redirect('admin_dashboard')









from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def join_project_view(request, project_id):
    project = Project.objects.get(id=project_id)
    
    # Check if the user is already participating in the project
    if ProjectParticipation.objects.filter(user=request.user, project=project).exists():
        # You can show an error or just redirect
        return redirect('projects:project_list')  # Example, you can show a message saying they can't join twice
    
    if request.method == "POST":
        participation_type = request.POST.get("participation_type")
        skills = request.POST.get("skills") if participation_type == 'volunteering' else None
        
        # Create and save the new participation record
        participation = ProjectParticipation(
            user=request.user,
            project=project,
            participation_type=participation_type,
            skills=skills
        )
        participation.save()
        
        return redirect('projects:project_list')
    
    return render(request, 'project_detail.html', {'project': project})




# views.py


from django.core.mail import send_mail
from django.conf import settings

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Event
from .forms import ProjectForm, EventForm


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, VolunteerProject  # Import VolunteerProject
from .forms import ProjectForm, EventForm
from django.core.mail import send_mail
from django.conf import settings

@login_required(login_url='login')
def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id, created_by=request.user)

    if request.method == 'POST':
        print("Received POST request:", request.POST)

        if 'project_update' in request.POST:
            form = ProjectForm(request.POST, instance=project)
            if form.is_valid():
                form.save()
                print("Project updated successfully!")
                return redirect('projects:project_detail', project_id=project.id)
            print("Project update form errors:", form.errors)
            event_form = EventForm()  # Initialize event_form for rendering errors

        elif 'event_create' in request.POST:
            event_form = EventForm(request.POST)
            if event_form.is_valid():
                event = event_form.save(commit=False)
                event.project = project
                event.save()

                # Fetch emails of all volunteers and attendees (excluding project creator)
                recipient_emails = list(
                    project.projectparticipation_set
                    .filter(participation_type__in=['volunteering', 'attending'])  # Get both
                    .values_list('user__email', flat=True)
                )

                print("Recipient Emails List:", recipient_emails)

                if recipient_emails:
                    print("Sending email to:", recipient_emails)

                    subject = f"New Event Created: {event.name}"
                    message = f"""
A new event has been created for the project: {project.title}

Event: {event.name}  
Description: {event.description}  
Date: {event.date.strftime('%B %d, %Y at %I:%M %p')}

Thank you for being an active part of the community. We look forward to your participation!



Best regards,
The VISHNU Team 
📧 vishnucommunity@gmail.com
"""
                    from_email = settings.DEFAULT_FROM_EMAIL
                    send_mail(subject, message, from_email, recipient_emails, fail_silently=False)
                    print("Event created and email notifications sent successfully!")
                else:
                    print("No participants found to send email notifications.")

                return redirect('projects:project_detail', project_id=project.id)

            print("Event form errors:", event_form.errors)
            form = ProjectForm(instance=project)  # Re-initialize ProjectForm with instance for error display

        else:  # This handles cases where neither 'project_update' nor 'event_create' is in POST
            form = ProjectForm(instance=project)
            event_form = EventForm()

    else:  # This is the GET request
        form = ProjectForm(instance=project)
        event_form = EventForm()

    return render(request, 'projects/update_project.html', {
        'form': form,
        'event_form': event_form,
        'project': project
    })




@login_required(login_url='login')
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, created_by=request.user)  # Ensure the user is the project creator
    if request.method == 'POST':
        project.delete()
        return redirect('organiser_dashboard')  # Redirect to the organizer dashboard
    return render(request, 'projects/delete_project.html', {'project': project})



    # projects/views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project

@login_required(login_url='login')
def leave_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user = request.user

    # Remove the user from the project's volunteers
    project.volunteers.remove(user)

    return redirect('volunteer_dashboard')




from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event, Notification

@receiver(post_save, sender=Event)
def notify_users_on_event_creation(sender, instance, created, **kwargs):
    if created:
        # Notify volunteers
        for user in instance.volunteers.all():
            message = f"New event '{instance.name}' has been created for the project '{instance.project.name}'."
            Notification.objects.create(user=user, message=message)







# This where i write commnets views


