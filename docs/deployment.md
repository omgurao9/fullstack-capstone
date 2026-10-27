# Deployment notes

This project can be deployed to a Python-capable host that supports Django and persistent storage. The exact steps depend on your provider/account.

Required environment variables:
- `DJANGO_SECRET_KEY`: long random secret
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS`: your public host name, comma-separated

For a simple container host, build the included Dockerfile and expose port 8000. The demo uses SQLite and seeds data at startup; SQLite storage must be persistent or data may disappear when the instance restarts. For production, configure PostgreSQL, HTTPS, secure cookies, a proper static-file strategy, and a non-demo account/password.

A deployment URL is not included because it must come from a real deployment performed in your account.
