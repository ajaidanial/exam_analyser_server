from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Initializes the app by running the necessary commands."

    def handle(self, *args, **kwargs):
        """Call all the necessary commands."""

        call_command("migrate")
        call_command("createdjangoadmin")
        call_command("loadinitialdata")
