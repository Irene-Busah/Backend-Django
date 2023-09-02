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
    print(overdue_tasks)

    for task in overdue_tasks:
        user_email = task.user.email if task.user else None
        if user_email:
            send_mail(
                subject='Task Reminder',
                message=f'Reminder: Your task "{task.title}" is overdue!',
                from_email='busahirene123@gmail.com',  # Sender's email address
                recipient_list=[user_email],  # Recipient's email address
                fail_silently=True,
            )
        task.complete = True
        task.save()
    return "Done"