from tests.base import TestViewSetBase


class TestUserViewSet(TestViewSetBase):
    basename = "current_user"

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

    def test_retrieve(self):
        self.set_token(self.user)
        user = self.single_resource()

        assert user == {
            'id': self.user.id,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'role': self.user.role,
            'username': self.user.username,
            'avatar_picture': f"http://testserver{self.user.avatar_picture.url}"
        }

    def test_patch(self):
        self.set_token(self.user)
        self.patch_single_resource({"first_name": "TestName"})

        user = self.single_resource()
        assert user["first_name"] == "TestName"
