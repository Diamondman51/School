web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn education.wsgi --bind 0.0.0.0:$PORT