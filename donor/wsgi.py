import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'donor.settings')

# Use the application without WhiteNoise for local development
application = get_wsgi_application()

# Use WhiteNoise for serving static files in production
if os.environ.get('DJANGO_ENV') == 'production':
    application = WhiteNoise(application, root='staticfiles')

