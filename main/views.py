from typing import cast, Any

import django_filters
from django.http import Http404, HttpResponse
from django.urls import reverse
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from .models import User, Tag, Task
from .permissions import DeleteStaffOnly
from .serializers import UserSerializer, TaskSerializer, TagSerializer, CountdownJobSerializer, JobSerializer
from main.services.single_resource import SingleResourceMixin, SingleResourceUpdateMixin
from .services.async_celery import AsyncJob, JobStatus


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
    permission_classes = [DeleteStaffOnly, IsAuthenticated]
    # permission_classes = (AllowAny,)



class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
    permission_classes = (DeleteStaffOnly, IsAuthenticated)


class CurrentUserViewSet(
    SingleResourceMixin, SingleResourceUpdateMixin, viewsets.ModelViewSet
):
    serializer_class = UserSerializer
    queryset = User.objects.order_by("id")

    def get_object(self) -> User:
        return cast(User, self.request.user)


class UserTasksViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = (
        Task.objects.order_by("id")
        .select_related("author", "assignee")
        .prefetch_related("tags")
    )
    serializer_class = TaskSerializer


class TaskTagsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        task_id = self.kwargs["parent_lookup_task_id"]
        return Task.objects.get(pk=task_id).tags.all()


class CountdownJobViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CountdownJobSerializer

    def get_success_headers(self, data: dict) -> dict[str, str]:
        task_id = data["task_id"]
        return {"Location": reverse("jobs-detail", args=[task_id])}


class AsyncJobViewSet(viewsets.GenericViewSet):
    serializer_class = JobSerializer

    def get_object(self) -> AsyncJob:
        lookup_url_kwargs = self.lookup_url_kwarg or self.lookup_field
        task_id = self.kwargs[lookup_url_kwargs]
        job = AsyncJob.from_id(task_id)
        if job.status == JobStatus.UNKNOWN:
            raise Http404()
        return job

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse:
        instance = self.get_object()
        serializer_data = self.get_serializer(instance).data
        if instance.status == JobStatus.SUCCESS:
            location = self.request.build_absolute_uri(instance.result)
            return Response(
                serializer_data,
                headers={"location": location},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer_data)
