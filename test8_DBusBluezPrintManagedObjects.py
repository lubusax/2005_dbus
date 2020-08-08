# https://github.com/LEW21/pydbus/blob/master/doc/tutorial.rst
# https://dbus.freedesktop.org/doc/dbus-specification.html

from pydbus import SystemBus, SessionBus
from gi.repository import GLib
import pprint


pp = pprint.PrettyPrinter(indent=1)

systemBus = SystemBus()

bluezService= systemBus.get('org.bluez', '/' )

managedObjects = bluezService.GetManagedObjects()
pp.pprint(managedObjects)
