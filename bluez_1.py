# adapted from
# https://github.com/LEW21/pydbus/blob/master/examples/systemctl.py

from pydbus import SystemBus
import sys
import pprint

busTEST0 = "org.bluez.test0"

bus = SystemBus()

bluezProxy = bus.get('org.bluez','/')

# print(help(bluezProxy))

bluezInterface = bluezProxy['org.freedesktop.DBus.ObjectManager']

bluezObjects = bluezInterface.GetManagedObjects()

pprint.pprint(bluezObjects)

bluezAdapter              = bus.get('org.bluez','/org/bluez/hci0')['org.bluez.Adapter1']
bluezGattManager          = bus.get('org.bluez','/org/bluez/hci0')['org.bluez.GattManager1']
bluezLEAdvertisingManager = bus.get('org.bluez','/org/bluez/hci0')['org.bluez.LEAdvertisingManager1']

            # appPath = '/'
            # app = dbus.service(bus,'/')

servicePath = '/org/bluez/test/service0'
            # serviceUUID = '12345678-1234-5678-1234-56789abcdfff'
            # servicePrimary = True
            # service = dbus.service.Object(bus, servicePath)


class ServiceTEST0(object):
    """
    DBus Service XML definition. 
    type="i" for integer, "s" string, "d" double, "as" list of string data.
    """
    dbus = """
    <node>
      <interface name='org.bluez.test.service0'>
            <method name="server_no_args">
            </method>
      </interface>
    </node>
    """.format(busTEST0)

    def server_no_args(self): return

            # PATH_BASE = '/org/bluez/example/service'

            # def __init__(self, bus, index, uuid, primary):
            #     self.path = self.PATH_BASE + str(index)
            #     self.bus = bus
            #     self.uuid = uuid
            #     self.primary = primary
            #     self.characteristics = []
            #     dbus.service.Object.__init__(self, bus, self.path)

            # def get_properties(self):
            #     return {
            #             GATT_SERVICE_IFACE: {
            #                     'UUID': self.uuid,
            #                     'Primary': self.primary,
            #                     'Characteristics': dbus.Array(
            #                             self.get_characteristic_paths(),
            #                             signature='o')
            #             }
            #     }

            # def get_path(self):
            #     return dbus.ObjectPath(self.path)

            # def add_characteristic(self, characteristic):
            #     self.characteristics.append(characteristic)

            # def get_characteristic_paths(self):
            #     result = []
            #     for chrc in self.characteristics:
            #         result.append(chrc.get_path())
            #     return result

            # def get_characteristics(self):
            #     return self.characteristics

            # @dbus.service.method(DBUS_PROP_IFACE,
            #                      in_signature='s',
            #                      out_signature='a{sv}')
            # def GetAll(self, interface):
            #     if interface != GATT_SERVICE_IFACE:
            #         raise InvalidArgsException()

            #     return self.get_properties()[GATT_SERVICE_IFACE]

