"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
source /home/batmobi748/.virtualenvs/myenv/bin/activate
https://github.com/anandrathidev/seeker_provider
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8^ddocc&9lq5$%h32fgt_j-7##0-o!h2vgh-!_j5u2wc3er0ih'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['anandrathi.pythonanywhere.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'social_django',
    'crispy_forms',
    'index',
    'administrator',
    # 'easy_maps',
    # 'leaflet',
    'el_pagination',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'corsheaders',
    # 'django_elasticsearch_dsl',
    'django.contrib.sites',

    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    #  # ... include the providers you want to enable:
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.gitlab',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.twitter',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    # 'social_django.middleware.SocialAuthExceptionMiddleware',

    #"account.middleware.FacebookAuthAlreadyAssociatedMiddleware",
    "account.middleware.FacebookAuthAlreadyAssociatedMiddleware",
    #this middleware is for facebook users already logged in who wants to login
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'project.processors.PosterContextProcessors',
                'project.processors.saveReportProcessor',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect',
                'django.template.context_processors.request', ## For EL-pagination


            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'anandrathi$default',
        'USER': 'anandrathi',
        'PASSWORD': 'REO19&19',
        'HOST': 'anandrathi.mysql.pythonanywhere-services.com',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.yahoo.YahooOpenId',

    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    # 'allauth.account.auth_backends.AuthenticationBackend',
)


SOCIAL_AUTH_STRATEGY = 'social_django.strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social_django.models.DjangoStorage'

SOCIAL_AUTH_URL_NAMESPACE = 'social'

STATIC_URL = '/static/'
#STATICFILES_DIRS = '/home/anandrathi/RE/real-estate/project/static'
STATIC_ROOT = '/home/anandrathi/RE/real-estate/project/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/anandrathi/RE/real-estate/project/media_cdn'
CRISPY_TEMPLATE_PACK='bootstrap4'



# SOCIAL_AUTH_GITHUB_KEY = '44fd4145a8d85fda4ff1'
# SOCIAL_AUTH_GITHUB_SECRET = '2de7904bdefe32d315805d3b7daec7906cc0e9e7'

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_GITHUB_KEY = '399bc306d35ec9bcaf4e'
SOCIAL_AUTH_GITHUB_SECRET = 'c80665cfaf0d163ef210403c66b1dc5a6c91d26e'

SOCIAL_AUTH_FACEBOOK_KEY = "442789136494433"        # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = "a5d046f8bbe660763f995e835c8abdaf"  # App Secret


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '576414184693-t0gh6fjlb1sgi6o28um5emp77sfntd54.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '6YzYeVEJgpiJjkiP_c2uW8tF'

SOCIAL_AUTH_LOGIN_ERROR_URL = '/'

AUTH_PROFILE_MODULE = 'account.Profile'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS=True

EMAIL_HOST='smtp.gmail.com'

EMAIL_HOST_USER='gospeltruth18@gmail.com'

EMAIL_HOST_PASSWORD='bossess1'

EMAIL_PORT=587

DEFAULT_FROM_EMAIL = 'gospeltruth18@gmail.com'

SERVER_EMAIL = 'gospeltruth18@gmail.com'

EASY_MAPS_GOOGLE_KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ___0123456789'


# ELASTICSEARCH_DSL={
#     'default': {
#         'hosts': 'anandrathi.pythonanywhere.com',
#         'timeout': 60,
#     },
# }
# elasticsearch settings
# FOUNDELASTICSEARCH_URL = "anandrathi.pythonanywhere.com"
# HTTP_AUTH = os.environ.get("HTTP_AUTH", None)

# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email'] # add this
# SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {       # add this
#   'fields': 'id, name, email, picture.type(large), link'
# }
# SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [                 # add this
#     ('name', 'name'),
#     ('email', 'email'),
#     ('picture', 'picture'),
#     ('link', 'profile_url'),
# ]

SOCIAL_AUTH_RAISE_EXCEPTIONS = True
RAISE_EXCEPTIONS = True

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',

)

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.TokenAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated','rest_framework.permissions.AllowAny' )
# }

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#     'http://localhost:4200'
#     )

# CORS_ORIGIN_ALLOW_ALL = True
# Application definition


from corsheaders.defaults import default_methods
CORS_ALLOW_METHODS = list(default_methods)
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = list(default_headers)

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]


SITE_ID=1