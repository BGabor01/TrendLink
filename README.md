# TrendLink
A social media platform written in Django, that uses recommendation algorithms for personalized content and connections

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Preparation](#preparation)


## Features

- User Registration and Authentication
- Profile Management
  - Change Profile Picture

## Requirements

- Docker
- Docker Compose

## Preparation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/BGabor01/TrendLink.git 
   ```

2. **Create an .env File:**

    Create an .env file in the project root with the following content (adjust values as necessary):
    ```bash
    POSTGRES_DB=your_db_name
    POSTGRES_USER=your_db_user
    POSTGRES_PASSWORD=your_db_password
    DJANGO_SECRET_KEY=your_secret_key
    ```

3. **Build the docker containers**
    ```bash
    docker-compose build
    ```

4. **Start the applications:**
    ```bash
    docker-compose up
    ```

5. **Create a super user for Django**
- Enter the container with this command:
    ```bash
    docker exec -it trendlink-django-1 bash
    ```
- Inside the container:
    ```bash
    python manage.py createsuperuser
    ```
