import os

from celery import Celery

from django.apps import AppConfig
from django.conf import settings

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'server.core.settings.dev')


app = Celery(os.getenv('PROJECT_NAME', 'base'))


class CeleryConfig(AppConfig):
    name = 'server.core.celery'
    verbose_name = 'Celery Config'

    def ready(self):
        # Using a string here means the worker don't have to serialize
        # the configuration object to child processes.
        # - namespace='CELERY' means all celery-related configuration keys
        #   should have a `CELERY_` prefix.

        app.config_from_object('django.conf:settings', namespace='CELERY')

        app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)

        app.conf.update(
            result_backend='rpc://',
            result_expires=3600,
        )

        if hasattr(settings, 'RAVEN_CONFIG'):
            # Celery signal registration
            from raven import Client as RavenClient
            from raven.contrib.celery import register_signal
            from raven.contrib.celery import register_logger_signal

            raven_client = RavenClient(dsn=settings.RAVEN_CONFIG['dsn'])
            register_logger_signal(raven_client)
            register_signal(raven_client)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
