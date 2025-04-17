from django import forms
from .models import Volunteer
from projects.models import Project  

# Profile update form excluding username and email
class ProfileUpdateForm(forms.ModelForm):
    request_organizer = forms.BooleanField(required=False, label="Request to become an organizer")

    class Meta:
        model = Volunteer
        fields = ['dob', 'skills', 'location', 'experience']

    def save(self, commit=True):
        volunteer = super().save(commit=False)
        if self.cleaned_data.get('request_organizer'):
            volunteer.request_organizer = True  # Store request flag
        if commit:
            volunteer.save()
        return volunteer


        
# Project form to create or update projects
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'location', 'skills_required', 'time_commitment']







