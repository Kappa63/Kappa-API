# K-API

**The Kappa API** - a Flask-based REST API running at: https://api.qiblawi.dev

---

## Features

- User registration with API key generation
- API key authentication via `X-API-Key` header
- Database integration using SQLAlchemy
- Redis ratelimiting
- Swagger UI documentation
- Temporary backend for DoseGuard
- Temporary backend for Portfolio CMS

## Getting Started

### Prerequisites

- Python 3.11+
- Flask
- Requests
- BeautifulSoup4
- Flasgger
- SQLAlchemy
- Bcrypt
- Gunicorn (for production deployment)
- Redis

### Installation

```bash
git clone https://github.com/Kappa63/Kappa-API.git
cd Kappa-API
pip install -r requirements.txt
```
### Running

#### Development Server

```bash
export FLASK_APP=setup.py
python3 -m flask run --host=0.0.0.0 --port=5000
```
#### Production Server (Gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 setup:app
```

### Swagger Documentation

Access the interactive API docs at: `http://localhost:5000`
