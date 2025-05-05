from django.db import migrations

def load_initial_data(apps, schema_editor):
    ServiceCategory = apps.get_model('booking', 'ServiceCategory')
    ServiceSubCategory = apps.get_model('booking', 'ServiceSubCategory')
    Service = apps.get_model('booking', 'Service')

    # 1. Hair Services
    hair = ServiceCategory.objects.create(name="Hair Services", display_order=1)

    # Haircuts
    haircuts = ServiceSubCategory.objects.create(category=hair, name="Haircuts", display_order=1)
    Service.objects.create(subcategory=haircuts, name="Ladies Haircut (Short)", price=2000, duration_minutes=30)
    Service.objects.create(subcategory=haircuts, name="Ladies Haircut (Medium)", price=2500, duration_minutes=45)
    Service.objects.create(subcategory=haircuts, name="Ladies Haircut (Long)", price=3000, duration_minutes=60)
    Service.objects.create(subcategory=haircuts, name="Gents Haircut", price=1800, duration_minutes=30)
    Service.objects.create(subcategory=haircuts, name="Kids Haircut (Under 12)", price=1200, duration_minutes=30)

    # Blow Dry & Styling
    blow_dry = ServiceSubCategory.objects.create(category=hair, name="Blow Dry & Styling", display_order=2)
    Service.objects.create(subcategory=blow_dry, name="Blow Dry (Short)", price=2000, duration_minutes=45)
    Service.objects.create(subcategory=blow_dry, name="Blow Dry (Long)", price=2800, duration_minutes=60)
    Service.objects.create(subcategory=blow_dry, name="Ironing(Per Section)", price=1200, duration_minutes=30)
    Service.objects.create(subcategory=blow_dry, name="Curling (Full Hair)", price=2500, duration_minutes=45)

    # Hair Spa
    hair_spa = ServiceSubCategory.objects.create(category=hair, name="Hair Spa", display_order=3)
    Service.objects.create(subcategory=hair_spa, name="Classic Hair Spa (Short)", price=3000, duration_minutes=60)
    Service.objects.create(subcategory=hair_spa, name="Botox Hair Spa (Medium)", price=5000, duration_minutes=75)
    Service.objects.create(subcategory=hair_spa, name="Moroccan Hair Spa (Long)", price=7000, duration_minutes=90)

    #Straightening & Rebonding
    straightening = ServiceSubCategory.objects.create(category=hair, name="Straightening & Rebonding", display_order=4)
    Service.objects.create(subcategory=straightening, name="Permanent Straightening (Short)", price=9000, duration_minutes=60)
    Service.objects.create(subcategory=straightening, name="Permanent Straightening (Long)", price=15000, duration_minutes=90)
    Service.objects.create(subcategory=straightening, name="Rebonding (Medium)", price=13500, duration_minutes=80)

    # Advanced Hair Treatments
    advanced_treatments = ServiceSubCategory.objects.create(category=hair, name="Advanced Hair Treatments", display_order=5)
    Service.objects.create(subcategory=advanced_treatments, name="Keratin Treatment – Short", price=22000, duration_minutes=60)
    Service.objects.create(subcategory=advanced_treatments, name="Keratin Treatment – Long", price=30000, duration_minutes=90)
    Service.objects.create(subcategory=advanced_treatments, name="Cysteine Treatment", price=25000, duration_minutes=80)

    # Add-On Services
    add_on = ServiceSubCategory.objects.create(category=hair, name="Add-On Services", display_order=6)
    Service.objects.create(subcategory=add_on, name="Hair Wash Only", price=1000, duration_minutes=10)
    Service.objects.create(subcategory=add_on, name="Scalp Massage (15 min)", price=2000, duration_minutes=15)
    Service.objects.create(subcategory=add_on, name="Hair Serum Application", price=800, duration_minutes=15)

    # Skin Services
    skin = ServiceCategory.objects.create(name="Skin Services", display_order=2)

    facials = ServiceSubCategory.objects.create(category=skin, name="Facials", display_order=1)
    Service.objects.create(subcategory=facials, name="Classic Cleanup", price=2500, duration_minutes=60)
    Service.objects.create(subcategory=facials, name="Skin Glow Facial", price=4000, duration_minutes=90)
    Service.objects.create(subcategory=facials, name="Vitamin C Facial", price=6000, duration_minutes=90)
    Service.objects.create(subcategory=facials, name="Hydra Facial", price=7500, duration_minutes=120)

    threading = ServiceSubCategory.objects.create(category=skin, name="Threading & Waxing", display_order=2)
    Service.objects.create(subcategory=threading, name="Eyebrows Threading", price=300, duration_minutes=15)
    Service.objects.create(subcategory=threading, name="Full Face Wax", price=1800, duration_minutes=30)
    Service.objects.create(subcategory=threading, name="Full Arms Wax", price=4500, duration_minutes=45)
    Service.objects.create(subcategory=threading, name="Full Legs Wax", price=6000, duration_minutes=60)

    detan = ServiceSubCategory.objects.create(category=skin, name="Detan & Bleach", display_order=3)
    Service.objects.create(subcategory=detan, name="Face & Neck Detan", price=3000, duration_minutes=45)
    Service.objects.create(subcategory=detan, name="Full Body Detan", price=8000, duration_minutes=90)
    Service.objects.create(subcategory=detan, name="Face Bleach", price=2000, duration_minutes=30)

    skin_addons = ServiceSubCategory.objects.create(category=skin, name="Add-On Services", display_order=4)
    Service.objects.create(subcategory=skin_addons, name="Lip Lightening Treatment", price=1200, duration_minutes=20)
    Service.objects.create(subcategory=skin_addons, name="Under Eye Treatment", price=1800, duration_minutes=25)

    # 3. Body Services
    body = ServiceCategory.objects.create(name="Body Services", display_order=3)

    # Massages
    massages = ServiceSubCategory.objects.create(category=body, name="Massages", display_order=1)
    Service.objects.create(subcategory=massages, name="Full Body Massage (60 min)", price=12000, duration_minutes=60)
    Service.objects.create(subcategory=massages, name="Shoulder Massage (30 min)", price=4500, duration_minutes=30)
    Service.objects.create(subcategory=massages, name="Foot Massage (60 min)", price=6500, duration_minutes=60)

    # Body Treatments
    body_treatments = ServiceSubCategory.objects.create(category=body, name="Body Treatments", display_order=2)
    Service.objects.create(subcategory=body_treatments, name="Classic Body Scrub", price=8500, duration_minutes=45)
    Service.objects.create(subcategory=body_treatments, name="Body Polish", price=14500, duration_minutes=90)
    Service.objects.create(subcategory=body_treatments, name="Underarm Treatment", price=7000, duration_minutes=30)

    # 4. Nail Services
    nails = ServiceCategory.objects.create(name="Nail Services", display_order=4)

    # Manicure & Pedicure
    manicure = ServiceSubCategory.objects.create(category=nails, name="Manicure & Pedicure", display_order=1)
    Service.objects.create(subcategory=manicure, name="Classic Manicure", price=2800, duration_minutes=30)
    Service.objects.create(subcategory=manicure, name="Spa Pedicure", price=5500, duration_minutes=45)
    Service.objects.create(subcategory=manicure, name="Hydrating Pedicure with Gel Color", price=6800, duration_minutes=60)

    # Nail Extensions & Art
    nail_art = ServiceSubCategory.objects.create(category=nails, name="Nail Extensions & Art", display_order=2)
    Service.objects.create(subcategory=nail_art, name="Gel Full Set (Hands)", price=9000, duration_minutes=90)
    Service.objects.create(subcategory=nail_art, name="Acrylic Full Set with Gel Color", price=9500, duration_minutes=120)
    Service.objects.create(subcategory=nail_art, name="Nail Art (Per Nail)", price=250, duration_minutes=15)  # Base price

    # 5. Bridal Services
    bridal = ServiceCategory.objects.create(name="Bridal Services", display_order=5)

    # Bridal Packages
    bridal_pkgs = ServiceSubCategory.objects.create(category=bridal, name="Bridal Packages", display_order=1)
    Service.objects.create(subcategory=bridal_pkgs, name="Bridal Makeup & Hair Styling", price=25000, duration_minutes=180, is_special=True)
    Service.objects.create(subcategory=bridal_pkgs, name="Pre-Bridal Skin & Hair Care Package", price=20000, duration_minutes=240, is_special=True)

    # Additional Services
    bridal_addons = ServiceSubCategory.objects.create(category=bridal, name="Additional Services", display_order=2)
    Service.objects.create(subcategory=bridal_addons, name="Saree Draping", price=3000, duration_minutes=30)
    Service.objects.create(subcategory=bridal_addons, name="Mehendi Application (Per Hand)", price=2000, duration_minutes=30)

    def reverse_func(apps, schema_editor):
        Service = apps.get_model('booking', 'Service')
        ServiceSubCategory = apps.get_model('booking', 'ServiceSubCategory')
        ServiceCategory = apps.get_model('booking', 'ServiceCategory')

        Service.objects.all().delete()
        ServiceSubCategory.objects.all().delete()
        ServiceCategory.objects.all().delete()

    class Migration(migrations.Migration):
        dependencies = [
            ('booking', '0001_initial'),  # Must match your initial migration
        ]

        operations = [
            migrations.RunPython(load_initial_data, reverse_func),
        ]


def reverse_func(apps, schema_editor):
    Service = apps.get_model('booking', 'Service')
    ServiceSubCategory = apps.get_model('booking', 'ServiceSubCategory')
    ServiceCategory = apps.get_model('booking', 'ServiceCategory')

    Service.objects.all().delete()
    ServiceSubCategory.objects.all().delete()
    ServiceCategory.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('booking', '0001_initial'),  # Make sure this matches your initial migration
    ]

    operations = [
        migrations.RunPython(load_initial_data, reverse_func),
    ]