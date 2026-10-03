from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Equipment, Booking
from sklearn.cluster import KMeans
import numpy as np
from datetime import date, timedelta

def map_view(request):
    # CRITICAL FIX: 'id' is added here so the map buttons know exactly which item to rent
    equipments = list(Equipment.objects.filter(is_available=True).values(
        'id', 'name', 'category', 'price_per_day', 'latitude', 'longitude'
    ))

    # Clustering Logic to identify Hotspots
    hotspots = []
    if len(equipments) >= 3:
        coords = np.array([[eq['latitude'], eq['longitude']] for eq in equipments])
        kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)
        kmeans.fit(coords)
        for center in kmeans.cluster_centers_:
            hotspots.append({'lat': center[0], 'lng': center[1]})

    return render(request, 'core/map.html', {
        'equipments': equipments,
        'hotspots': hotspots
    })

@login_required(login_url='/admin/login/')
def dashboard_view(request):
    if request.method == 'POST':
        Equipment.objects.create(
            owner=request.user,
            name=request.POST.get('name'),
            category=request.POST.get('category'),
            price_per_day=request.POST.get('price'),
            latitude=request.POST.get('latitude'),
            longitude=request.POST.get('longitude'),
            is_available=True
        )
        return redirect('dashboard')

    my_equipment = Equipment.objects.filter(owner=request.user).order_by('-id')
    my_bookings = Booking.objects.filter(renter=request.user).order_by('-id')
    
    return render(request, 'core/dashboard.html', {
        'my_equipment': my_equipment,
        'my_bookings': my_bookings
    })

@login_required(login_url='/admin/login/')
def rent_equipment(request, eq_id):
    equipment = get_object_or_404(Equipment, id=eq_id)

    if request.method == 'POST':
        days = int(request.POST.get('days'))
        start_date = date.today()
        end_date = start_date + timedelta(days=days)
        total_price = equipment.price_per_day * days

        # Create the booking and tie it to the user
        Booking.objects.create(
            renter=request.user,
            equipment=equipment,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            status='Confirmed'
        )

        # Remove the equipment from the map
        equipment.is_available = False
        equipment.save()
        return redirect('dashboard')

    return render(request, 'core/rent.html', {'equipment': equipment})