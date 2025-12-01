import psutil
from .models import Task

class SystemInfoService:

    def get_server_load(self):

        cpu = psutil.cpu_percent(interval=0.5)
        queued_tasks = Task.objects.filter(status__in=['pending', 'processing']).count()
        return {
            "cpu": cpu,
            "queued_tasks": queued_tasks
        }
