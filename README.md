# 💇‍♀ GlamSalon Online Booking System


GlamSalon is a clean Django web app that allows salon customers to book appointments online, view services with prices, and manage their bookings.

## ✨ Features

- Book appointments with available time slots
- Browse categorized services with pricing
- Secure login and registration
- View and manage appointments

## 🛠 Tech Stack

- *Frontend*: HTML + CSS (via Bootstrap 5)
- *Backend*: Django 5.2
- *Database*: SQLite
- *Tools*: PyCharm, GitHub

## 👩‍💻 Team

- *Tharushi-Perera* – Project Lead, Booking System
- *Sanjhana2710* – Login & Registration
- *SayuriWitharana* – Service & Stylist Pages, Styling
- *ROSEHNI02* – Homepage, Offers, Styling

## 🚀 Getting Started

bash
git clone https://github.com/Tharushi-Perera/salon_app.git
cd salon_app
pip install -r requirements.txt (When cloning requirements.txt will be added as a dependency and run automatically. Run this code only if needed)
python manage.py makemigrations
python manage.py migrate
python populate_services.py
python manage.py runserver


Open http://127.0.0.1:8000/ in your browser.