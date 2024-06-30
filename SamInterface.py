import dbus
from dbus.mainloop.glib import DBusGMainLoop

DBusGMainLoop(set_as_default=True)

bus = dbus.SystemBus()
service = bus.get_object('io.stillhq.SamService', '/io/stillhq/SamService')
sam_interface = dbus.Interface(service, 'io.stillhq.SamService')
