from django.conf import settings
from django.conf.urls import url
from django.views.decorators.cache import cache_page

from .views import FrontendView, VouchSafeView

app_name = 'frontend'

urlpatterns = [
    # Voucher backend
    url(r'^vouch$',
        cache_page(
            settings.PAGE_CACHE_SECONDS)(VouchSafeView.as_view()),
        name='vouch'),
    # Homepage, base views
    url(r'^$',
        cache_page(
            settings.PAGE_CACHE_SECONDS)(FrontendView.as_view()),
        name='home'),
]
