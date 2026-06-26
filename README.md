# music-web-api

A RESTful Music Recommendation API built using Flask that allows users to discover songs, like tracks, create playlists, and receive personalized recommendations.

The application follows modern backend development practices including JWT authentication, PostgreSQL database integration, cloud deployment, and scalable API architecture.

---

## Live Demo

🔗 https://music-web-api.onrender.com

---

## API Documentation

Interactive API documentation is available through Swagger UI.

**Swagger Docs**

`https://music-web-api.onrender.com/apidocs/`

---

## Features

### User Authentication

* User registration
* User login
* JWT Access Token authentication
* Refresh Token support
* Secure logout with token blacklisting
* Protected user profile endpoint

### Music Discovery

* Search songs using the iTunes API
* Retrieve song metadata including:

  * Song title
  * Artist
  * Album
  * Album artwork
  * Preview URL

### Song Management

* Like songs
* View liked songs
* Remove liked songs
* Prevent duplicate likes

### Playlist Management

* Create playlists
* Update playlist details
* Delete playlists
* Add songs to playlists
* Remove songs from playlists
* View playlist contents

### Recommendation System

* Personalized recommendations based on user preferences
* Similar-user recommendation approach
* Recommendation filtering to avoid duplicate suggestions

### Security

* JWT Authentication
* Password hashing
* Token blacklisting
* Protected API routes
* Secure environment variable management

### Error Handling

* Structured JSON responses
* Validation handling
* Authentication error handling
* Resource not found responses
* Consistent API status messages

---

## Tech Stack

### Backend

* Python
* Flask
* Flask-RESTful
* Flask-JWT-Extended
* SQLAlchemy
* Marshmallow

### Database

#### Development

* SQLite

#### Production

* PostgreSQL
* Neon PostgreSQL

### External APIs

* iTunes Search API

### API Documentation

* Swagger UI
* Flasgger

### Deployment

* Render

### Development Tools

* Git
* GitHub
* Postman
* pip

---

## Deployment Architecture

The application is deployed using cloud-native services:

* Flask REST API hosted on Render
* PostgreSQL database hosted on Neon
* Music metadata fetched from the iTunes API
* JWT-based authentication system
* Environment variables used for credential management
* Database schema migrations managed using Flask-Migrate

---

## Project Structure

```text
music-web-api
│
├── app/
│   ├── auth/
│   ├── songs/
│   ├── playlists/
│   ├── recommendations/
│   ├── schemas/
│   ├── models/
│   ├── extensions.py
│   ├── config.py
│   └── __init__.py
│
├── migrations/
├── run.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## Installation and Setup

### Clone Repository

```bash
git clone https://github.com/yashisaini718/music-web-api.git
cd music-web-api
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file and add:

```env
SECRET_KEY=your_secret_key

DATABASE_URL=your_database_url

JWT_SECRET_KEY=your_jwt_secret_key

FLASK_ENV=development
```

### Run Application

```bash
python run.py
```

The API runs at:

```text
http://127.0.0.1:5000
```

---

## Example API Endpoints

### Authentication

```http
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
POST /api/auth/logout
```

### Songs

```http
GET  /api/songs/search?q=artist_name
POST /api/songs/like
GET  /api/songs/liked
DELETE /api/songs/unlike/<song_id>
```

### Playlists

```http
POST   /api/playlists
GET    /api/playlists
GET    /api/playlists/<id>
PUT    /api/playlists/<id>
DELETE /api/playlists/<id>
```

### Recommendations

```http
GET /api/recommendations
```

---

## Database Migration

The application was initially developed using SQLite and later migrated to PostgreSQL hosted on Neon.

Migration management is handled using Flask-Migrate and Alembic.

Common commands:

```bash
flask db init

flask db migrate -m "Initial Migration"

flask db upgrade
```

---

## Security Considerations

* Passwords are securely hashed before storage.
* JWT tokens are used for authentication.
* Token blacklisting prevents reuse after logout.
* Sensitive credentials are stored using environment variables.
* Secret keys are excluded from version control.
* Protected routes require valid authentication tokens.

---

## Testing

API endpoints were tested using Postman.

Common test scenarios include:

* User registration and login
* Token authentication
* Song search functionality
* Liked songs management
* Playlist operations
* Recommendation generation

---

## Learning Outcomes

Through this project I gained hands-on experience with:

* REST API development using Flask
* JWT authentication and authorization
* SQLAlchemy ORM
* Marshmallow schema validation
* PostgreSQL database integration
* Database migration using Flask-Migrate
* External API integration using the iTunes API
* API testing using Postman
* Production deployment using Render
* Secure credential management
* Designing scalable backend architectures
* Version control using Git and GitHub

---

## Future Improvements

* Advanced recommendation engine
* Spotify API integration
* Song recommendation caching
* Rate limiting
* User listening history
* Playlist sharing
* Music analytics dashboard
* Docker containerization

---

## Author

**Yashi Saini**

GitHub: https://github.com/yashisaini718
