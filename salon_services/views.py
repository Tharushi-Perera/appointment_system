from django.shortcuts import render

#def services_page(request):
#    return render(request, 'salon_services/services.html')


def services_page(request):
    service_data = {
        "Hair": [
            {"name": "Haircut", "price": 1200},
            {"name": "Hair Coloring", "price": 2500},
        ],
        "Face": [
            {"name": "Facial Treatment", "price": 2000},
            {"name": "Makeup", "price": 3000},
        ],
        "Nails": [
            {"name": "Manicure", "price": 1500},
            {"name": "Pedicure", "price": 1800},
        ],
    }
    return render(request, 'salon_services/services.html', {"service_data": service_data})
