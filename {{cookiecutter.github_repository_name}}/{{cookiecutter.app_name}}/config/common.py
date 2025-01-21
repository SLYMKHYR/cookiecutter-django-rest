import os
from os.path import join
from pathlib import Path

import dj_database_url
from configurations import Configuration
from decouple import config
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).resolve().parent.parent


class Common(Configuration):
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        "django.contrib.sites",

        # Third party apps
        'rest_framework',  # utilities for rest apis
        'rest_framework.authtoken',  # token authentication
        'django_filters',  # for filtering rest endpoints
        'drf_spectacular', # OpenAPI 3 schema generator

        # Your apps
        '{{cookiecutter.app_name}}.users',

    )

    # https://docs.djangoproject.com/en/2.0/topics/http/middleware/
    MIDDLEWARE = (
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "django.contrib.sites.middleware.CurrentSiteMiddleware",
    )

    ALLOWED_HOSTS = ["*"]
    CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', True, cast=bool)
    ROOT_URLCONF = '{{ cookiecutter.app_name }}.urls'
    SECRET_KEY = config('DJANGO_SECRET_KEY')
    WSGI_APPLICATION = '{{ cookiecutter.app_name }}.wsgi.application'

    # Email
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    ADMINS = (
        ('Author', '{{cookiecutter.email}}'),
    )

    DATABASE_URL = config('DATABASE_URL', default=f'sqlite:///{BASE_DIR}/db.sqlite3')
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }

    # General
    APPEND_SLASH = False
    TIME_ZONE = 'UTC'
    LANGUAGE_CODE = 'en-us'
    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    USE_I18N = False
    USE_L10N = True
    USE_TZ = True
    LOGIN_REDIRECT_URL = '/'

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/
    STATIC_URL = config("STATIC_URL", "static/")
    STATIC_ROOT = config("STATIC_ROOT", os.path.join(BASE_DIR, "statics"))
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    # Media files
    MEDIA_ROOT = join(os.path.dirname(BASE_DIR), 'media')
    MEDIA_URL = '/media/'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': STATICFILES_DIRS,
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    # Set DEBUG to False as a default for safety
    # https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = config("DEBUG", default=True, cast=bool)

    # Password Validation
    # https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#module-django.contrib.auth.password_validation
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]
    ENVIRONMENT = 'local'
    LOGGING_LEVEL = "INFO"
    LOGGING_FORMAT = "{{"
    "\"timestamp\": \"{asctime}\", "
    "\"level\": \"{levelname}\", "
    "\"threadName\": \"{threadName}\", "
    "\"name\": \"{name}\", "
    "\"request_id\": \"{request_id}\", "
    "\"message\": \"{message}\""
    "}}"
    # Logging
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "console": {
                "format": LOGGING_FORMAT,
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "style": "{"
            },
        },
        "filters": {
            "request": {
                "()": "aggregator.logging.filters.RequestIdFilter"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
                "filters": ["request"]
            },
        },
        "root": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": LOGGING_LEVEL,
                "propagate": True,
            },
            "django.server": {
                "handlers": ["django.server", "console"],
                "level": LOGGING_LEVEL,
                "propagate": False,
            },
            "django.request": {
                "handlers": ["console"],
                "level": LOGGING_LEVEL,
                "propagate": False,
            },
            "django.db.backends": {
                "handlers": ["console"],
                "level": LOGGING_LEVEL,
            },

        },
    }

    SITE_ID = config('SITE_ID', default=1, cast=int)

    # Custom user app
    AUTH_USER_MODEL = 'users.User'

    # Django Rest Framework
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': int(os.getenv('DJANGO_PAGINATION_LIMIT', 10)),
        'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
        )
    }

    if not DEBUG:
        sentry_sdk.init(
            dsn="https://30421a6213705e4ccb81a21d44abeb2d@o1167969.ingest.us.sentry.io/4507655974354944",
            integrations=[DjangoIntegration()],
            environment=ENVIRONMENT,
            # If you wish to associate users to errors (assuming you are using
            # django.contrib.auth) you may enable sending PII data.
            send_default_pii=True,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # traces_sample_rate=1.0,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            # profiles_sample_rate=1.0,
        )
