"""
WSGI config for hownewspaperswrite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import pprint
import sys
sys.path.append('/home/legionovainvicta/jobs/hownewspaperswrite/django/hownewspaperswrite/')
sys.path.append('/home/legionovainvicta/jobs/hownewspaperswrite/django/hownewspaperswrite/templates/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hownewspaperswrite.settings")
#/home/legionovainvicta/jobs/hownewspaperswrite/django/hownewspaperswrite
#activate_env=os.path.expanduser("/home/legionovainvicta/jobs/hownewspaperswrite/django/hnw/bin/activate_this.py1")
#execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
