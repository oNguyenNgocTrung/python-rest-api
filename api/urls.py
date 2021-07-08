from django.urls import include, path
from django.conf.urls import url 
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'health_check', views.HealthCheckViewSet, basename='HealthCheck')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^organizations/$',  
      views.OrganizationList.as_view(),  
      name=views.OrganizationList.name), 
    url(r'^organizations/(?P<pk>[0-9]+)$',  
      views.OrganizationDetail.as_view(), 
      name=views.OrganizationDetail.name),
    url(r'^clients/$',  
      views.ClientList.as_view(),  
      name=views.ClientList.name), 
    url(r'^clients/(?P<pk>[0-9]+)$',  
      views.ClientDetail.as_view(), 
      name=views.ClientDetail.name), 
]
