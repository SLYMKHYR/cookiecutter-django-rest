"""
WSGI config for {{ cookiecutter.app_name }} project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/gunicorn/
"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ cookiecutter.app_name }}.settings")
application = get_wsgi_application()
