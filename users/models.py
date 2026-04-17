from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('producer', 'Productor'),
        ('transporter', 'Transportista'),
        ('consumer', 'Consumidor'),
        ('admin', 'Administrador'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='consumer')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

class ProducerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='producer_profile')
    farm_name = models.CharField(max_length=200, blank=True)
    farm_location = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'producer_profiles'

class TransporterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='transporter_profile')
    vehicle_type = models.CharField(max_length=100, blank=True)
    vehicle_plate = models.CharField(max_length=20, blank=True)
    capacity_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    available = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'transporter_profiles'