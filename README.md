# Django User Management System

This is a Django web application designed for managing user accounts, including registration, login, profile management (with picture and bio), password changes, and an admin interface for user listing and editing. It's built with a focus on clean architecture, Bootstrap styling, and readiness for deployment.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Local Development Setup](#local-development-setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
  - [Creating a Superuser](#creating-a-superuser)
  - [Configuring Email for Local Testing](#configuring-email-for-local-testing)
- [Unit Tests](#unit-tests)
- [Deployment to Render](#deployment-to-render)
  - [Render Setup](#render-setup)
  - [Environment Variables on Render](#environment-variables-on-render)
  - [Database on Render](#database-on-render)
  - [Post-Deployment Steps](#post-deployment-steps)
- [Dockerization](#dockerization)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- User Registration with Email Activation
- User Login/Logout
- Password Reset functionality
- User Profile View
- User Profile Editing (including profile picture, bio, and "about" section)
- Password Change for logged-in users
- Admin Interface for listing and editing all users (admin-only access)
- Bootstrap 5 for responsive and modern UI
- Message framework for user feedback (success/error alerts)

---

## Technologies Used

- **Backend**: Django 5.2.3 (Python 3.13.0)
- **Database**: SQLite3 (development), PostgreSQL (production via Render)
- **Styling**: Bootstrap 5
- **Forms**: `django-widget-tweaks` for Bootstrap integration
- **Image Handling**: Pillow
- **Environment Variables**: `python-dotenv` (local), Render Environment Variables (production)
- **WSGI Server**: Gunicorn (production)
- **Static Files**: WhiteNoise (production)
- **Database URL Parsing**: `dj-database-url`
- **Deployment Platform**: Render

---

## Local Development Setup

### Prerequisites

- Python 3.13.0
- pip (Python package installer)
- git
- Microsoft Visual C++ Build Tools (for Pillow on Windows)

### Installation

```bash
git clone <repository_url>
cd django_users_management/auth_project
cd ..
python -m venv venv
