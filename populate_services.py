import os
import django
from datetime import timedelta

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from booking.models import ServiceCategory, ServiceSubCategory, Service

DATA = {
    "Hair Services": {
        "Haircuts": [
            ("Ladies Haircut (Short)", 2000, 30),
            ("Ladies Haircut (Medium)", 2500, 45),
            ("Ladies Haircut (Long)", 3000, 60),
            ("Gents Haircut", 1800, 30),
            ("Kids Haircut (Under 12)", 1200, 30),
        ],
        "Blow Dry & Styling": [
            ("Blow Dry (Short)", 2000, 45),
            ("Blow Dry (Long)", 2800, 60),
            ("Ironing (Per Section)", 1200, 30),
            ("Curling (Full Hair)", 2500, 45),
        ],
        "Hair Spa": [
            ("Classic Hair Spa (Short)", 3000, 60),
            ("Botox Hair Spa (Medium)", 5000, 75),
            ("Moroccan Hair Spa (Long)", 7000, 90),
        ],
        "Straightening & Rebonding": [
            ("Permanent Straightening (Short)", 9000, 60),
            ("Permanent Straightening (Long)", 15000, 90),
            ("Rebonding (Medium)", 13500, 80),
        ],
        "Advanced Hair Treatments": [
            ("Keratin Treatment – Short", 22000, 60),
            ("Keratin Treatment – Long", 30000, 90),
            ("Cysteine Treatment", 25000, 80),
        ],
        "Add-On Services": [
            ("Hair Wash Only", 1000, 10),
            ("Scalp Massage (15 min)", 2000, 15),
            ("Hair Serum Application", 800, 15),
        ]
    },
    "Skin Services": {
        "Facials": [
            ("Classic Cleanup", 2500, 60),
            ("Skin Glow Facial", 4000, 90),
            ("Vitamin C Facial", 6000, 90),
            ("Hydra Facial", 7500, 120),
        ],
        "Threading & Waxing": [
            ("Eyebrows Threading", 300, 15),
            ("Full Face Wax", 1800, 30),
            ("Full Arms Wax", 4500, 45),
            ("Full Legs Wax", 6000, 60),
        ],
        "Detan & Bleach": [
            ("Face & Neck Detan", 3000, 45),
            ("Full Body Detan", 8000, 90),
            ("Face Bleach", 2000, 30),
        ],
        "Add-On Services": [
            ("Lip Lightening Treatment", 1200, 20),
            ("Under Eye Treatment", 1800, 25),
        ]
    },
    "Body Services": {
        "Massages": [
            ("Full Body Massage (60 min)", 12000, 60),
            ("Shoulder Massage (30 min)", 4500, 30),
            ("Foot Massage (60 min)", 6500, 60),
        ],
        "Body Treatments": [
            ("Classic Body Scrub", 8500, 45),
            ("Body Polish", 14500, 90),
            ("Underarm Treatment", 7000, 30),
        ]
    },
    "Nail Services": {
        "Manicure & Pedicure": [
            ("Classic Manicure", 2800, 30),
            ("Spa Pedicure", 5500, 45),
            ("Hydrating Pedicure with Gel Color", 6800, 60),
        ],
        "Nail Extensions & Art": [
            ("Gel Full Set (Hands)", 9000, 90),
            ("Acrylic Full Set with Gel Color", 9500, 120),
            ("Nail Art (Per Nail)", 250, 15),
        ]
    },
    "Bridal Services": {
        "Bridal Packages": [
            ("Bridal Makeup & Hair Styling", 25000, 180, True),
            ("Pre-Bridal Skin & Hair Care Package", 20000, 240, True),
        ],
        "Additional Services": [
            ("Saree Draping", 3000, 30),
            ("Mehendi Application (Per Hand)", 2000, 30),
        ]
    }
}

# Create or retrieve each category, then subcategories, then services
display_order = 1
for cat_name, subcategories in DATA.items():
    category, _ = ServiceCategory.objects.update_or_create(
        name=cat_name,
        defaults={'display_order': display_order}
    )
    display_order += 1

    sub_display_order = 1
    for sub_name, services in subcategories.items():
        subcategory, _ = ServiceSubCategory.objects.update_or_create(
            category=category,
            name=sub_name,
            defaults={'display_order': sub_display_order}
        )
        sub_display_order += 1

        for service_data in services:
            service_name = service_data[0]
            price = service_data[1]
            duration = service_data[2]
            is_special = service_data[3] if len(service_data) > 3 else False

            Service.objects.update_or_create(
                subcategory=subcategory,
                name=service_name,
                defaults={
                    'price': price,
                    'duration_minutes': duration,
                    'is_special': is_special,
                    'available': True
                }
            )

print("✔️ All sample data populated successfully.")

