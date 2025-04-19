

# Create your views here.
from django.shortcuts import render

def homepage(request):
    return render(request, 'core/homepage.html')


def services(request):
    service_data = {
        "Hair": [
            {"name": "Hair Cut", "price": 1500, "image_url": "/static/images/haircut.jpg"},
            {"name": "Hair Color", "price": 3000, "image_url": "/static/images/haircolor.jpg"},
            # Add more services here
        ],
        "Skin": [
            {"name": "Facial", "price": 3500, "image_url": "/static/images/facial.jpg"},
            {"name": "Cleanup", "price": 2000, "image_url": "/static/images/cleanup.jpg"},
        ],
        "Body": [
            {"name": "Body Massage", "price": 4000, "image_url": "/static/images/massage.jpg"},
        ],
        "Nails": [
            {"name": "Manicure", "price": 2500, "image_url": "/static/images/manicure.jpg"},
            {"name": "Pedicure", "price": 2700, "image_url": "/static/images/pedicure.jpg"},
        ],
        "Bridal": [
            {"name": "Bridal Makeup", "price": 8000, "image_url": "/static/images/bridal.jpg"},
        ],
    }

    return render(request, 'core/services.html', {'service_data': service_data})

