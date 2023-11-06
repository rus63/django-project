from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from main.models import Task
from tests.factories.user_factory import UserFactory


class TaskFactory(DjangoModelFactory):
    header = Faker("sentence")
    description = Faker("sentence")
    author = SubFactory(UserFactory)
    assignee = SubFactory(UserFactory)

    class Meta:
        model = Task
