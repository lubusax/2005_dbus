## does not work --- still 2020 08 01
''' ERROR MESSAGE
gi.repository.GLib.Error: g-dbus-error-quark: GDBus.Error:org.freedesktop.DBus.Error.ServiceUnknown:
The name org.freedesktop.Notifications was not provided by any .service files (2)
'''

from pydbus import SessionBus

bus = SessionBus()
notifications = bus.get('.Notifications')

notifications.Notify('test', 0, 'dialog-information', "Hello World!", "pydbus works :)", [], {}, 5000)