from django.shortcuts import render

def services_page(request):
    return render(request, 'salon_services/services.html')

