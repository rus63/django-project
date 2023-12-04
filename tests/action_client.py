from http import HTTPStatus
from typing import Optional

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import User
from main.serializers import TaskSerializer
from tests.factories.tag_factory import TagFactory
from tests.factories.task_factory import TaskFactory
from tests.factories.user_factory import UserFactory


class ActionClient:
    def __init__(self, api_client: APIClient) -> None:
        self.api_client = api_client
        # self.user: User
        self.user_attr = UserFactory.build()
        self.user = User.objects.create_user(**self.user_attr)

    def init_user(self) -> None:

        self.set_token()
        self.api_client.force_authenticate(user=self.user)

    def set_token(self):
        refresh = RefreshToken.for_user(self.user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def create_user(self, **attributes):
        # self.init_user()
        self.set_token()
        response = self.request_create_user(**attributes)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def request_create_user(self, **attributes):
        user_attr = UserFactory.build(**attributes)
        return self.api_client.post(reverse(f"users-list"), data=user_attr,)

    def create_task(self, **attributes):
        # self.init_user()
        response = self.request_create_task(**attributes)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def request_create_task(self, **attributes):
        task = TaskFactory.build(**attributes)
        return self.api_client.post(reverse(f"tasks-list"), data=task, format="json")

    def create_tag(self, **attributes):
        # self.init_user()
        response = self.request_create_tag(**attributes)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def request_create_tag(self, **attributes):
        tag = TagFactory.build(**attributes)
        return self.api_client.post(reverse(f"tags-list"), data=tag, format="json")
