# cncs
A URL shortening service tailored for Markdown and code snippets


## Requirements:

- Python 3.8 
- PostgreSQL 12.2

## Installation

To start, create a PostgreSQL database. Afterwards, install the project dependencies and set the environment variables on `.env`

```bash
$ python3.8 -m venv venv
$ source venv/scripts/activate # ./venv/Scripts/activate.bat for windows
$ pip install -r requirements.txt
$ cp .env.example .env
```

If you have provided the correct PostgreSQL credentials, applying the migrations and starting the HTTP server shouldn't trigger any errors

```bash 
$ python manage.py migrate
$ python manage.py runserver
```

You can now use the app on http://localhost:8000/