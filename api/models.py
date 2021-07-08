from django.db import models

# Create your models here.
class Organization(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  name = models.CharField(max_length=150, blank=False, unique=True)
  logo_url = models.URLField()

  def __str__(self):
    return self.name

class Client(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  name = models.CharField(max_length=150, blank=False, unique=True)
  uid = models.CharField(max_length=100, blank=False, unique=True)
  auth0_uid = models.CharField(max_length=100, blank=False, unique=True)
  organization = models.ForeignKey(Organization,related_name='clients', on_delete=models.CASCADE)

  def __str__(self):
    return self.name
