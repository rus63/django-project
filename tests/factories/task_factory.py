from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from main.models import Task


class TaskFactory(DjangoModelFactory):
    header = Faker("sentence")
    description = Faker("sentence")

    class Meta:
        model = Task
