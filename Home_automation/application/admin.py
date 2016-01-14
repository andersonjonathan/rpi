from django.contrib import admin
from .models import (
    Schedule,
    ScheduleSlot,
    Plug,
    RadioProtocol,
    RadioSignal,
    RadioPlug,
    WiredPlug,
)


class ScheduleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Schedule)
admin.site.register(ScheduleSlot)
admin.site.register(Plug)
admin.site.register(RadioProtocol)
admin.site.register(RadioSignal)
admin.site.register(RadioPlug)
admin.site.register(WiredPlug)

# Register your models here.
