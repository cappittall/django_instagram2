export DJANGO_SETTINGS_MODULE=inmansdj.settings
# web: gunicorn inmansdj.wsgi --log-file -
web: daphne -b 0.0.0.0 -p $PORT inmansdj.asgi:application
worker: python manage.py runworker -v2
