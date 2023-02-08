from django.db.models.query import QuerySet
from rest_framework_simplejwt.tokens import RefreshToken
from taste_dna.domain.users.models import User
from taste_dna.domain.users.services import UserServices


class UserAppServices:
    def __init__(self) -> None:
        self.user_services = UserServices()

    def list_users(self) -> QuerySet[User]:
        return self.user_services.get_user_repo().all()
    

    def get_user_token(self, user: User):
        token = RefreshToken.for_user(user)
        data = dict(
            status=True,
            message="You have logged in successfully",
            access=str(token.access_token),
            refresh=str(token),
        )
        return data
    def get_user_by_pk(self,pk) -> User:
        return self.list_users().get(pk=pk)

    def delete_user_by_pk(self,pk) -> User:
        instance =self.get_user_by_pk(pk=pk)
        instance.delete()
        return instance