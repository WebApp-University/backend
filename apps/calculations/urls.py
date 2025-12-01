from django.urls import path
from .views import CreateTaskView, MyTasksView, TaskDetailView, CancelTaskView

urlpatterns = [
    path("tasks/", CreateTaskView.as_view(), name = "create_task"),
    path("tasks/my/", MyTasksView.as_view(), name = "my_tasks"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name = "task_detail"),
    path("tasks/<int:pk>/cancel/", CancelTaskView.as_view(), name = "task_cancel")
]
