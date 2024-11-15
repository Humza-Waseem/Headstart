from django.shortcuts import render, redirect
from .forms import StudentForm, StartupIdeaForm
from .models import CareerRecommendation, StartupIdea
from .ai_module import get_career_recommendations, validate_startup_idea
from django.contrib.auth.decorators import login_required


# def homepage(request):
#    return render(request, 'base/homepage.html')

# def GuestHomePage(request):
#     return render(request, 'base/GuestHomePage.html')

# @login_required
# def UserHomePage(request):
#     return render(request, 'base/UserHomePage.html')


def student_profile(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            # Call AI model to get career recommendations
            recommendations = get_career_recommendations(student)
            for rec in recommendations:
                CareerRecommendation.objects.create(
                    student=student,
                    recommended_career=rec['career'],
                    description=rec['description'],
                    relevance_score=rec['score']
                )
            return redirect('career_recommendations', student_id=student.id)
    else:
        form = StudentForm()
    return render(request, 'base/student_profile.html', {'form': form})

# Career Recommendation View
def career_recommendations(request, student_id):
    recommendations = CareerRecommendation.objects.filter(student_id=student_id)
    return render(request, 'base/career_recommendations.html', {'recommendations': recommendations})

# Startup Idea View
def startup_idea(request):
    if request.method == 'POST':
        form = StartupIdeaForm(request.POST)
        if form.is_valid():
            startup_idea = form.save()
            # Call AI model for startup idea validation
            validation_score = validate_startup_idea(startup_idea)
            startup_idea.validation_score = validation_score
            startup_idea.save()
            return redirect('startup_results', idea_id=startup_idea.id)
    else:
        form = StartupIdeaForm()
    return render(request, 'base/startup_idea.html', {'form': form})

# Startup Validation Result View
def startup_results(request, idea_id):
    idea = StartupIdea.objects.get(id=idea_id)
    return render(request, 'base/startup_results.html', {'idea': idea})
