from django.db import models


class Schedule(models.Model):
    name = models.CharField(max_length=255, unique=True)


class ScheduleSlot(models.Model):
    TIME = 't'
    SUN_UP = 'u'
    SUN_DOWN = 'd'
    MODES = (
        (TIME, 'Time'),
        (SUN_UP, 'Sun up'),
        (SUN_DOWN, 'Sun down'),
    )
    start_mode = models.CharField(max_length=1,
                                  choices=MODES,
                                  default=TIME)

    start = models.TimeField(null=True, blank=True)

    end_mode = models.CharField(max_length=1,
                                choices=MODES,
                                default=TIME)

    end = models.TimeField(null=True, blank=True)
    schedule = models.ForeignKey(Schedule)


class Plug(models.Model):
    AUTO = 'a'
    ON = '1'
    OFF = '0'
    STATUSES = (
        (AUTO, 'Auto'),
        (ON, 'On'),
        (OFF, 'Off'),
    )
    name = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=1,
                              choices=STATUSES,
                              default=OFF)
    schedule = models.ForeignKey(Schedule)


class RadioProtocol(models.Model):
    name = models.CharField(max_length=255)
    time = models.IntegerField(help_text="Period time t in seconds")


class RadioSignal(models.Model):
    protocol = models.ForeignKey(RadioProtocol)
    char = models.CharField(max_length=1)
    on = models.IntegerField(help_text="Nr of periods on")
    off = models.IntegerField(help_text="Nr of periods off")

    class Meta:
        unique_together = (('protocol', 'char'),)


class RadioPlug(Plug):
    protocol = models.ForeignKey(RadioProtocol)
    payload_on = models.CharField(max_length=255)  # This might be a limiting factor in the future.
    payload_off = models.CharField(max_length=255)  # This might be a limiting factor in the future.


class WiredPlug(Plug):
    gpio = models.IntegerField(help_text="GPIO port", unique=True)
    invert_gpio = models.BooleanField(help_text="Set to true if 1 turns off the plug and 0 turns it on.")

