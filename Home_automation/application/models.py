from subprocess import call

from django.db import models
from django.utils import timezone

from .exceptions import UnknownCommand
from .utils.radioplugs import transmit
from .utils.wiredplugs import set_state
from .utils.sun import sun


class Schedule(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return u'{name}'.format(name=self.name)

    def active_slot(self):
        slots = self.scheduleslot_set.all()
        status = None
        now = timezone.datetime.now().time()
        for slot in slots:
            slot_status = None
            if slot.start_mode == slot.TIME:
                if now >= slot.start:
                    slot_status = slot
            elif slot.start_mode == slot.SUN_UP:
                if now >= sun(58.41, 15.57).sunrise():
                    slot_status = slot
            elif slot.start_mode == slot.SUN_DOWN:
                if now >= sun(58.41, 15.57).sunset():
                    slot_status = slot
            if slot_status:
                if slot.end_mode == slot.TIME:
                    if now <= slot.end:
                        status = slot
                elif slot.end_mode == slot.SUN_UP:
                    if now <= sun(58.41, 15.57).sunrise():
                        status = slot
                elif slot.end_mode == slot.SUN_DOWN:
                    if now <= sun(58.41, 15.57).sunset():
                        status = slot
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
    button = models.ForeignKey("Button", null=True, blank=False, on_delete=models.SET_NULL)

    def __unicode__(self):
        return u'{name}'.format(name=self.schedule.name)


class Button(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    plug = models.ForeignKey('Plug', related_name="buttons")
    info = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=255, choices=(
        ("btn-default", "White"),
        ("btn-primary", "Blue"),
        ("btn-success", "Green"),
        ("btn-info", "Light blue"),
        ("btn-warning", "Orange"),
        ("btn-danger", "Red"),
    ))
    priority = models.IntegerField(default=0)

    class Meta:
        unique_together = (('name', 'plug'),)
        ordering = ["priority"]

    def child(self):
        if hasattr(self, 'radiobutton'):
             return self.radiobutton
        if hasattr(self, 'wiredbutton'):
            return self.wiredbutton
        if hasattr(self, 'irbutton'):
            return self.irbutton

    def __unicode__(self):
        return u'{name} [{plug}]'.format(name=self.name, plug=self.plug.name)

    def perform_action_internal(self):
        raise NotImplementedError("Please Implement this method")

    def perform_action(self):
        raise NotImplementedError("Please Implement this method")


class Plug(models.Model):
    has_auto_mode = models.BooleanField(default=True)
    in_auto_mode = models.BooleanField(default=False)
    name = models.CharField(max_length=255, unique=True)
    schedule = models.ForeignKey(Schedule, null=True, blank=True, on_delete=models.SET_NULL)
    default_button = models.ForeignKey(
        Button, related_name="default_action_for_plug", null=True, blank=True, on_delete=models.SET_NULL)

    def child(self):
        if hasattr(self, 'radioplug'):
             return self.radioplug
        if hasattr(self, 'wiredplug'):
            return self.wiredplug
        if hasattr(self, 'irdevice'):
            return self.irdevice

    def __unicode__(self):
        return u'{name}'.format(name=self.name)


class RadioTransmitter(models.Model):
    name = models.CharField(max_length=255)
    gpio = models.CharField(max_length=255)

    def __unicode__(self):
        return u'{name}'.format(name=self.name)


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
        return u'{protocol} [{char}] [ON: {on}, OFF: {off}]'.format(
            protocol=self.protocol, char=self.char, on=self.on, off= self.off)


class RadioButton(Button):
    payload = models.CharField(max_length=255)  # This might be a limiting factor in the future.
    rounds = models.IntegerField(default=10)

    def __unicode__(self):
        return u'{name} [{plug}]'.format(name=self.name, plug=self.plug.name)

    def _format_payload(self, str_payload):
        str_payload = str_payload.replace(" ", "")
        signals = list(self.plug.radioplug.protocol.radiosignal_set.all())
        t = self.plug.radioplug.protocol.time
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

    def perform_action_internal(self):
        payload = self._format_payload(self.payload)
        transmit(payload, self.plug.radioplug.transmitter.gpio, self.rounds)

    def perform_action(self):
        self.active = True
        for b in self.plug.buttons.all():
            if b.name != self.name:
                b.active = False
                b.save()
        self.save()
        self.perform_action_internal()


class RadioPlug(Plug):
    transmitter = models.ForeignKey(RadioTransmitter, blank=False, null=True)
    protocol = models.ForeignKey(RadioProtocol)


class IRDevice(Plug):
    pass


class IRButton(Button):
    remote = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    count = models.IntegerField(default=10)

    def __unicode__(self):
        return u'{name} [{plug}]'.format(name=self.name, plug=self.plug.name)

    def perform_action_internal(self):
        call(['irsend', 'SEND_ONCE', self.remote, self.key, "--count={}".format(self.count)])

    def perform_action(self):
        self.perform_action_internal()


class WiredButton(Button):
    payload = models.CharField(max_length=1, choices=(("0", "0"), ("1", "1")))

    def perform_action_internal(self):
        set_state(self.plug.wiredplug.gpio, int(self.payload))

    def perform_action(self):
        self.active = True
        for b in self.plug.buttons.all():
            if b.name != self.name:
                b.active = False
                b.save()
        self.save()
        self.perform_action_internal()


class WiredPlug(Plug):
    gpio = models.IntegerField(help_text="GPIO port", unique=True)
