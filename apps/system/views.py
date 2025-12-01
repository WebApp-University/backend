from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import SystemInfoService
from .serializers import LoadSerializer


class StatusCPUView(APIView):

    def get(self, request):

        try:
            system_info_service = SystemInfoService()
            load_data = system_info_service.get_server_load()
            serializer = LoadSerializer(load_data)

            return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    'status': 'ERROR',
                    'notification': str(e)
                },
                status = status.HTTP_400_BAD_REQUEST
            )
