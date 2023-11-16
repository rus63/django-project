import factory
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import Task, User, Tag
from tests.base import TestViewSetBase


class TestTagsViewSet(TestViewSetBase):
    basename = "tags"
    test_tag_attributes = {
        "header": "Test tag",
    }

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.tag_author = User.objects.create_user(
            username="tag_author", password="password", role="developer", is_staff=True
        )

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        return {
            **attributes,
            "id": entity["id"],
        }

    def test_create(self) -> None:
        self.set_token(self.tag_author)

        self.client.force_login(self.tag_author)
        self.tag_attr = {**self.test_tag_attributes}
        response_data = self.create(self.tag_attr)
        expected_response = self.expected_details(
            response_data, self.test_tag_attributes
        )

        assert response_data == expected_response

    def test_list(self) -> None:
        self.set_token(self.tag_author)
        self.client.force_login(self.tag_author)
        Tag.objects.create(**self.test_tag_attributes)
        response = self.list()[0]
        expected_response = self.expected_details(response, self.test_tag_attributes)

        assert response == expected_response

    def test_retrieve(self) -> None:
        self.set_token(self.tag_author)
        self.client.force_login(self.tag_author)
        tag = Tag.objects.create(**self.test_tag_attributes)
        response = self.retrieve(tag.id)
        expected_response = self.expected_details(response, self.test_tag_attributes)

        assert response == expected_response

    def test_delete(self) -> None:
        self.set_token(self.tag_author)
        self.client.force_login(self.tag_author)
        tag = Tag.objects.create(**self.test_tag_attributes)

        self.delete(tag.id)
