from tests.base import TestViewSetBase


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = {
        'username': 'johnsmith',
        'first_name': 'John',
        'last_name': 'Smith',
        'email': 'john@test.com',
    }
    test_user_attributes = {
        'username': 'test_user',
        'first_name': 'TEST',
        'last_name': 'USER',
        'email': 'john@test.com',
    }

    # def test_create(self):
    #     response = self.create(data=self.test_user_attributes)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        # user = self.create(self.user_attributes)
        # expected_response = self.expected_details(user, self.user_attributes)
        # assert user == expected_response
        self.create(self.test_user_attributes)

    def test_list(self):
        self.client.force_login(self.user)
        self.create(self.test_user_attributes)
        response = self.list()
        print(response)
        expected_response = self.expected_details(response, self.user_attributes)
