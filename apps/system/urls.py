from django.urls import path
from .views import StatusCPUView


urlpatterns = [
    path('load/', StatusCPUView.as_view(), name = 'load_system_status_data'),
]
