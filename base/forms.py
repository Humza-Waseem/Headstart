from django import forms
from .models import Student, StartupIdea

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'academic_performance', 'interests']

class StartupIdeaForm(forms.ModelForm):
    class Meta:
        model = StartupIdea
        fields = ['idea_title', 'idea_description']
