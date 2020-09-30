from django.apps import apps
from django.contrib import admin


def register_all_app_models():
    """Function used to register all the applications models."""

    models = apps.get_models()
    for model in models:
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass


# Register all Models
register_all_app_models()
