from corsheaders.defaults import default_headers
from pathlib import Path
from datetime import timedelta
from decouple import config
import os

# from dotenv import load_dotenv
# load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent






deploy = True
if(deploy):
    # deploy
    SECRET_KEY = os.getenv('SECRET_KEY', 'LIARA_URL is not set.')
    hotel_email = os.getenv('EMAIL_HOST', 'LIARA_URL is not set.')
    password_email = os.getenv('EMAIL_HOST_PASSWORD', 'LIARA_URL is not set.')
    DEBUG = os.getenv('DEBUG', 'LIARA_URL is not set.')
    admin_url = os.getenv('ADMIN', 'LIARA_URL is not set.')
else:
    # local
    SECRET_KEY = config('SECRET_KEY')
    hotel_email = config('EMAIL_HOST')
    password_email = config('EMAIL_HOST_PASSWORD')
    admin_url = config('ADMIN')
    DEBUG = True



ALLOWED_HOSTS = ["*"]
AUTH_USER_MODEL = 'accounts.User'
CORS_ORIGIN_ALLOW_ALL=True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #news:
    'rest_framework',
    # 'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'drf_yasg'
]

INSTALLED_APPS += [
    'accounts',
]





CORS_ALLOWED_ORIGINS = [
    "https://domain.com",
    "https://api.domain.com",
    "http://localhost:3000",
    "http://127.0.0.1:9000"
]

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',  # for localhost (REACT Default)
    'http://192.168.10.45:3000',  # for network
)

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # +++
    'django.middleware.common.CommonMiddleware',  # +++
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# if(deploy):
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': os.getenv('database_name', 'LIARA_URL is not set.'),
#             'USER': os.getenv('database_username', 'LIARA_URL is not set.'),
#             'PASSWORD': os.getenv('password', 'LIARA_URL is not set.'),
#             'HOST': os.getenv('database_hostname_or_ip', 'LIARA_URL is not set.'),
#             'PORT': os.getenv('database_port', 'LIARA_URL is not set.'),
#         }
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'data/db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
# STATIC_ROOT =  os.path.join(BASE_DIR, 'static/')

STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'react/build/'),
    # os.path.join(BASE_DIR, 'media/'),
    # os.path.join(BASE_DIR, 'static/'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




# REST FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ],
    # 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'

}
# JWT_SECRET_KEY = 'er9238fnwi7fy2d3n3f239r87dcjknwq0e92'
# JWT_ALGORITHM = 'HS256'

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     )
    
# }

# Django project settings.py

# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
#     "ROTATE_REFRESH_TOKENS": True,
#     "BLACKLIST_AFTER_ROTATION": True,
#     "UPDATE_LAST_LOGIN": False,

#     "ALGORITHM": "HS256",
#     "VERIFYING_KEY": "",
#     "AUDIENCE": None,
#     "ISSUER": None,
#     "JSON_ENCODER": None,
#     "JWK_URL": None,
#     "LEEWAY": 0,

#     "AUTH_HEADER_TYPES": ("Bearer",),
#     "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
#     "USER_ID_FIELD": "id",
#     "USER_ID_CLAIM": "user_id",
#     "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

#     "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
#     "TOKEN_TYPE_CLAIM": "token_type",
#     "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

#     "JTI_CLAIM": "jti",

#     "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
#     "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
#     "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

#     "TOKEN_OBTAIN_SERIALIZER": "accounts.serializers.EnhancedTokenObtainPairSerializer",
#     "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
#     "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
#     "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
#     "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
#     "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
# }









