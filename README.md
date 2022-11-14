# Shorty
A standard URL shortener with QR code support and a basic user interface

# Installation
```
pip install git+https://github.com/Velocidensity/shorty
```
Optionally with a virtual environment of your choice.

# Usage

Use with a WSGI server of your choice, example command for gunicorn:
```
gunicorn --bind 127.0.0.1:8080 shorty:app --workers 4
```

nginx is strongly recommended as a reverse proxy. Example configuration:

```nginx
location /shorty/ {
    proxy_pass http://127.0.0.1:8080/;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Prefix /shorty/;  # Remove if running location /

    # This will prevent shortened URLs going to 127.0.0.1:8080 from being rewritten
    proxy_redirect off;
}
```

# Configuration
Default: 
```ini
BIND_HOST="127.0.0.1"
BIND_PORT=8080
SQLALCHEMY_DATABASE_URI='sqlite:///data.db'
```
To change it, set `SHORTY_CONFIG` env var to a path to your configuration file. This is not required if you intend to use the default SQLite database (in `instance/shorty.db`).

BIND_HOST/BIND_PORT only apply when running the app directly for debugging purposes.

# Development
Development environment is managed via poetry.

```
poetry install --with=dev
```

## Compiling Tailwind CSS
Default barebones frontend comes with a precompiled Tailwind file, but if you wish to change it, you can recompile it with the following commands:
```
npm install -D tailwindcss
npx tailwindcss -c tailwind.config.js -o shorty/static/tailwind.css --minify
```

