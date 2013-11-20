from django.core.management.base import NoArgsCommand

from etat.members.models import Role

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        Role.objects.active().update(active=True)
        Role.objects.inactive().update(active=False)