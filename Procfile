web: gunicorn todoApp.wsgi:application --log-file - --log-level debug
python manage.py collectstatic=1
manage.py migrate