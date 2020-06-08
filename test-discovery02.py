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
	print('added: ', path)
	#print(properties)
	if not properties:
		print(" ---Warning: NO PROPERTIES")
		return

	if "Name" in properties:
		print("  Name: ",properties["Name"])
		if properties["Name"]==nameThingsGate:
			print("we found it!")
			#path="/org/bluez/hci0/dev_B8_27_EB_E7_44_E3"
			#ifaceWanted = dbus.Interface(bus.get_object("org.bluez", path),
      #                               "org.bluez.Device1")
			#ifaceWanted.Connect()
			#properties.Connect()

	#print_normal(properties)

def properties_changed(interface, changed, invalidated, path):
	print('      >> prop. changed : ', path)
	properties = interfaces["org.bluez.Device1"]
	if not properties:
		print(" ---Warning: NO PROPERTIES")
		return	
	if "Name" in properties:
		print("  Name: ",properties["Name"])
		if properties["Name"]==nameThingsGate:
			print("we found it!")


if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

	bus = dbus.SystemBus()

	adapter = bluezutils.find_adapter()
	# path="/org/bluez/hci0/dev_B8_27_EB_E7_44_E3"
	# ifaceWanted = dbus.Interface(bus.get_object("org.bluez", path),
	# 															"org.bluez.Device1")
	# ifaceWanted.Connect()

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

	#scan_filter.update({ "UUIDs": ["FFFF"] })
	#scan_filter.update({ "Transport": "le" })

	print(pformat(scan_filter))

	adapter.SetDiscoveryFilter(scan_filter)

	adapter.StartDiscovery()

	mainloop = GObject.MainLoop()
	mainloop.run()
