from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Task, User


class TestDelete(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.staff_user = User.objects.create_user(
            username="test_staff_user", password="password", is_staff=True
        )
        cls.non_staff_user = User.objects.create_user(
            username="test_non_staff_user", password="password"
        )

        cls.task = Task.objects.create(header="Task1", author=cls.staff_user)

    def test_delete_by_staff(self) -> None:
        self.client.login(username="test_staff_user", password="password")
        response = self.client.delete(f"/api/tasks/{self.task.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_by_non_staff(self) -> None:
        self.client.login(username="test_non_staff_user", password="password")
        response = self.client.delete(f"/api/tasks/{self.task.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN
