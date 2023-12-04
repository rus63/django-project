from http import HTTPStatus
from typing import List, Union, Any, OrderedDict, Optional

from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import User
from tests.action_client import ActionClient
from tests.factories.user_factory import UserFactory


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    action_client: ActionClient
    basename: str
    user_attributes: dict


    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user_attributes = UserFactory.build()
        cls.user = cls.create_api_user()
        cls.client = APIClient()
        cls.action_client = ActionClient(cls.client)

    def set_token(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    @classmethod
    def create_api_user(cls) -> User:
        return User.objects.create(**cls.user_attributes)

    @classmethod
    def detail_url(cls, key: Union[int, str], args=None) -> str:
        keys = [key]
        if args:
            keys.insert(0, args)
        return reverse(f"{cls.basename}-detail", args=keys)

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
        response = self.client.get(self.list_url(args), args=query_params)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def retrieve(self, args: Any, id=None, params=None) -> dict:
        response = self.client.get(self.detail_url(args, id), params)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def update(self, data: dict, args: List[Union[str, int]]) -> dict:
        response = self.client.put(self.detail_url(args), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def delete(self, args: Any) -> None:
        response = self.client.delete(self.detail_url(args))
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content

    def request_single_resource(self, data: dict = None) -> Response:
        return self.client.get(self.list_url(), data=data)

    def single_resource(self, data: dict = None) -> dict:
        response = self.request_single_resource(data)
        assert response.status_code == HTTPStatus.OK
        return response.data

    def request_patch_single_resource(self, attributes: dict) -> Response:
        url = self.list_url()
        return self.client.patch(url, data=attributes)

    def patch_single_resource(self, attributes: dict) -> dict:
        response = self.request_patch_single_resource(attributes)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data
