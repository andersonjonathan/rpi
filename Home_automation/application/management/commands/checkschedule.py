from django.core.management.base import BaseCommand
from application.models import Plug


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        plugs = Plug.objects.filter(status=Plug.AUTO)

        for plug in plugs:
            if hasattr(plug, 'radioplug'):
                plug = plug.radioplug
            if hasattr(plug, 'wiredplug'):
                plug = plug.wiredplug
            if plug.schedule.status_at_the_moment():
                plug.turn_on_internal()
            else:
                plug.turn_off_internal()
