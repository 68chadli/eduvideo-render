#!/bin/sh

# Attendre que la base soit prête (optionnel)
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Créer un superutilisateur automatiquement (si non existant)
echo "from accounts.models import User; User.objects.filter(is_superuser=True).exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

exec gunicorn core.wsgi:application --bind 0.0.0.0:10000