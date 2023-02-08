"""taste_dna URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from django.urls import include, path
from rest_framework import routers
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .users import views
from .on_boarding_questions import views
from django.conf import settings, urls as URL
from django.views.generic.base import RedirectView
from taste_dna.interface.on_boarding_questions.urls import router as question_router
# import urls from interface layer modules

ENABLE_API = settings.ENABLE_API
PROJECT_URL = ""
API_SWAGGER_URL = "api/v0/"
REDIRECTION_URL = API_SWAGGER_URL if ENABLE_API else PROJECT_URL


router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# router.register(r"users", views.UserViewSet, basename="Users")
# router.register('questions', views.onboardingquestionViewSet, basename='question')
router.register('questionanswer', views.QuestionAnswerViewSet, basename='questionanswer')
router.register('questionoption', views.QuestionOptionViewSet, basename='questionoption')



# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("",include(router.urls)),
    path("",include(question_router.urls))

    # path("", RedirectView.as_view(url="api/v0/", permanent=False)),
]


