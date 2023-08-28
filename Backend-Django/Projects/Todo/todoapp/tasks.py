# tasks.py

from celery import shared_task
from datetime import datetime
from django.utils import timezone
from django.core.mail import send_mail
from .models import Task

@shared_task
def send_task_reminders():
    now = timezone.now()
    overdue_tasks = Task.objects.filter(completion_time__lte=now, complete=False)

    for task in overdue_tasks:
        user_email = task.user.email if task.user else None
        if user_email:
            send_mail(
                'Task Reminder',
                f'Reminder: Your task "{task.title}" is overdue!',
                'your_email@example.com',  # Sender's email address
                [user_email],  # Recipient's email address
                fail_silently=False,
            )
        task.complete = True
        task.save()
