from django.db import models
from django.utils import timezone


class User(models.Model):

    id = models.BigAutoField(primary_key = True)
    username = models.TextField(unique = True)
    email = models.TextField(unique = True)
    password = models.TextField()


    class Meta:
        db_table = 'users'
        managed = False



class Task(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]


    id = models.BigAutoField(primary_key = True)
    user = models.ForeignKey("User", on_delete = models.CASCADE, related_name = "tasks")

    input_data = models.JSONField()
    output_data = models.JSONField(null = True, blank = True)

    status = models.CharField(max_length = 20, choices = STATUS_CHOICES, default = "pending")

    progress = models.IntegerField(default = 0)

    created_at = models.DateTimeField(default = timezone.now)
    started_at = models.DateTimeField(null = True, blank = True)
    finished_at = models.DateTimeField(null = True, blank = True)

    server_name = models.CharField(max_length = 100, null = True, blank = True)

    class Meta:
        db_table = 'tasks'
        managed = False

    def __str__(self):
        return f"Task {self.id} ({self.status})"