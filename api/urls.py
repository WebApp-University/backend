from django.urls import path, include

urlpatterns = [
    path("authentific/", include("apps.authentific.urls")),
path("calculations/", include("apps.calculations.urls"))
]
