from django.core.management.base import BaseCommand, CommandError
from application.models import Plug

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        plugs = Plug.objects.all()

        for plug in plugs:
            if hasattr(plug, 'radioplug'):
                plug = plug.radioplug
            if hasattr(plug, 'wiredplug'):
                plug = plug.wiredplug
