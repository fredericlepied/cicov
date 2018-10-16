# CICOV

## requirements

 * python3

## clean everything and start server

 * create super admin (`/admin`) with username `admin` and password `password`
 * :warning: remove old db and rewrite initial migrations for api

    rm -rf db.sqlite3 && rm -rf api/migrations/ && python manage.py makemigrations api && python manage.py migrate && echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password')" | python manage.py shell && python manage.py runserver
