# https://github.com/LEW21/pydbus/blob/master/doc/tutorial.rst
# https://dbus.freedesktop.org/doc/dbus-specification.html

from pydbus import SystemBus, SessionBus
from gi.repository import GLib
import os
import pprint
import inspect
import _dbus_bindings

pp = pprint.PrettyPrinter(indent=2)

print(dir(_dbus_bindings))

