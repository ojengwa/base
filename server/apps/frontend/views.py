import os

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.views.generic.base import View, ContextMixin
from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class FrontendView(View, ContextMixin):
    """Render main page."""

    def get_context_data(self, **kwargs):
        context = FrontendView.get_context_data(self, **kwargs)
        context['ws_messages'] = cache.get("ws_messages")

        return context

    def get(self, request):
        """Return html for main application page."""

        abspath = open(os.path.join(settings.STATIC_ROOT,
                                    'frontend/index.html'), 'r')
        return HttpResponse(content=abspath.read())


class VouchSafeView(GenericAPIView):
    """Return protected data main page. Voucher printing, etc"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Process GET request and return protected data."""

        data = {
            'data': 'THIS IS THE PROTECTED STRING FROM SERVER',
        }

        return Response(data, status=status.HTTP_200_OK)
