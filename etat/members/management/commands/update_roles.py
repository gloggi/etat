from django.core.management.base import BaseCommand

from etat.members.models import Role

class Command(BaseCommand):

    def handle(self, *args, **options):
        Role.objects.active().update(active=True)
        Role.objects.inactive().update(active=False)