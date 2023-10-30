from http import HTTPStatus
from typing import List, Union, Any, OrderedDict

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import User


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str
    user_attributes = {
        "username": "johnsmith",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
        "role": "developer",
        # "is_staff": True
    }

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        cls.client = APIClient()

    def set_token(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    @classmethod
    def create_api_user(cls) -> User:
        return User.objects.create(**cls.user_attributes)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        response = self.client.post(self.list_url(args), data=data)
        # print(response.status_code)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def list(
        self, query_params: dict = None, args: List[Union[str, int]] = None
    ) -> dict:
        response = self.client.get(self.list_url(query_params), args=args)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def retrieve(self, args: Any) -> dict:
        response = self.client.get(self.detail_url(args))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def update(self, data: dict, args: List[Union[str, int]]) -> dict:
        response = self.client.put(self.detail_url(args), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def delete(self, args: Any) -> None:
        response = self.client.delete(self.detail_url(args))
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content
