from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

from django_nyt.urls import get_pattern as get_nyt_pattern

from .admin import AdminSite

admin.site.site_title = 'Admin Console'
admin.site.site_header = 'Admin Console'
admin.site.__class__ = AdminSite

urlpatterns = [

    # this url is used to generate email content
    # url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/\
    #     (?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     TemplateView.as_view(template_name="password_reset_confirm.html"),
    #     name='password_reset_confirm'),

    url(r'^api/v1/', include('server.apps.api.urls')),
    # url(r'^tenant/', include('apps.tenants.urls', namespace="tenants")),

    url(r'^crossdomain\.xml$', RedirectView.as_view(
        url=settings.STATIC_URL + 'crossdomain.xml')),

    url(r'^tower/', admin.site.urls),

    # TODO: The url structure of nyt should fit into our /api/ structure
    url(r'^notifications/', get_nyt_pattern()),


    # catch all others because of how history is handled by react router -
    # cache this page because it will never change
    url(r'', include('server.apps.frontend.urls', namespace='frontend')),
]


if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    urlpatterns += staticfiles_urlpatterns()
