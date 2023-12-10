from factory import Faker
from factory.django import DjangoModelFactory


class TagFactory(DjangoModelFactory):
    header = Faker("sentence", )

    class Meta:
        model = dict
