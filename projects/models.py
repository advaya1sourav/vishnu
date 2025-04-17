from django.db import models
from django.conf import settings  # Import settings to get AUTH_USER_MODEL
from django.utils import timezone
from users.models import Volunteer  # Import the Volunteer model from users/models.py
from django.contrib.auth.models import User

# Import settings to use AUTH_USER_MODEL


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    skills_required = (
        models.TextField()
    )  # Changed from CharField to allow longer text if needed
    time_commitment = models.IntegerField()  # Changed from CharField to IntegerField
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_projects",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(default=timezone.now)
    volunteers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="volunteered_projects", blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)  # Admin must approve projects

    def __str__(self):
        return self.title


class VolunteerProject(models.Model):
    volunteer = models.ForeignKey(
        Volunteer, on_delete=models.CASCADE, related_name="volunteer_projects"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="project_volunteers"
    )
    date_joined = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[("Pending", "Pending"), ("Accepted", "Accepted")],
        default="Pending",
    )

    def __str__(self):
        return f"{self.volunteer.username} - {self.project.title}"


from django.db import models
from django.conf import settings


class ProjectParticipation(models.Model):
    ATTENDING = "attending"
    VOLUNTEERING = "volunteering"
    PARTICIPATION_CHOICES = [
        (ATTENDING, "Attending"),
        (VOLUNTEERING, "Volunteering"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    participation_type = models.CharField(max_length=50, choices=PARTICIPATION_CHOICES)
    skills = models.TextField(blank=True, null=True)

    # Ensure a user can't join a project more than once, regardless of participation type
    class Meta:
        unique_together = (
            "user",
            "project",
        )  # Prevents the same user from joining the same project more than once

    def __str__(self):
        return f"{self.user} in {self.project} as {self.participation_type}"


# Event Model (New)
from django.conf import settings
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="events"
    )  # Add related_name

    volunteers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="volunteered_events"
    )


# Notification Model (New)
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"


# This is where i write comments class

from django.db import models
from django.conf import settings  # Import settings to get AUTH_USER_MODEL


class Comment(models.Model):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # Use AUTH_USER_MODEL
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}"
