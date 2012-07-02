# Django specifiek
from django.conf import settings


def version(request):
    """
    Latest stable API version
    """
    return dict(version=settings.API_VERSION, api_url=settings.API_URL)
