from .base import *

# GENERAL
# ------------------------------------------------------------------------------
ALLOWED_HOSTS = ["*"]

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    }
}

# WhiteNoise
# ------------------------------------------------------------------------------
MIDDLEWARE += ("whitenoise.middleware.WhiteNoiseMiddleware",)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Settings to be used only when SSL is enabled or in HTTPS
# ------------------------------------------------------------------------------
if env.bool("USE_SSL", True):
    print("SSL is enabled, including SSL related settings...")
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
