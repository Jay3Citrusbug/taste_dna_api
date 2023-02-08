from taste_dna.interface.on_boarding_questions.views import onboardingquestionViewSet
# from rest_framework.routers import DefaultRouter
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'questions', onboardingquestionViewSet, basename='question')