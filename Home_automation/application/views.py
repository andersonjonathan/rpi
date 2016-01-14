from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

from .models import Plug
from utils.radioplugs import send_code
from utils.wiredplugs import turn_on, turn_off


@login_required
def index(request):
    return render(request, 'application/index.html')


@login_required
def switch(request, on, nr):
    if on == 'on':
        on = True
    elif on == 'off':
        on = False
    else:
        raise PermissionDenied
    send_code(True, on, int(nr))
    return redirect('/')


@login_required
def wire(request, on):
    if on == 'on':
        on = True
    elif on == 'off':
        on = False
    else:
        raise PermissionDenied
    wire_port = 18
    if on:
        turn_on(wire_port)
    else:
        turn_off(wire_port)
    return redirect('/')


def plug(request, pk, status):
    plug_obj = Plug.objects.get(pk=pk)
    if hasattr(plug_obj, 'radioplug'):
        plug_obj = plug_obj.radioplug
    if hasattr(plug_obj, 'wiredplug'):
        plug_obj = plug_obj.wiredplug
    if status == 'on':
        plug_obj.turn_on()
    elif status == 'off':
        plug_obj.turn_off()
    elif status == 'auto':
        plug_obj.turn_on_auto()
    else:
        raise PermissionDenied
    return redirect('/')