from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import loginView, registerView, dashboardView, cardDetailsView, categoryView

urlpatterns = [
    path("login/", loginView, name="login"),
    path("register/", registerView, name="register"),
    path("dashboard/", dashboardView, name="dashboard"),
    path("card-details/", cardDetailsView, name="card-details"),
    path("category/", categoryView, name="category"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
