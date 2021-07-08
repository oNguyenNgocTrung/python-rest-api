# from django.http import HttpResponse 
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets, renderers, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from api.models import Organization, Client
from api.serializers import OrganizationSerializer, ClientSerializer

from functools import wraps
import jwt

class ApiRoot(generics.GenericAPIView): 
  name = 'api-root' 
  def get(self, request, *args, **kwargs): 
    return Response({ 
      'organizations': reverse(OrganizationList.name, request=request), 
      'clients': reverse(ClientList.name, request=request)
      })

class HealthCheckViewSet(viewsets.ViewSet):
  renderer_classes = [renderers.JSONRenderer]
  def list(self, request):
    data = { 'status': 'OK' }
    return Response(data)


class OrganizationList(generics.ListCreateAPIView): 
    queryset = Organization.objects.all() 
    serializer_class = OrganizationSerializer 
    name = 'organization-list'

class OrganizationDetail(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Organization.objects.all() 
    serializer_class = OrganizationSerializer 
    name = 'organization-detail' 

class ClientList(generics.ListCreateAPIView): 
    queryset = Client.objects.all() 
    serializer_class = ClientSerializer 
    name = 'client-list'

class ClientDetail(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Client.objects.all() 
    serializer_class = ClientSerializer 
    name = 'client-detail' 

# @api_view(['GET', 'POST']) 
# def organization_list(request):
#   if request.method == 'GET':
#     organizations = Organization.objects.all()
#     organizations_serializer = OrganizationSerializer(organizations, many=True)
#     return Response(organizations_serializer.data)
#   elif request.method == 'POST':
#     organizations_serializer = OrganizationSerializer(data=request.data)
#     if organizations_serializer.is_valid():
#       organizations_serializer.save()
#       return Response(organizations_serializer.data, status=status.HTTP_201_CREATED)

#     return Response(organizations_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE']) 
# def organization_detail(request, pk):
#   try: 
#     organization = Organization.objects.get(pk=pk) 
#   except Organization.DoesNotExist: 
#     return Response(status=status.HTTP_404_NOT_FOUND)

#   if request.method == 'GET':
#     organization_serializer = OrganizationSerializer(organization) 
#     return Response(organization_serializer.data)
#   elif request.method == 'PUT':
#     organization_serializer = OrganizationSerializer(organization, data=request.data)
#     if organization_serializer.is_valid():
#       organization_serializer.save()
#       return Response(organization_serializer.data)

#     return Response(organization_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#   elif request.method == 'DELETE':
#     organization.delete()
#     return HttpResponse(status=status.HTTP_204_NO_CONTENT)



def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token

def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            decoded = jwt.decode(token, verify=False)
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse({'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response
        return decorated
    return require_scope
