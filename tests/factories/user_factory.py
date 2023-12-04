from factory import PostGenerationMethodCall, Faker
from factory.django import DjangoModelFactory

from main.models import User
from tests.factories.base import ImageFileProvider

Faker.add_provider(ImageFileProvider)


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    password = "password"
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    avatar_picture = Faker("image_file", fmt="jpeg")
    role = Faker("random_element", elements=User.Roles.values)

    class Meta:
        model = dict
