from rest_framework.response import Response
from rest_framework import viewsets, status

class HealthCheckViewSet(viewsets.ViewSet):
  def list(self, request):
    return Response(data={}, status=status.HTTP_200_OK)