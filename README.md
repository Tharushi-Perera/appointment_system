# 💇‍♀️ GlamSalon Online Booking System

GlamSalon is a clean Django web app that allows salon customers to book appointments online, view services with prices, and manage their bookings.

## ✨ Features

- Book appointments with available time slots  
- Browse categorized services with pricing  
- Secure login and registration  
- View and manage appointments  
- Interactive UI with real-time updates  

## 🛠 Tech Stack  

### Frontend  
- **HTML5** + **CSS3** (via Bootstrap 5)  
- **JavaScript** (ES6) for dynamic interactions  
- **jQuery** for AJAX requests and DOM manipulation  

### Backend  
- **Django 5.2** (Python web framework)   

### Database  
- **SQLite** (Development)   

### Tools  
- **PyCharm** (IDE)  
- **GitHub** (Version Control)  
- **Font Awesome** (Icons)  

## 👩‍💻 Team  

- **Tharushi-Perera** – Project Lead, Booking System  
- **Sanjhana2710** – Login & Registration  
- **SayuriWitharana** – Service & Stylist Pages, Styling  
- **ROSEHNI02** – Homepage, Offers, Styling  

## 🚀 Getting Started  

```bash
# Clone repository
git clone https://github.com/Tharushi-Perera/salon_app.git
cd salon_app

# Set up virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Set up database
python manage.py makemigrations
python manage.py migrate

# Load initial services data
python populate_services.py

# Run development server
python manage.py runserver