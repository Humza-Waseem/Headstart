from django.contrib import admin

from .models import Student, CareerRecommendation, StartupIdea

# Register your models here.
admin.site.register(Student)
admin.site.register(CareerRecommendation)
admin.site.register(StartupIdea)