from rest_framework import serializers
from .models import Task


class TaskCreateSerializer(serializers.Serializer):

    input_data = serializers.DictField()

    def validate_input_data(self, value):
        A = value.get("A")
        B = value.get("B")

        if A is None or B is None:
            raise serializers.ValidationError("input_data must contain 'A' and 'B' matrices")

        def validate_matrix(M, name):
            if not all(isinstance(row, list) for row in M):
                raise serializers.ValidationError(f"{name} must be list[list]")

            row_lens = [len(r) for r in M]

            if any(l == 0 for l in row_lens):
                raise serializers.ValidationError(f"{name} rows must be non-empty")

            if len(set(row_lens)) != 1:
                raise serializers.ValidationError(f"{name} rows length mismatch")

        validate_matrix(A, "A")
        validate_matrix(B, "B")

        if len(A[0]) != len(B):
            raise serializers.ValidationError("A columns must equal B rows")

        return value


class TaskListSerializer(serializers.ModelSerializer):

    class Meta:

        model = Task
        fields = (
            "id",
            "status",
            "progress",
            "created_at",
            "started_at",
            "finished_at",
            "server_name",
            "input_data",
            "output_data",
        )
