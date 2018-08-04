from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from .mixins import TenantAccessRequiredMixin


class TenantDashboardView(LoginRequiredMixin,
                          TenantAccessRequiredMixin, TemplateView):

    template_name = "tenants/dashboard.html"
