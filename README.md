# URL Shortener with FastAPI, MongoDB & JWT Auth
A full-stack URL shortener built with FastAPI, MongoDB (via Beanie ODM), and JWT-based authentication, complete with a lightweight frontend. This project is based on the roadmap.sh URL shortening service project, fulfilling its API and optional frontend requirements.   
https://roadmap.sh/projects/url-shortening-service

## ✨ Features

### 🔐 Authentication
- User registration and login
- Secure password hashing (bcrypt)
-JWT-based token authentication

### 🌐 URL Shortening
- Generate unique, short URLs
- Redirect with access tracking
- Update or delete URLs
- View access statistics

### 🧠 Tech Stack
- FastAPI backend
- Beanie ODM over MongoDB
- JWT for authentication
- Jinja2 templates for frontend
- httpx for internal API requests

### 🖥️ Frontend
- Minimal HTML UI with login, form for URL input
- Displays user's shortened URLs and access counts

## 🚀 Getting Started
- Requires python 3.13+
### 1. Install dependencies
`pip install -r requirements.txt`

### 2. Configure your environment
Create a `.env` file in the project root. Use `example.env` as a template:
```bash
MONGO_URI="your_mongo_uri"
MONGO_DB="short_urls"

MONGO_TEST_URI="your_mongo_uri"
MONGO_TEST_DB="short_urls_test"

SECRET_KEY="your_secret_key"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
💡 This app has been tested with a MongoDB Atlas Cluster (Tier 0 / Free tier).
### 3. Run the server
`fastapi dev shurl/main.py`

### 5. Add a user:
- Go to http://127.0.0.1:8000/docs
- Use the `POST /api/auth/users` endpoint to register a new user.

### 6. Visit the web interface:
Open http://127.0.0.1:8000 in your browser.

## 🧪 Testing
You can run the tests using: `pytest`.