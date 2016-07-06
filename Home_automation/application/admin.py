from django.contrib import admin
from .models import (
    Schedule,
    ScheduleSlot,
    Plug,
    RadioTransmitter,
    RadioProtocol,
    RadioSignal,
    RadioPlug,
    WiredPlug,
    Button, WiredButton, RadioButton)


class ScheduleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Schedule)
admin.site.register(ScheduleSlot)
admin.site.register(Plug)
admin.site.register(RadioTransmitter)
admin.site.register(RadioProtocol)
admin.site.register(RadioSignal)
admin.site.register(RadioPlug)
admin.site.register(WiredPlug)
admin.site.register(Button)
admin.site.register(WiredButton)
admin.site.register(RadioButton)
# Register your models here.
