# celery.py

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')

app = Celery('todo')

# Add the imports setting to specify the location of your tasks.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.imports = ('todoapp.tasks',)  # Replace 'todoapp' with the actual app name

app.autodiscover_tasks()

