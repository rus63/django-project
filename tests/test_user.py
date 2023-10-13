from tests.base import TestViewSetBase


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    test_user_attributes = {
        "username": "test_user",
        "first_name": "TEST",
        "last_name": "USER",
        "email": "john@test.com",
    }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self) -> None:
        self.client.force_login(self.user)

        self.create(self.test_user_attributes)

    def test_list(self) -> None:
        self.client.force_login(self.user)

        response = self.list()[0]
        expected_response = self.expected_details(response, self.user_attributes)

        assert response == expected_response

    def test_retrieve(self) -> None:
        self.client.force_login(self.user)

        response = self.retrieve(self.user.id)
        expected_response = self.expected_details(response, self.user_attributes)

        assert response == expected_response

    def test_delete(self) -> None:
        self.client.force_login(self.user)
        self.delete(self.user.id)
