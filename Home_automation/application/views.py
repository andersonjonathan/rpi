from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from plugs.radioplugs import send_code
from plugs.wiredplugs import turn_on, turn_off


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
    send_code(True, on, nr)
    return render(request, 'application/index.html')


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
    return render(request, 'application/index.html')
