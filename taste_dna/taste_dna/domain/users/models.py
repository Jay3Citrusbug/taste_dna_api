import uuid
from lib.data_manipulation.type_conversion import asdict
from typing import Union
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from dataclasses import dataclass, field
from dataclass_type_validator import dataclass_validate
from django.core.validators import validate_email
from lib.django import custom_models



@dataclass(frozen=True)
class UserID:
    """
    This is a value object that should be used to generate and pass the UserID to the UserFactory
    """

    id: uuid.UUID = field(init=False, default_factory=uuid.uuid4)


@dataclass_validate(before_post_init=True)
@dataclass(frozen=True)
class UserPersonalData:
    """
    This is a value object that should be used to pass user personal data to the UserFactory
    """

    email: str
    username: Union[str, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None

    def __post_init__(self):
        validate_email(self.email)


@dataclass_validate(before_post_init=True)
@dataclass(frozen=True)
class UserBasePermissions:
    """
    This is a value object that should be used to pass user base permissions to the UserFactory
    """

    is_staff: bool
    is_active: bool


class UserManagerAutoID(UserManager):
    """
    A User Manager that sets the uuid on a model when calling the create_superuser function.
    """

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        if id not in extra_fields:
            extra_fields = dict(extra_fields, id=UserID().id)

        return self._create_user(username, email, password, **extra_fields)


# Create your models here.
class User(AbstractUser, custom_models.DatedModel):
    """
    A User replaces django's default user id with a UUID that should be created by the application, not the database.
    """

    STATUS_PENDING = "pending"
    STATUS_VERIFIED = "verified"
    STATUS_CHOICES = [
        (STATUS_PENDING, "pending"),
        (STATUS_VERIFIED, "verified"),
    ]

    id = models.UUIDField(primary_key=True, editable=False)
    profile_image = models.ImageField(
        upload_to="images/", null=True, blank=True, verbose_name="profile_images"
    )
    google_auth_id = models.CharField(max_length=50, null=True, blank=True)
    following = models.ManyToManyField("self", blank=True)
    follower = models.ManyToManyField("self", blank=True)
    is_new_user = models.BooleanField(default=True)
    is_verified = models.CharField(max_length=150, choices=STATUS_CHOICES)

    objects = UserManagerAutoID()


class UserFactory:
    @staticmethod
    def build_entity_with_id(
        personal_data: UserPersonalData,
        base_permissions: UserBasePermissions,
        google_auth_id: str = None,
    ):
        personal_data_dict = asdict(personal_data, skip_empty=True)
        base_permissions_dict = asdict(base_permissions, skip_empty=True)
        return User(
            id=UserID().id,
            **personal_data_dict,
            **base_permissions_dict,
            google_auth_id=google_auth_id,
        )
