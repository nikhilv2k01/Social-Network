# Social Networking API

This project is a social networking application API built with Django Rest Framework. It includes user authentication, search functionality, friend request management, and listing of friends.

## Features

- User signup and login
- Search users by email or name
- Send, accept, and reject friend requests
- List friends
- List pending friend requests
- Rate limiting on friend requests

## Installation

### Prerequisites

- Python 3.x
- Docker
- Docker Compose
- Git

### Clone the Repository

bash
git clone https://github.com/nikhilv2k01/Social-Network.git
cd social_network



### Set Up Virtual Environment
Create and activate a virtual environment:

python3 -m venv social_env
source social_env/bin/activate  # On Windows use `social_env\Scripts\activate`

### Install Dependencies

pip install -r requirements.txt

### Set Up Environment Variables
Create a .env file in the project root directory and add the following environment variables:

DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]



### Set Up Database
Apply the database migrations:

python manage.py migrate

Run the Development Server

python manage.py runserver


### Docker Setup
Build and Run the Docker Containers
Build and run the Docker containers using Docker Compose:

docker-compose up --build

This will start the application and make it accessible at http://localhost:8000.


### API Endpoints
# User Authentication
Signup: POST /api/signup/
Login: POST /api/login/
## User Management
Search Users: GET /api/users/search/?search=<keyword>
Send Friend Request: POST /api/friend-request/send/
Accept/Reject Friend Request: POST /api/friend-request/respond/
List Friends: GET /api/friends/
List Pending Friend Requests: GET /api/pending-requests/

### Usage
### Postman Collection

Import the provided Social Network Collection (https://api.postman.com/collections/20809430-f0bb48ce-ae42-4ad2-a805-345d8e3f7699?access_key=ENTER THE KEY) to quickly test the API endpoints. The collection includes all available endpoints with example requests.

### Rate Limiting
Users can send up to 3 friend requests within a minute. If this limit is exceeded, a 429 Too Many Requests response will be returned.


### Project Structure

social_network/
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── social_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   ├── tests.py
│   └── ...
├── social_network/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
└── social_env/
    ├── bin/
    ├── include/
    └── lib/
