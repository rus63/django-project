import django_filters
from rest_framework import viewsets
from .models import User, Tag, Task
from .serializers import UserSerializer, TaskSerializer, TagSerializer


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("name",)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TaskFilter(django_filters.FilterSet):
    state = django_filters.CharFilter()
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())
    author = django_filters.CharFilter(
        field_name="author__last_name", lookup_expr="icontains"
    )
    assignee = django_filters.CharFilter(
        field_name="author__last_name", lookup_expr="icontains"
    )

    class Meta:
        model = Task
        fields = ("state", "tags", "author", "assignee")


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.select_related("author", "assignee")
        .prefetch_related("tags")
        .order_by("id")
    )
    serializer_class = TaskSerializer
    filterset_class = TaskFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
