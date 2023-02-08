from typing import Type
from .models import User, UserFactory
from django.contrib.auth import authenticate
from django.db.models.manager import BaseManager
from lib.django.exceptions import InvalidUserException


class UserServices:
    @staticmethod
    def get_user_factory() -> Type[UserFactory]:
        return UserFactory
    
    @staticmethod
    def get_user_repo() -> BaseManager[User]:
        return User.objects
    