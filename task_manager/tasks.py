import io
import time

from django.template.loader import render_to_string
from django.core import mail
from main.models import Task, User
from main.services.storage_backends import local_file_name, save_file
from task_manager.celery import app


@app.task
def send_assign_notification(task_id: int) -> None:
    task = Task.objects.get(pk=task_id)
    assignee = User.objects.get(pk=task.assignee.id)
    send_html_email(
        subject="You've assigned a task.",
        template="notification.html",
        context={"task": task},
        recipients=[assignee.email],
    )


@app.task
def send_html_email(
    subject: str, template: str, context: dict, recipients: list[str]
) -> None:
    html_message = render_to_string(f"emails/{template}", context)
    return mail.send_mail(
        subject=subject,
        message="",
        from_email=None,
        recipient_list=recipients,
        html_message=html_message,
    )


@app.task
def countdown(seconds: int) -> str:
    time.sleep(seconds)
    result_data = io.BytesIO(b"test data")
    file_name = local_file_name("test_report", countdown.request, "data")
    return save_file(file_name, result_data)