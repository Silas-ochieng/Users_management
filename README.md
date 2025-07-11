Django User Management System
This is a Django web application designed for managing user accounts, including registration, login, profile management (with picture and bio), password changes, and an admin interface for user listing and editing. It's built with a focus on clean architecture, Bootstrap styling, and readiness for deployment.

Table of Contents
Features

Technologies Used

Local Development Setup

Prerequisites

Installation

Running the Application

Creating a Superuser

Configuring Email for Local Testing

Configuring Django Sites

Unit Tests

Deployment to Render

Render Setup

Environment Variables on Render

Database on Render

Post-Deployment Steps

Dockerization

Contributing

License

Features
User Registration with Email Activation

User Login/Logout

Password Reset functionality

User Profile View

User Profile Editing (including profile picture, bio, and "about" section)

Password Change for logged-in users

Admin Interface for listing and editing all users (admin-only access)

Bootstrap 5 for responsive and modern UI

Message framework for user feedback (success/error alerts)

Technologies Used
Backend: Django 5.2.3 (Python 3.13.0)

Database: SQLite3 (development), PostgreSQL (production via Render)

Styling: Bootstrap 5

Forms: django-widget-tweaks for Bootstrap integration

Image Handling: Pillow

Environment Variables: python-dotenv (local), Render Environment Variables (production)

WSGI Server: gunicorn (production)

Static Files: whitenoise (production)

Database URL Parsing: dj-database-url

Deployment Platform: Render

Local Development Setup
Follow these steps to get the project running on your local machine.

Prerequisites
Python 3.13.0 installed

pip (Python package installer)

git (for cloning the repository)

Microsoft Visual C++ Build Tools: Essential for compiling Pillow on Windows. Download from Visual Studio Build Tools. During installation, select the "Desktop development with C++" workload.

Installation
Clone the repository:

git clone <repository_url>
cd django_users_management/auth_project

(Replace <repository_url> with your actual GitHub/GitLab repository URL)

Navigate to the parent directory and create a virtual environment:

cd ..
python -m venv venv

Activate the virtual environment:

Windows (PowerShell):

.\venv\Scripts\activate

macOS/Linux (Bash/Zsh):

source venv/bin/activate

Navigate back into your project directory:

cd auth_project

Install dependencies:
Ensure your requirements.txt contains only the essential packages. If you haven't already, update it to:

Django==5.2.3
django-widget-tweaks==1.4.12
Pillow==10.3.0
dj-database-url==2.1.0
gunicorn==22.0.0
whitenoise==6.6.0
python-dotenv==1.0.1

Then install:

pip install -r requirements.txt

Create a .env file:
In your auth_project directory (where manage.py is), create a file named .env and add your local environment variables. Do NOT commit this file to Git.

# .env file for local development (DO NOT COMMIT TO GIT!)

SECRET_KEY='your-local-development-secret-key' # Generate a random string
DJANGO_DEBUG='True'
ALLOWED_HOSTS='127.0.0.1,localhost'

# Email Credentials for local testing (e.g., Gmail App Password)
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT='587'
EMAIL_USE_TLS='True'
EMAIL_USE_SSL='False'
EMAIL_HOST_USER='your_sending_email@gmail.com' # Your Gmail address
EMAIL_HOST_PASSWORD='your_16_character_gmail_app_password' # Your Gmail App Password
DEFAULT_FROM_EMAIL='User Portal Support <your_sending_email@gmail.com>'
SERVER_EMAIL='webmaster@yourdomain.com'

Important: For EMAIL_HOST_PASSWORD, you must generate a Gmail App Password if you have 2-Step Verification enabled.

Apply database migrations:

python manage.py migrate

Running the Application
Start the Django development server:

python manage.py runserver

Open your browser and go to http://127.0.0.1:8000/.

Creating a Superuser
To access the Django admin panel:

python manage.py createsuperuser

Follow the prompts to set up your admin username, email, and password.

Configuring Email for Local Testing
For email activation links to work correctly during local development:

Ensure django.contrib.sites is in INSTALLED_APPS in settings.py.

Set SITE_ID = 1 in settings.py.

After running migrate, log into the Django admin (http://127.0.0.1:8000/admin/).

Go to Sites and edit the site with ID: 1.

Change the "Domain name" to 127.0.0.1:8000 and save.

Unit Tests
(This section will be expanded once unit tests are written)

Deployment to Render
This project is configured for deployment on Render.com.

Render Setup
Push your code to a Git repository (GitHub/GitLab). Ensure your .gitignore file is correctly configured to exclude venv/, db.sqlite3, media/, staticfiles/, and .env.

Sign up/Log in to Render.

Create a New Web Service and connect it to your repository.

Configure the service:

Name: your-app-name (e.g., user-management-system)

Region: Choose a region.

Branch: main (or your primary branch)

Root Directory: auth_project (if your manage.py is inside this folder)

Runtime: Python 3

Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput

Start Command: gunicorn auth_project.wsgi:application

Instance Type: Free or Starter.

Environment Variables on Render
Add these as environment variables in your Render web service settings:

SECRET_KEY: A new, strong, random string (different from local).

DJANGO_DEBUG: False

ALLOWED_HOSTS: your-app-name.onrender.com (and any custom domains, comma-separated)

WEB_CONCURRENCY: 4 (or adjust based on instance type)

EMAIL_HOST: smtp.gmail.com

EMAIL_PORT: 587

EMAIL_USE_TLS: True

EMAIL_USE_SSL: False

EMAIL_HOST_USER: Your sending Gmail address

EMAIL_HOST_PASSWORD: Your Gmail App Password (generated for Render)

DEFAULT_FROM_EMAIL: User Portal Support <your_sending_email@gmail.com>

SERVER_EMAIL: webmaster@yourdomain.com

Database on Render
Create a New PostgreSQL Database on Render.

Render will automatically provide a DATABASE_URL environment variable to your web service.

Post-Deployment Steps
Run Migrations: After the initial deploy, go to your Render web service's "Shell" tab and run:

python manage.py migrate

Create Production Superuser:

python manage.py createsuperuser

Update Django Admin Site Domain: Log into your deployed app's admin (https://your-app-name.onrender.com/admin/) and change the "Domain name" in the Sites section to your Render app's URL (e.g., your-app-name.onrender.com).