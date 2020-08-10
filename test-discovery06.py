#!/usr/bin/python

#from __future__ import absolute_import, print_function, unicode_literals

from optparse import OptionParser, make_option
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GObject
# except ImportError:
#   import gobject as GObject
#import bluezutils

BLUEZ 															= 'org.bluez'
IFACE_OBJECT_MANAGER_DBUS						= 'org.freedesktop.DBus.ObjectManager'
IFACE_PROPERTIES_DBUS								= "org.freedesktop.DBus.Properties"
LE_ADVERTISING_MANAGER_IFACE 				= 'org.bluez.LEAdvertisingManager1'
GATT_MANAGER_IFACE 									= 'org.bluez.GattManager1'
GATT_CHRC_IFACE 										= 'org.bluez.GattCharacteristic1'
ADAPTER_IFACE 											= 'org.bluez.Adapter1'

PATH_HCI0 													= '/org/bluez/hci0'

UUID_GATESETUP_SERVICE      				= '5468696e-6773-496e-546f-756368000100'
ALIAS_BEGINS_WITH										= 'ThingsInTouch'
# ThingsInTouch Services        go from 0x001000 to 0x001FFF
# ThingsInTouch Characteristics go from 0x100000 to 0x1FFFFF

UUID_READ_WRITE_TEST_CHARACTERISTIC = '5468696e-6773-496e-546f-756368100000'
UUID_NOTIFY_TEST_CHARACTERISTIC     = '5468696e-6773-496e-546f-756368100001'

DEVICE_NAME 												= 'ThingsInTouch-Gate-01'

compact = True
device 	= {}

def printInfo(prefix, properties, compact=False):
	
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

def aliasFromThingsInTouch(alias):
	if alias[:len(ALIAS_BEGINS_WITH)] == ALIAS_BEGINS_WITH:
		return True
	else:
		return False

def interfaces_added(path, interfaces):
	newDevice = interfaces["org.bluez.Device1"]
	if not newDevice:
		return

	device[path] = newDevice

	prefix ="NEW -->"
	printInfo(prefix, device[path])

	alias = device[path]["Alias"]

	if aliasFromThingsInTouch(alias):
		print("Device from ThingsInTouch")


	print( device[path]["Alias"])

def properties_changed(interface, changed, invalidated, path):
	if interface != "org.bluez.Device1":
		return

	device[path].update(changed)

	prefix ="		change "
	printInfo(prefix, device[path])

if __name__ == '__main__':
	DBusGMainLoop(set_as_default=True)

	bus 							= dbus.SystemBus()

	hci0 							= bus.get_object( BLUEZ, PATH_HCI0)
	adapter_interface = dbus.Interface( hci0,   ADAPTER_IFACE)

	bus.add_signal_receiver(interfaces_added, dbus_interface = IFACE_OBJECT_MANAGER_DBUS, signal_name = "InterfacesAdded")

#	bus.add_signal_receiver(properties_changed, dbus_interface = IFACE_PROPERTIES_DBUS,
#		signal_name = "PropertiesChanged", arg0 = "org.bluez.Device1", path_keyword = "path")

# fill ---device[path]--- with the devices
# already known before searching
	om = dbus.Interface(bus.get_object("org.bluez", "/"),	"org.freedesktop.DBus.ObjectManager")
	objects = om.GetManagedObjects()
	for path, interfaces in objects.items():
		if "org.bluez.Device1" in interfaces:
			device[path] = interfaces["org.bluez.Device1"]
			address = device[path]["Address"]
			prefix ="KNOWN++++ "
			printInfo(prefix, device[path], compact)
#################################

	scan_filter = dict()
	scan_filter["Transport"] 	= "le"
	scan_filter['UUIDs'] 			= [UUID_GATESETUP_SERVICE]

	adapter_interface.SetDiscoveryFilter(scan_filter)
	adapter_interface.StartDiscovery()

	mainloop = GObject.MainLoop()
	mainloop.run()