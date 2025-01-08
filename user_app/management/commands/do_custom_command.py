from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "A stand-in for an important custom command."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Performed a custom command!"))
