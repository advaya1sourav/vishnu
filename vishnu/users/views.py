from django.shortcuts import render
from projects.models import Project


# users/views.py

from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def volunteer_dashboard_view(request):
    # Get the logged-in user
    user = request.user

    # Get the projects the user has joined
    joined_projects = Project.objects.filter(projectparticipation__user=request.user)


    # Pass the projects to the template
    return render(request, 'users/volunteer_dashboard.html', {'joined_projects': joined_projects})


# users/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def organiser_dashboard_view(request):
    # Get projects created by the logged-in user (organizer)
    projects = Project.objects.filter(created_by=request.user)
    
    # Pass the projects to the template
    return render(request, 'users/project_organiser_dashboard.html', {'projects': projects})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='login')
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})

@login_required(login_url='login')
def contact_view(request):
    return render(request, 'users/contact.html')
@login_required(login_url='login')
def about_view(request):
    return render(request, 'users/about.html')


from django.shortcuts import render, get_object_or_404
from .models import Volunteer
@login_required(login_url='login')
def volunteer_profile_view(request, user_id):
    volunteer = get_object_or_404(Volunteer, id=user_id)
    return render(request, 'users/volunteer_profile.html', {'volunteer': volunteer})


# users/views.py
# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from users.models import Volunteer

@login_required(login_url='login')
def profile_update_view(request):
    volunteer = get_object_or_404(Volunteer, pk=request.user.pk)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=volunteer)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=volunteer)

    return render(request, 'users/profile_update.html', {'form': form})










    


