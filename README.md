# TrendLink
A social media platform, that uses recommendation algorithms for personalized content and connections

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Requirements](#requirements)
- [Preparation](#preparation)
- [Docker configuration](#docker-configuration)


## Features

- User Registration and Authentication
- Profile Management
- Post Creation and Management
- Comment Creation and Management

## Tech Stack

### Backend
- **Framework**: Django
- **API**: Django Rest Framework (DRF)
- **Database**: PostgreSQL
- **Authentication**: SessionAuth
- **Containerization**: Docker
- **Proxy Server**: Nginx

### Frontend
- **HTML/CSS**
- **JavaScript**
- **JQuery**

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

## Docker Configuration
**Database (PostgreSQL)**
- The docker-compose.yml file sets up a PostgreSQL database container. Make sure the .env file contains the correct database configuration:

```bash
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
```

**Nginx**
- Nginx is used as a reverse proxy to serve the Django application.
- The configuration file is located at ```trend_link/nginx.conf```.
- The Docker Compose setup maps this configuration file to the Nginx container.