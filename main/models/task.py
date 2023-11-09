from django.db import models
from .tag import Tag
from .user import User


class Task(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 1
        NORMAL = 2
        HIGH = 3

    class States(models.TextChoices):
        NEW_TASK = "new_task"
        IN_DEVELOPMENT = "in_development"
        IN_QA = "in_qa"
        IN_CODE_REVIEW = "in_code_review"
        READY_FOR_RELEASE = "ready_for_release"
        RELEASED = "released"
        ARCHIVED = "archived"

    header = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=300)
    date_of_creation = models.DateField(auto_now_add=True)
    date_of_changing = models.DateField(auto_now=True)
    deadline = models.DateField(null=True)
    state = models.CharField(choices=States.choices, default=States.NEW_TASK)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.LOW)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="author", null=True
    )
    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="assignee", null=True
    )

    def __str__(self) -> str:
        return self.header
