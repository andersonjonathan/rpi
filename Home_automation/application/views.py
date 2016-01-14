from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Plug

from django.http import JsonResponse


@login_required
def index(request):
    plugs = Plug.objects.all()
    return render(request, 'application/index.html', {'plugs': plugs, 'current_page': 'Plugs'})


@login_required
def switch(request, pk, status):
    plug = Plug.objects.get(pk=pk)
    if hasattr(plug, 'radioplug'):
        plug = plug.radioplug
    if hasattr(plug, 'wiredplug'):
        plug = plug.wiredplug
    try:
        if status == 'on':
            plug.turn_on()
        elif status == 'off':
            plug.turn_off()
        elif status == 'auto':
            plug.turn_on_auto()
        else:
            return JsonResponse({"status": "faulty command"})
    except:
        return JsonResponse({"status": "Exception."})
    return JsonResponse({"status": "ok"})