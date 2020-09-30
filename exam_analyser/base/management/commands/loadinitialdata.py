from django.apps import apps
from django.core.management.base import BaseCommand

from exam_analyser.configurations import INITIAL_DATA_CREATION_CONFIGURATION


class Command(BaseCommand):
    help = "Creates the applications initial default data. Used for dev purpose."

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating initial app data.")

        for config in INITIAL_DATA_CREATION_CONFIGURATION:

            model = apps.get_model(config["model"])
            data = config["data"]

            for single_data in data:
                # delete if already exists
                model.objects.filter(**single_data).delete()
                # re create to avoid any breakages
                model.objects.create(**single_data)

        self.stdout.write("Initial app data created.")
