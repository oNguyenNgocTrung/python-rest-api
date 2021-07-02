from rest_framework.response import Response
from rest_framework import viewsets, renderers

class HealthCheckViewSet(viewsets.ViewSet):
  renderer_classes = [renderers.JSONRenderer]
  def list(self, request):
    data = { 'status': 'OK' }
    return Response(data)
