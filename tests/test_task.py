from datetime import date

from main.models import Task, User, Tag
from tests.base import TestViewSetBase


class TestTasksViewSet(TestViewSetBase):
    basename = "tasks"
    test_task_attributes = {
        "header": "Test task",
        "description": "Description of test task",
        "date_of_creation": date.today().strftime("%Y-%m-%d"),
        "date_of_changing": date.today().strftime("%Y-%m-%d"),
        "deadline": date(2023, 5, 1).strftime("%Y-%m-%d"),
        "state": "in_development",
        "priority": 2,
    }

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.author = User.objects.create_user(
            username="task_author", password="password", role="developer", is_staff=True
        )
        cls.assignee = User.objects.create_user(
            username="task_assignee", password="password", role="developer"
        )
        cls.tag = Tag.objects.create(header="ready")

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        return {
            **attributes,
            "id": entity["id"],
            "author": entity["author"],
            "assignee": entity["assignee"],
            "tags": entity["tags"],
        }

    def test_create(self) -> None:
        self.client.force_login(self.author)

        self.task_attr = {
            **self.test_task_attributes,
            "author": self.author.id,
            "assignee": self.assignee.id,
            "tags": self.tag.id,
        }
        response_data = self.create(self.task_attr)
        expected_response = self.expected_details(
            response_data, self.test_task_attributes
        )

        assert response_data == expected_response

    def test_list(self) -> None:
        self.client.force_login(self.author)
        Task.objects.create(
            author=self.author,
            assignee=self.assignee,
            **self.test_task_attributes,
        )
        response = self.list()[0]
        expected_response = self.expected_details(response, self.test_task_attributes)

        assert response == expected_response

    def test_retrieve(self) -> None:
        self.client.force_login(self.author)
        task = Task.objects.create(
            author=self.author,
            assignee=self.assignee,
            **self.test_task_attributes,
        )
        response = self.retrieve(task.id)
        expected_response = self.expected_details(response, self.test_task_attributes)

        assert response == expected_response

    def test_delete(self) -> None:
        self.client.force_login(self.author)
        task = Task.objects.create(
            author=self.author,
            assignee=self.assignee,
            **self.test_task_attributes,
        )

        self.delete(task.id)
