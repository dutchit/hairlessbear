# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys

# assuming your django settings file is at '/home/myusername/mysite/mysite/settings.py'
path = '/home/rhonrado/hairlessbear/lyfers/'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'tutorial.settings'

## Uncomment the lines below depending on your Django version
###### then, for django >=1.5:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
###### or, for older django <=1.4
#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()

#-----------------------------------------------------------------------------------------
# """
# WSGI config for tutorial project.

# It exposes the WSGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
# """

# import os

# from django.core.wsgi import get_wsgi_application
# path = '/home/rhonrado/hairlessbear/lyfers/tutorial'
# if path not in sys.path:
#     sys.path.append(path)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tutorial.settings")

# application = get_wsgi_application()