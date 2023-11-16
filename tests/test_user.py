from http import HTTPStatus

from django.core.files.uploadedfile import SimpleUploadedFile

from tests.base import TestViewSetBase
from tests.factories.user_factory import UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    test_user_attributes = UserFactory.build()

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        attributes.pop("password")
        return {**attributes, "id": entity["id"], "avatar_picture": entity["avatar_picture"]}

    def test_create(self) -> None:
        self.set_token(self.user)
        self.client.force_login(self.user)

        self.create(self.test_user_attributes)

    def test_list(self) -> None:
        self.set_token(self.user)
        self.client.force_login(self.user)

        response = self.list()[0]
        expected_response = self.expected_details(response, self.user_attributes)

        assert response == expected_response

    def test_retrieve(self) -> None:
        self.set_token(self.user)
        self.client.force_login(self.user)

        response = self.retrieve(self.user.id)
        expected_response = self.expected_details(response, self.user_attributes)

        assert response == expected_response

    def test_delete(self) -> None:
        self.set_token(self.user)
        self.client.force_login(self.user)
        self.delete(self.user.id)

    def test_large_avatar(self) -> None:
        self.set_token(self.user)
        user_attributes = UserFactory.build(
            avatar_picture=SimpleUploadedFile("large.jpg", b"x" * 2 * 1024 * 1024)
        )
        response = self.client.post(self.list_url(), user_attributes)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"avatar_picture": ["Maximum size 1048576 exceeded."]}

    def test_avatar_bad_extension(self) -> None:
        self.set_token(self.user)
        user_attributes = UserFactory.build()
        user_attributes["avatar_picture"].name = "bad_extension.pdf"
        response = self.client.post(self.list_url(), user_attributes)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "avatar_picture": [
                "File extension “pdf” is not allowed. Allowed extensions are: jpeg, jpg, png."
            ]
        }
