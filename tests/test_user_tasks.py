from http import HTTPStatus

from main.models import User, Task
from tests.base import TestViewSetBase


class TestUserTasksViewSet(TestViewSetBase):
    basename = "user_tasks"

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

    def setUp(self) -> None:
        self.user1 = self.action_client.create_user()
        self.user2 = self.action_client.create_user()
        self.set_token(User.objects.get(pk=self.user1["id"]))
        self.tag = self.action_client.create_tag(header="Some tag")

    def test_list(self) -> None:
        task1 = self.action_client.create_task(assignee=self.user1["id"], author=self.user1["id"], tags=[self.tag["id"]])
        self.action_client.create_task(assignee=self.user2["id"], author=self.user2["id"], tags=[self.tag["id"]])

        tasks = self.list(args=[self.user1["id"]])

        assert tasks == [task1]

    def test_retrieve_foreign_task(self) -> None:
        user = self.action_client.create_user()
        tag = self.action_client.create_tag(header="Some tag")
        task = self.action_client.create_task(assignee=self.user1["id"], author=self.user1["id"], tags=[tag["id"]])

        response = self.client.get(self.detail_url(task["id"], user["id"]))

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_retrieve(self) -> None:
        created_task = self.action_client.create_task(assignee=self.user1["id"], author=self.user1["id"], tags=[self.tag["id"]])
        response = self.client.get(self.detail_url(created_task["id"], self.user1["id"]))
        assert response.status_code == HTTPStatus.OK, response.content

        retrieved_task = response.data

        assert created_task == retrieved_task
