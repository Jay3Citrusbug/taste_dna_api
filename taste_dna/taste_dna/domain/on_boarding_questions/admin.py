from django.contrib import admin
from .models import OnboardingQuestion,QuestionAnswer,QuestionOption

admin.site.register(OnboardingQuestion)
admin.site.register(QuestionAnswer)

admin.site.register(QuestionOption)

