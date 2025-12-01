from rest_framework import serializers


class LoadSerializer(serializers.Serializer):
    cpu = serializers.FloatField()
    queued_tasks = serializers.IntegerField()
