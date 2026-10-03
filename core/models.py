from django.db import models
from django.contrib.auth.models import User

class Equipment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='equipment_owned')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50) 
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    latitude = models.FloatField(default=0.0) 
    longitude = models.FloatField(default=0.0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.category}"

class Booking(models.Model):
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # <-- Add this line
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.equipment.name} booked by {self.renter.username}"