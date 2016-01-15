from django.db import models
from django.utils import timezone
from .exceptions import UnknownCommand
from .utils.radioplugs import transmit
from .utils.wiredplugs import turn_on as wire_on, turn_off as wire_off
from .utils.sun import sun


class Schedule(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return u'{name}'.format(name=self.name)

    def status_at_the_moment(self):
        slots = self.scheduleslot_set.all()
        status = False
        now = timezone.datetime.now().time()
        for slot in slots:
            slot_status = False
            if slot.start_mode == slot.TIME:
                if now >= slot.start:
                    slot_status = True
            elif slot.start_mode == slot.SUN_UP:
                if now >= sun(58.41, 15.57).sunrise():
                    slot_status = True
            elif slot.start_mode == slot.SUN_DOWN:
                if now >= sun(58.41, 15.57).sunset():
                    slot_status = True
            if slot_status:
                if slot.end_mode == slot.TIME:
                    if now <= slot.end:
                        status = True
                elif slot.end_mode == slot.SUN_UP:
                    if now <= sun(58.41, 15.57).sunrise():
                        status = True
                elif slot.end_mode == slot.SUN_DOWN:
                    if now <= sun(58.41, 15.57).sunset():
                        status = True
        return status


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

    def __unicode__(self):
        return u'{name}'.format(name=self.schedule.name)


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

    def __unicode__(self):
        status = ""
        for s in self.STATUSES:
            if self.status == s[0]:
                status = s[1]
        return u'{name} [{status}]'.format(name=self.name, status=status)

    def turn_on_internal(self):
        raise NotImplementedError("Please Implement this method")

    def turn_off_internal(self):
        raise NotImplementedError("Please Implement this method")

    def turn_on(self):
        raise NotImplementedError("Please Implement this method")

    def turn_off(self):
        raise NotImplementedError("Please Implement this method")

    def turn_on_auto(self):
        raise NotImplementedError("Please Implement this method")


class RadioProtocol(models.Model):
    name = models.CharField(max_length=255)
    time = models.FloatField(help_text="Period time t in seconds")

    def __unicode__(self):
        return u'{name}'.format(name=self.name)


class RadioSignal(models.Model):
    protocol = models.ForeignKey(RadioProtocol)
    char = models.CharField(max_length=1)
    on = models.IntegerField(help_text="Nr of periods on")
    off = models.IntegerField(help_text="Nr of periods off")

    class Meta:
        unique_together = (('protocol', 'char'),)

    def __unicode__(self):
        return u'{protocol} [{char}]'.format(protocol=self.protocol, char=self.char)


class RadioPlug(Plug):
    protocol = models.ForeignKey(RadioProtocol)
    payload_on = models.CharField(max_length=255)  # This might be a limiting factor in the future.
    payload_off = models.CharField(max_length=255)  # This might be a limiting factor in the future.

    def _format_payload(self, str_payload):
        signals = list(self.protocol.radiosignal_set.all())
        t = self.protocol.time
        payload = []
        for c in str_payload:
            on = None
            off = None
            for s in signals:
                if s.char.lower() == c.lower():
                    on = s.on
                    off = s.off
                    break

            if on is not None:
                payload.append((1, on*t))
            else:
                raise UnknownCommand

            if off is not None:
                payload.append((0, off*t))
            else:
                raise UnknownCommand
        return payload

    def turn_on_internal(self):
        payload = self._format_payload(self.payload_on)
        transmit(payload)

    def turn_off_internal(self):
        payload = self._format_payload(self.payload_off)
        transmit(payload)

    def turn_off(self):
        self.status = self.OFF
        self.save()
        self.turn_off_internal()

    def turn_on(self):
        self.status = self.ON
        self.save()
        self.turn_on_internal()

    def turn_on_auto(self):
        self.status = self.AUTO
        self.save()


class WiredPlug(Plug):
    gpio = models.IntegerField(help_text="GPIO port", unique=True)
    invert_gpio = models.BooleanField(help_text="Set to true if 1 turns off the plug and 0 turns it on.")

    def turn_on_internal(self):
        wire_on(self.gpio)

    def turn_off_internal(self):
        wire_off(self.gpio)

    def turn_off(self):
        self.status = self.OFF
        self.save()
        self.turn_off_internal()

    def turn_on(self):
        self.status = self.ON
        self.save()
        self.turn_on_internal()

    def turn_on_auto(self):
        self.status = self.AUTO
        self.save()
