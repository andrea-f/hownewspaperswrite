import os
import sys

sys.path.append('/home/legionovainvicta/jobs/hownewspaperswrite/django/hownewspaperswrite/hownewspaperswrite/')
sys.path.append('/home/legionovainvicta/jobs/hownewspaperswrite/django/hownewspaperswrite/')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
sys.path.append('/usr/lib/python2.7/dist-packages')
#os.environ['PYTHON_EGG_CACHE'] = '/srv/www/ducklington.org/.python-egg'
os.environ['DJANGO_SETTINGS_MODULE'] = 'hownewspaperswrite.settings'
os.environ["CELERY_LOADER"] = "django"

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
