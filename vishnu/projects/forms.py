from django import forms
from .models import Project, Event


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'location', 'skills_required', 'time_commitment']

    def clean_time_commitment(self):
        time_commitment = self.cleaned_data.get('time_commitment')
        if time_commitment < 1:
            raise forms.ValidationError("Time commitment cannot be negative.")
        return time_commitment








class EventForm(forms.ModelForm):
    date = forms.DateTimeField(
    widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    input_formats=['%Y-%m-%dT%H:%M']
)

    class Meta:
        model = Event
        fields = ['name', 'description', 'date']




# the form for comments
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Ensure this matches the field in the Comment model


