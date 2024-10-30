#!/bin/sh

# Run database migrations and collect static files
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser(
        username='$DJANGO_SUPERUSER_USERNAME', 
        email='$DJANGO_SUPERUSER_EMAIL', 
        password='$DJANGO_SUPERUSER_PASSWORD'
    )
    print('Superuser created')
else:
    print('Superuser already exists')
"

# Start Django development server
exec python manage.py runserver 0.0.0.0:8000
