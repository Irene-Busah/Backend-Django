# Django To-Do Application

This Django To-Do application allows users to create, manage, and track tasks with due dates. It also sends email notifications for overdued tasks and edited tasks.

## Table of Contents
- Features
- Prerequisites
- Installation
- Configuration
- Usage


### Features
- User authentication and task management.
- Creation of tasks with titles, descriptions, and completion dates.
- Email notifications for overdued task, edited tasks and deletions.
- User-friendly web interface.
- Easily customizable for your own use.

### Prerequisites
Before you begin, ensure you have met the following requirements:

* Python 3.x installed on your machine.
* Django and Celery packages installed.
- A working email configuration (e.g., Gmail) for sending notifications.

### Installation
1. Clone this repository to your local machine:  
```
git clone https://github.com/Irene-Busah/Backend-Django/tree/main/Backend-Django/Projects/Todo 
cd Todo
```

2. Create a virtual environment (optional but recommended):  
```
python -m venv venv 
source venv/bin/activate # On Windows, use: venv\Scripts\activate
```

3. Install project dependencies:  
```
pip install -r requirements.txt
```

### Configuration
Email Configuration  
To configure email for sending notifications, update the Django settings in settings.py. For example, if you're using Gmail, you can add the following:  
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = 'yourpassword'
```

### Usage
1. Run database migrations:
```
python manage.py migrate
```

2. Start the Redis server. If you haven't already installed Redis, download and install it from the official website. After installation, you can start the server with:
```
redis-server.exe
```
Note: On Windows, you need to start Redis via CMD with administrative privileges

3. Start the Celery worker for background task processing:
```
celery -A todo.celery worker --pool=solo -l info
```

4. Open another terminal and start the Celery beat for background task scheduling:
```
celery -A todo beat -l info
```

5. Start the development server:
```
python manage.py runserver
```
Access the application in your web browser at http://localhost:8000/. 

