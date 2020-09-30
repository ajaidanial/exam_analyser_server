from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates the applications super admin based on the given env variables."

    def handle(self, *args, **kwargs):
        self.create_django_admin()

    def create_django_admin(self):
        self.stdout.write("Creating django admin.")

        credentials = settings.DJANGO_ADMIN
        user_model = get_user_model()

        # delete, if already exists
        user_model.objects.filter(username=credentials["username"]).delete()

        # create it
        user = user_model.objects.create_superuser(**credentials)

        self.stdout.write("Django admin created.")
