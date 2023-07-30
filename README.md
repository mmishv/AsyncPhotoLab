# AsyncPhotoLab API
The AsyncPhotoLab API is a FastAPI-based web service that provides user authentication, photo processing, and other related functionalities.
## Features
- User registration and login using JWT tokens.
- Token-based authentication for accessing protected endpoints.
- Secure password hashing using bcrypt.
- Photo upload for processing.
- Download processed photos.
- Fetching processed photos from the server.
## Technologies Used
- FastAPI: web framework for building APIs with Python.
- Redis: in-memory data structure store used for token storage and management.
- JWT: for secure user authentication and authorization.
- bcrypt: password-hashing library for securely storing user passwords.
- Celery: asynchronous task queue used for photo processing.
- RabbitMQ: message broker used for queuing and managing Celery tasks.
- Aiofiles: for asynchronous file operations.
- Uvicorn: ASGI server that serves the FastAPI application.
## Endpoints
POST /auth/register/
Register a new user. Returns the user's details if successful.

POST /auth/login/
Log in and get an access token. Returns the access token if successful.

POST /auth/token/
Refresh the access token using the refresh token. Returns a new access token if successful.

POST /auth/logout/
Log out and invalidate the access token. Returns a success message.

POST /upload/
Upload a photo for processing. Returns a task ID.

GET /auth/me/
Get the current user's details. Requires a valid access token.

GET /download/{task_id}
Download the processed photo corresponding to the given task ID.

GET /result/{task_id}
Get the base64-encoded processed photo and task ID.

GET /photos/processed/
Get a list of processed photos.
