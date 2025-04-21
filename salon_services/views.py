from django.shortcuts import render

def services_main(request):
    return render(request, 'salon_services/services.html')

def hair_services(request):
    return render(request, 'salon_services/hair_services.html')

def skin_services(request):
    return render(request, 'salon_services/skin_services.html')

def body_services(request):
    return render(request, 'salon_services/body_services.html')

def nail_services(request):
    return render(request, 'salon_services/nail_services.html')

def bridal_services(request):
    return render(request, 'salon_services/bridal_services.html')

