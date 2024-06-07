# CS 321 Team 2 Project

## Project Overview

This project is a comprehensive development initiative for CS 321 Team 2, involving both frontend and backend implementation. The backend uses the Django REST framework, while the frontend is built with React and Material UI.

## Installation Instructions

### Prerequisites

Before starting, ensure you have the following software installed:

- Python 3.x
- Node.js and npm (Node Package Manager)

### Backend Setup

1. **Install Python Packages**
   Navigate to the backend directory and install the required Python packages by running the following commands in your terminal:

   ```bash
   pip install djangorestframework
   pip install django-cors-headers
   pip install markdown
   pip install django-filter
   pip install psycopg2-binary # if you encounter an error
   pip install djangorestframework-simplejwt
   ```

2. **Database Setup**
   Ensure you have a database configured (PostgreSQL is suggested). Update the DATABASES setting in your Django 'settings.py' file accordingly.

3. **Migrations**
   Apply the database migrations by running:

   ```bash
   python manage.py makemigrations # to compile the database changes
   python manage.py migrate        # to deploy the changes
   ```

4. **Run the Backend Server**
   Start the Django development server:

   ```bash
   python manage.py runserver
   ```

### Frontend Setup


1. **Install Node.js Packages**
   Install the required npm packages by running:

   ```bash
   npm install @mui/material @emotion/react @emotion/styled
   npm install @babel/plugin-proposal-class-properties
   npm install react-router-dom
   npm install @mui/icons-material
   ```
2. **Initialize the Project**
    If this is your first time setting up the frontend, initialize npm and create the package.json file:
    ```bash
    npm init -y --create-all packages and json
    ```
3. **Install Webpack**
    Install Webpack and Webpack CLI as development dependencies:
    ```bash
    npm i webpack webpack-cli --save-dev
    ```
4. **Run the Frontend Development Server 
    To start the frontend server, run:
    ```bash
    npm run dev
    ```
## Running the Project
1. **Start the Backend Server:**
    In the backend directory, ensure the virtual environment is activated and run:
    ```bash
    python manage.py runserver
    ```

2. **Start the Frontend Development Server:**
   In the frontend directory, run:
   ```bash
   npm run dev
    ```
3. **Access the Project:**
    Open your browser and visit `http://127.0.0.1:8000/` to view the project
    
## Contributing

  If you wish to contribute to this project, please submit a pull request or contact the project maintainers for more information.
