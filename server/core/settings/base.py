"""Django settings for base project."""
import os
import sys
import datetime

from .. import environ

join = os.path.join
dirname = os.path.dirname
exists = os.path.exists


env = environ.Env()

root = environ.Path(__file__) - 3
project_root = root - 1

env_file = join(dirname(str(root)), '.env')
if exists(env_file):
    environ.Env.read_env(str(env_file))

DEBUG = env.bool('DEBUG', False)
STAGE = env.str('STAGE')

if sys.argv[1:2] == ['test']:
    STAGE = 'test'

SECRET_KEY = env('SECRET_KEY')
# Should have '*' for local, the site URL for production
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', [])

DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL')

DATABASES = {
    'default': env.db(),
}

SITE_ID = 1

PROJECT_NAME = env.str('PROJECT_NAME', default='Base Project')

SENTRY_MANAGEMENT_URL = env.str('SENTRY_MANAGEMENT_URL', default="#")
MAILHOG_MANAGEMENT_URL = env.str('MAILHOG_MANAGEMENT_URL',
                                 default="http://localhost:8025")
RABBITMQ_MANAGEMENT_URL = env.str('RABBITMQ_MANAGEMENT_URL',
                                  default="http://localhost:15672")
POSTGRES_MANAGEMENT_URL = env.str('POSTGRES_MANAGEMENT_URL',
                                  default="http://localhost:5050")
SPHINX_DOCUMENTATION_URL = env.str('SPHINX_DOCUMENTATION_URL',
                                   default="http://localhost:8007")
REDIS_BROWSER_MANAGEMENT_URL = env.str('REDIS_BROWSER_MANAGEMENT_URL',
                                       default="http://localhost:8019")


ALLOWED_EMAIL_DOMAINS = [
    'example.com',
]

DEFAULT_PROTOCOL = env.str('DEFAULT_PROTOCOL', default='https')

if STAGE == 'local' or STAGE == 'testing':
    DEFAULT_PROTOCOL = 'http'


TENANT_ROOT_SITE_ID = env.int('TENANT_ROOT_SITE_ID', default=SITE_ID)
TENANT_INVITE_EXPIRATION_IN_DAYS = 2


CORE_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.humanize',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
)


THIRD_PARTY_APPS = (
    'rest_framework',
    'knox',
    'django_saas_email.apps.DjangoSaasEmailConfig',
    'tinymce',

    'rest_framework.authtoken',
    'rest_auth',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'rest_framework_swagger',
    'corsheaders',

    # Channels
    'channels',
    'django_nyt',
    'channels_panel',

    'server.core.celery.CeleryConfig',
    'actstream',
)

LOCAL_APPS = (
    'server.apps.tenants',
    'server.apps.frontend',
    'server.apps.accounts',
    'server.apps.comments',
    'server.apps.activities',
)


INSTALLED_APPS = CORE_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'server.apps.tenants.middleware.TenantMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware'
)

if DEBUG is True and STAGE == 'local':
    import socket

    INSTALLED_APPS += (
        'debug_toolbar',
        'django_extensions',
    )

    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ip[:-1] + '1']


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(root.path('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'server.core.context_processors.admin_settings'
            ],
        },
    },
]

ROOT_URLCONF = 'server.core.urls'

WSGI_APPLICATION = 'server.core.wsgi.application'

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'accounts.User'

ACCOUNT_ACTIVATION_DAYS = 7  # days

MEDIA_ROOT = str(root.path('media'))
MEDIA_URL = '/media/'

STATIC_ROOT = str(project_root.path('client/dist'))
STATIC_URL = env.str('STATIC_URL', default='/assets/')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


if not STAGE == 'test':
    STATICFILES_STORAGE = (
        'whitenoise.storage.CompressedManifestStaticFilesStorage')


DATABASES['default']['ATOMIC_REQUESTS'] = True

# Lets cache some things
REDIS_URL = env.str('REDIS_URL')
CACHING = env.bool('CACHING', default=False)

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': '{}/0'.format(REDIS_URL),
        'TIMEOUT': env.int('CACHE_TIMEOUT', default=86400),
    }
}


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_PAGINATION_CLASS': (
        'server.apps.api.pagination.StandardResultsSetPagination'),
    'PAGE_SIZE': 20,
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': (
        'server.apps.tenants.serializers.TenantSignUpSerializer'),
}

CORS_ORIGIN_WHITELIST = (
    '0.0.0.0:8000',
    'localhost:8000',
    'localhost:3000',
    '127.0.0.1:8000',
)

JWT_SECRET = env('JWT_SECRET')
JWT_ISSUER_NAME = env.str('JWT_ISSUER_NAME', default=PROJECT_NAME)

JWT_AUTH = {
    'JWT_PAYLOAD_HANDLER': 'server.apps.api.jwt.payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER': (
        'server.apps.api.jwt.response_payload_handler'),
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': (
        'server.apps.api.jwt.get_username_from_payload_handler'),
    'JWT_SECRET_KEY': JWT_SECRET,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=60 * 60 * 72),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=60 * 60 * 12),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_ISSUER': 'drf-saas-starter',
}

REST_USE_JWT = True

SWAGGER_SETTINGS = {
    'LOGIN_URL': 'admin:index',
    'LOGOUT_URL': 'admin:logout',
    'USE_SESSION_AUTH': True,
    'SECURITY_DEFINITIONS': {
        "token": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        },
    }
}


REST_KNOX = {
    'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
    'AUTH_TOKEN_CHARACTER_LENGTH': 64,
    'USER_SERIALIZER': 'knox.serializers.UserSerializer'
}

# heroku labs:enable runtime-dyno-metadata must have been run before + a
# new deploy
ON_HEROKU = env('HEROKU_APP_ID', default=False)

if ON_HEROKU:

    HEROKU_APP_NAME = env.str('HEROKU_APP_NAME')
    HEROKU_RELEASE_CREATED_AT = env('HEROKU_RELEASE_CREATED_AT', default=None)
    HEROKU_RELEASE_VERSION = env('HEROKU_RELEASE_VERSION', default=None)
    HEROKU_SLUG_DESCRIPTION = env('HEROKU_SLUG_DESCRIPTION', default=None)
    HEROKU_SLUG_COMMIT = GIT_BRANCH = env('HEROKU_SLUG_COMMIT', default=None)

    SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)

    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    # https://docs.djangoproject.com/en/1.10/ref/settings/#session-cookie-httponly
    CSRF_COOKIE_HTTPONLY = True
    # https://docs.djangoproject.com/en/1.10/ref/settings/#csrf-cookie-secure
    CSRF_COOKIE_SECURE = True

    INSTALLED_APPS += (
        'raven.contrib.django.raven_compat',
    )

    MIDDLEWARE = [
        # We recommend putting this as high in the chain as possible
        ('raven.contrib.django.raven_compat.middleware.'
         'SentryResponseErrorIdMiddleware'),
    ] + MIDDLEWARE

    RAVEN_CONFIG = {
        'dsn': ('https://d8149058f0924193aa9af8a87e8dca83:'
                'fec43582f54b4c448882b44a7ce308a3@sentry.io/122593'),
        'release': GIT_BRANCH
    }

    CACHES['default'][
        'KEY_PREFIX'] = "{}-{}".format(HEROKU_APP_NAME, HEROKU_RELEASE_VERSION)


if ON_HEROKU:

    # Heroku expects to receive error messages on STDERR, the following
    # logging takes care of this
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry', ],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                # To capture more than ERROR, change to WARNING, INFO, etc.
                'level': 'ERROR',
                'class': ('raven.contrib.django.raven_compat'
                          '.handlers.SentryHandler'),
                'tags': {'custom-tag': 'x'},
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }

elif STAGE in ['test', 'circleci']:

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_COLLAPSED': True,
}

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'channels_panel.panel.ChannelsDebugPanel',
]


ACCOUNT_ALLOW_REGISTRATION = env.bool('ACCOUNT_ALLOW_REGISTRATION', True)
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_ADAPTER = 'server.apps.accounts.adapters.AccountAdapter'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
# ACCOUNT_DEFAULT_HTTP_PROTOCOL="https"

EMAIL_VERIFICATION_REDIRECT_URL = env.str(
    'EMAIL_VERIFICATION_REDIRECT_URL', None)


REST_SESSION_LOGIN = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

LOGIN_REDIRECT_URL = 'frontend:home'
LOGIN_URL = 'admin:index'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.password_validation'
                 '.UserAttributeSimilarityValidator'),
        'OPTIONS': {
            'max_similarity': 0.7,
            'user_attributes': ('username', 'first_name', 'last_name', 'email')
        }
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'MinimumLengthValidator'),
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.CommonPasswordValidator'
        ),

    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.NumericPasswordValidator'
        ),
    }
]


SENDGRID_API_KEY = env("SENDGRID_API_KEY", default=None)
DJANGO_SAAS_TEST_EMAIL_ADDRESS = env(
    "DJANGO_SAAS_TEST_EMAIL_ADDRESS", default="test@example.org")

if ON_HEROKU:

    ANYMAIL = {
        "SENDGRID_API_KEY": SENDGRID_API_KEY,
    }

    EMAIL_BACKEND = env(
        'EMAIL_BACKEND', default='anymail.backends.sendgrid.SendGridBackend')

else:

    EMAIL_BACKEND = env(
        'EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
    EMAIL_PORT = env("EMAIL_PORT", default=1025)
    EMAIL_HOST = env("EMAIL_HOST", default='mailhog')
    EMAIL_HOST_USER = env("EMAIL_HOST_USER", default='')
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default='')
    EMAIL_USE_TLS = env("EMAIL_USE_TLS", default=False)

CRISPY_TEMPLATE_PACK = 'bootstrap4'

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'width': '70%',
    'height': '500px'
}


CELERY_BROKER_URL = env.str(
    'CLOUDAMQP_URL', default='amqp://guest:guest@127.0.0.1')
BROKER_POOL_LIMIT = 1
BROKER_HEARTBEAT = None
BROKER_CONNECTION_TIMEOUT = 30

CELERY_RESULT_BACKEND = None
CELERY_SEND_EVENTS = False

CELERY_EVENT_QUEUE_EXPIRES = 60


if STAGE == 'local':
    CELERY_TASK_ALWAYS_EAGER = env.bool(
        'CELERY_TASK_ALWAYS_EAGER', default=True)
elif STAGE == 'test':
    CELERY_TASK_ALWAYS_EAGER = True

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "ROUTING": "server.core.routing.channel_routing",
        "CONFIG": {
            "hosts": [REDIS_URL],
        }
    }
}

NYT_ENABLE_ADMIN = True
