import threading
from concurrent.futures import ThreadPoolExecutor
from django.utils import timezone
from .models import Task
import traceback
import os


EXECUTOR = ThreadPoolExecutor(max_workers = 4)
cancellation_events = {}
SERVER_NAME = os.getenv("SERVER_NAME", "server")


def multiply_matrices_with_progress(task_id):

    try:

        task = Task.objects.get(id=task_id)
        task.status = "processing"
        task.started_at = timezone.now()
        task.server_name = SERVER_NAME
        task.progress = 0
        task.save(update_fields = ["status", "started_at", "server_name", "progress"])

        evt = cancellation_events.get(task_id)
        input_data = task.input_data

        A = input_data["A"]
        B = input_data["B"]

        rows_A = len(A)
        cols_A = len(A[0])
        cols_B = len(B[0])

        result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

        total_rows = rows_A

        for i in range(rows_A):
            if evt and evt.is_set():

                task.status = "cancelled"
                task.finished_at = timezone.now()
                task.save(update_fields = ["status", "finished_at"])
                return

            rowA = A[i]

            for k in range(cols_A):

                aik = rowA[k]
                rowBk = [B[k][j] for j in range(cols_B)]

                for j in range(cols_B):
                    result[i][j] += aik * rowBk[j]


            percent = int((i+1) / total_rows * 100)
            task.progress = percent
            task.save(update_fields = ["progress"])

        task.output_data = {"result": result}
        task.status = "completed"
        task.progress = 100
        task.finished_at = timezone.now()
        task.save(update_fields = ["output_data", "status","progress", "finished_at"])

    except Exception as e:

        traceback.print_exc()

        try:
            task = Task.objects.get(id=task_id)
            task.status = "failed"
            task.finished_at = timezone.now()
            task.save(update_fields = ["status","finished_at"])

        except Exception:
            pass


def submit_matrix_task(task_id):

    cancellation_events[task_id] = threading.Event()
    future = EXECUTOR.submit(multiply_matrices_with_progress, task_id)

    def _cleanup(fut):
        cancellation_events.pop(task_id, None)

    future.add_done_callback(_cleanup)
    return future


def cancel_task(task_id):
    evt = cancellation_events.get(task_id)

    if evt:
        evt.set()
        return True

    try:
        task = Task.objects.get(id = task_id)
        if task.status in ("pending","processing"):
            task.status = "cancelled"
            task.finished_at = timezone.now()
            task.save(update_fields = ["status","finished_at"])

            return True

    except Task.DoesNotExist:
        pass

    return False
