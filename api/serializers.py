from rest_framework import serializers 
from api.models import Organization, Client

class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
  clients = serializers.HyperlinkedRelatedField( 
    many=True, 
    read_only=True, 
    view_name='client-detail') 
  class Meta: 
    model = Organization 
    fields = ('id',  
              'name',  
              'logo_url',
              'clients',
              'created_at')

class ClientSerializer(serializers.HyperlinkedModelSerializer):
  organization = serializers.SlugRelatedField(queryset=Organization.objects.all(), slug_field='name')

  class Meta: 
    model = Client 
    fields = ( 
        'id', 
        'name', 
        'uid', 
        'auth0_uid', 
        'organization', 
        'created_at')
