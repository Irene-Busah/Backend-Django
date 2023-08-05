from django.contrib.auth.signals import user_logged_out
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Task

@receiver(user_logged_out)
def delete_completed_tasks(sender, request, user, **kwargs):
    # Delete completed tasks for the logged-out user
    Task.objects.filter(user=user, complete=True).delete()
