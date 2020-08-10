#!/usr/bin/python

from __future__ import absolute_import, print_function, unicode_literals

from optparse import OptionParser, make_option
import dbus
import dbus.mainloop.glib
try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject
import bluezutils

compact = True
device = {}


def printInfo(prefix, properties, compact):
	
	address = properties.get("Address")
	if address is None:
		address = "    address unknown"

	if compact:	
		name = properties.get("Name")
		if name is None:
			name = "    name unknown"
		print("%s %s %s" % (prefix, address, name))
	else:
		print(prefix+"[ " + address + " ]")
		for key in properties:
			if (key == "Class"):
				print("    %s = 0x%06x" % (key, properties[key]))
			else:
				print("    %s = %s" % (key, properties[key]))



def interfaces_added(path, interfaces):
	newDevice = interfaces["org.bluez.Device1"]
	if not newDevice:
		return

	device[path] = newDevice

	prefix ="NEW -->"
	printInfo(prefix, device[path], compact)


def properties_changed(interface, changed, invalidated, path):
	if interface != "org.bluez.Device1":
		return

	device[path].update(changed)

	prefix ="		change "
	printInfo(prefix, device[path], compact)

if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

	bus = dbus.SystemBus()

	adapter = bluezutils.find_adapter()

	bus.add_signal_receiver(interfaces_added,
			dbus_interface = "org.freedesktop.DBus.ObjectManager",
			signal_name = "InterfacesAdded")

	bus.add_signal_receiver(properties_changed,
			dbus_interface = "org.freedesktop.DBus.Properties",
			signal_name = "PropertiesChanged",
			arg0 = "org.bluez.Device1",
			path_keyword = "path")

# fill ---device[path]--- with the devices
# already known before searching
	om = dbus.Interface(bus.get_object("org.bluez", "/"),
				"org.freedesktop.DBus.ObjectManager")
	objects = om.GetManagedObjects()
	for path, interfaces in objects.items():
		if "org.bluez.Device1" in interfaces:
			device[path] = interfaces["org.bluez.Device1"]
			address = device[path]["Address"]
			prefix ="KNOWN++++ "
			printInfo(prefix, device[path], compact)
#################################

	scan_filter = dict()
	scan_filter["Transport"] = "le"
	scan_filter['UUIDs'] = ['12345678-1234-5678-1234-56789abcdfff']
	filters = adapter.GetDiscoveryFilters()
	#print(filters)

	adapter.SetDiscoveryFilter(scan_filter)
	adapter.StartDiscovery()

	mainloop = GObject.MainLoop()
	mainloop.run()