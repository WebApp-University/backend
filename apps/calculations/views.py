from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import HasValidToken
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskCreateSerializer, TaskListSerializer
from . import services
from django.utils import timezone
from apps.calculations.models import User


def get_request_user_or_raise(request, data=None):
    user = getattr(request, "user", None)

    if user and getattr(user, "id", None):
        return user

    if data and "user_id" in data:
        return get_object_or_404(User, id = data["user_id"])

    return None


class CreateTaskView(APIView):
    permission_classes = [HasValidToken]
    MAX_ACTIVE_TASKS = 5

    def post(self, request):
        serializer = TaskCreateSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        input_data = serializer.validated_data["input_data"]

        user = get_request_user_or_raise(request, request.data)
        if user is None:
            return Response({"detail": "Authentication required"}, status=401)


        active_tasks = Task.objects.filter(
            user_id=user.id,
            status__in=["pending", "processing"]
        ).count()

        if active_tasks >= self.MAX_ACTIVE_TASKS:
            return Response(
                {"detail": f"Maximum number of active tasks ({self.MAX_ACTIVE_TASKS}) reached."},
                status=status.HTTP_400_BAD_REQUEST
            )

        task = Task(
            user_id=user.id,
            input_data=input_data,
            status="pending",
            progress=0,
            created_at=timezone.now()
        )
        task.save()

        services.submit_matrix_task(task.id)

        return Response({"task_id": task.id}, status=201)


class MyTasksView(APIView):
    permission_classes = [HasValidToken]

    def get(self, request):
        user = get_request_user_or_raise(request)
        tasks = Task.objects.filter(user_id=user.id).order_by("-created_at")
        return Response(TaskListSerializer(tasks, many=True).data)


class TaskDetailView(APIView):
    permission_classes = [HasValidToken]

    def get(self, request, pk):
        user = get_request_user_or_raise(request)
        task = get_object_or_404(Task, id=pk, user_id=user.id)
        return Response(TaskListSerializer(task).data)


class CancelTaskView(APIView):
    permission_classes = [HasValidToken]

    def post(self, request, pk):
        user = get_request_user_or_raise(request)
        task = get_object_or_404(Task, id=pk, user_id=user.id)

        ok = services.cancel_task(task.id)
        if ok:
            return Response({"detail": "cancelled"})

        return Response({"detail": "unable to cancel"}, status=400)
