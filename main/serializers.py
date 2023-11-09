from django.core.files import File
from django.core.validators import FileExtensionValidator
from rest_framework.exceptions import ValidationError

from task_manager import settings
from .models import User, Task, Tag
from rest_framework import serializers


class FileMaxSizeValidator:
    def __init__(self, max_size: int) -> None:
        self.max_size = max_size

    def __call__(self, value: File) -> None:
        if value.size > self.max_size:
            raise ValidationError(f"Maximum size {self.max_size} exceeded.")


class UserSerializer(serializers.ModelSerializer):
    avatar_picture = serializers.FileField(
        required=False,
        validators=[
            FileMaxSizeValidator(settings.UPLOAD_MAX_SIZES["avatar_picture"]),
            FileExtensionValidator(["jpeg", "jpg", "png"]),
        ],
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "avatar_picture",
        )


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "header",
            "description",
            "date_of_creation",
            "date_of_changing",
            "deadline",
            "state",
            "priority",
            "tags",
            "author",
            "assignee",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "header")
