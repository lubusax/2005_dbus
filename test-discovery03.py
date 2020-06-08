#!/usr/bin/python

from __future__ import absolute_import, print_function, unicode_literals

import dbus
import dbus.mainloop.glib
try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject
import bluezutils
import pprint
from pprint import pformat

nameThingsGate = "ThingsGate"

def print_normal(properties):

	for key in properties.keys():
		value = properties[key]
		if type(value) is dbus.String:
			value = str(value).encode('ascii', 'replace')
		if (key == "Class"):
			print("    %s = 0x%06x" % (key, value))
		else:
			print("    %s = %s" % (key, value))

	print()

def interfaces_added(path, interfaces):
	properties = interfaces["org.bluez.Device1"]
	if not properties:
		return

	if "Name" in properties:
		print("Name",properties["Name"])
		if properties["Name"]==nameThingsGate:
			print("we found it!")

	print_normal(properties)

def properties_changed(interface, changed, invalidated, path):
	print('properties changed '+'#'*120+ '\n')

	# if interface != "org.bluez.Device1":
	# 	return

	# if path in devices:
	# 	dev = devices[path]
	# 	if compact and skip_dev(dev, changed):
	# 		return
	# 	print ('devices path ', pformat(devices[path]), '§'*90)
	# 	print('devices path items : ', pformat(devices[path].items()), '§'*90)
	# 	print('changed items ', pformat(changed.items()), '§'*90, '\n')
	# 	devices[path] = devices[path].update(changed)
	# 	#print('devices path items AFTER: ', pformat(devices[path], '§'*90)
	# else:
	# 	devices[path] = changed

	# #print ('devices path ', devices[path])

	

	# if devices[path] != None : 
	# 	if ("Address" in devices[path]):
	# 		address = devices[path]["Address"]
	# 	else:
	# 		address = "<unknown>"

	# 	if compact:
	# 		print_compact(address, devices[path])
	# 	else:
	# 		print_normal(address, devices[path])
	# else:
	# 	print ('devices[path] is None')

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

	om = dbus.Interface(bus.get_object("org.bluez", "/"),
				"org.freedesktop.DBus.ObjectManager")
	objects = om.GetManagedObjects()
	for path, interfaces in objects.items():
		if "org.bluez.Device1" in interfaces:
			device = interfaces["org.bluez.Device1"]

	scan_filter = dict()

	scan_filter.update({ "UUIDs": ["FFFF"] })
	scan_filter.update({ "Transport": "le" })

	print(pformat(scan_filter))

	adapter.SetDiscoveryFilter(scan_filter)

	adapter.StartDiscovery()

	mainloop = GObject.MainLoop()
	mainloop.run()
