import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_rental.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Equipment

def populate_data():
    print("Clearing old equipment data...")
    Equipment.objects.all().delete() # This removes the old Nandikotkur pins

    print("Fetching users...")
    users = list(User.objects.all())

    print("Creating dummy equipment around Nandyal...")
    categories = ['Tractor', 'Harvester', 'Sprayer', 'Rotavator']
    brands = ['Mahindra', 'John Deere', 'Swaraj', 'Massey Ferguson', 'Tafe']

    # Base coordinates for Nandyal
    base_lat = 15.48
    base_lon = 78.48

    for i in range(50):
        owner = random.choice(users)
        category = random.choice(categories)
        brand = random.choice(brands)
        name = f"{brand} {category}"
        price = random.randint(1000, 5000)
        
        # Scatter across villages around Nandyal
        lat = base_lat + random.uniform(-0.15, 0.15)
        lon = base_lon + random.uniform(-0.15, 0.15)

        Equipment.objects.create(
            owner=owner,
            name=name,
            category=category,
            price_per_day=price,
            latitude=lat,
            longitude=lon,
            is_available=True
        )
    print("Successfully added 50 equipment listings near Nandyal!")

if __name__ == '__main__':
    populate_data()