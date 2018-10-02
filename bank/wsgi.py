"""
WSGI config for bank project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/mrprogramer/bank')
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloth.settings")
#If multiple Django sites are run in a single mod_wsgi process, all of them will use the settings of whichever one happens to run first. This can be solved by changing:
os.environ["DJANGO_SETTINGS_MODULE"] ="bank.settings"

application = get_wsgi_application()
