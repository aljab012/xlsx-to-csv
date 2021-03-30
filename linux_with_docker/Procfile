web: python manage.py collectstatic --no-input;
web: gunicorn parser_project.wsgi --log-file - --log-level debug