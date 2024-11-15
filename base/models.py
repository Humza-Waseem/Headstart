from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    academic_performance = models.CharField(max_length=10)  # GPA or other metric
    interests = models.TextField()  # Interests like fields of study or career areas
    
    def __str__(self):
        return self.name

# Career Recommendation Model
class CareerRecommendation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    recommended_career = models.CharField(max_length=100)
    description = models.TextField()  # Description of the career
    relevance_score = models.FloatField()  # How well it fits the student's profile
    
    def __str__(self):
        return f"{self.student.name} - {self.recommended_career}"

# Startup Idea Model
class StartupIdea(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    idea_title = models.CharField(max_length=100)
    idea_description = models.TextField()
    validation_score = models.FloatField(default=0.0)  # Score after idea validation

    def __str__(self):
        return f"{self.student.name} - {self.idea_title}"
