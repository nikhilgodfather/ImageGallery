# Image Gallery Application

An Image Gallery web application built using Django for the backend and Vue.js for the frontend. This application allows users to upload, update, delete, and view images in the gallery.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.x
- Node.js
- npm (Node Package Manager)
- Git

## Installation

Follow these steps to set up the project locally:

# 1. Clone the repository

```bash
git clone https://github.com/nikhilgodfather/ImageGallery.git
cd ImageGallery
```
# 2. Backend (Django)
cd backend
pip install -r requirements.txt

# 3. Make migrations and migrate the database
python manage.py makemigrations
python manage.py migrate

# 4. Start the Django development server
python manage.py runserver

# 5. Frontend (Vue.js)
cd ../frontend/vue-backend
npm install

# 6. Start the Vue.js frontend
npm run serve
