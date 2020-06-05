# adapted from
# https://github.com/LEW21/pydbus/blob/master/examples/systemctl.py

from pydbus import SystemBus
import sys
import pprint
import logging, logging.config
from pprint import pformat

logging.config.fileConfig(fname='./data/bluez_0.conf', disable_existing_loggers=False)
logging.debug(('running on python version: {v}').format(v= sys.version))

bus = SystemBus()

bluezProxy = bus.get('org.bluez','/')

# print(help(bluezProxy))

bluezInterface = bluezProxy['org.freedesktop.DBus.ObjectManager']

bluezObjects = bluezInterface.GetManagedObjects()

logging.debug(pformat(bluezObjects))

bluezAdapter              = bus.get('org.bluez','/org/bluez/hci0')['org.bluez.Adapter1']
bluezGattManager          = bus.get('org.bluez','/org/bluez/hci0')['org.bluez.GattManager1']
bluezLEAdvertisingManager = bus.get('org.bluez','/org/bluez/hci0')['org.bluez.LEAdvertisingManager1']
bluezMedia                = bus.get('org.bluez','/org/bluez/hci0')['org.bluez.Media1']
bluezNetworkServer        = bus.get('org.bluez','/org/bluez/hci0')['org.bluez.NetworkServer1']

#########################################################################
# ADAPTER # ADAPTER # ADAPTER # ADAPTER # ADAPTER
#########################################################################

# bluez Adapter Interface cpp
# https://gist.github.com/nickilous/9605410

#print(help(bluezAdapter))
''' Adapter
    |  Methods:
        |  GetDiscoveryFilters(self) -> as - ['UUIDs', 'RSSI', 'Pathloss', 'Transport', 'DuplicateData']
        |  RemoveDevice(self, device:o)
        |  SetDiscoveryFilter(self, properties:a{sv})
        |  StartDiscovery(self)
        |  StopDiscovery(self)

    |  Data descriptors:
        |  Address       (s) read
        |  AddressType   (s) read
        |  Alias         (s) readwrite
        |  Class         (u) read
        |  Discoverable  (b) readwrite
        |  Name          (s) read  (u) readwrite
        |  Discovering   (b) read
        |  Modalias      (s) read
        |  Name          (s) read
        |  Pairable      (b) readwrite
        |  PairableTimeout (u) readwrite
        |  Powered       (b) readwrite
        |  UUIDs         (as) read   '''

pprint.pprint(bluezAdapter.Address) 

bluezAdapterDiscoveryFilters = bluezAdapter.GetDiscoveryFilters()

pprint.pprint(bluezAdapterDiscoveryFilters)

#########################################################################
# GattManager ## GattManager ## GattManager ## GattManager ## GattManager #
#########################################################################
''' GattManager
 |  Methods:
    |  RegisterApplication(self, application:o, options:a{sv})
    |  UnregisterApplication(self, application:o)               '''
# print(help(bluezGattManager))


#########################################################################
# LEAdvertisingManager ## LEAdvertisingManager ## LEAdvertisingManager #
#########################################################################
''' LEAdvertisingManager
 |  Methods:
    |  RegisterAdvertisement(self, advertisement:o, options:a{sv})
    |  UnregisterAdvertisement(self, service:o)
 |  Data descriptors defined here:
    |  ActiveInstances       (y) read
    |  SupportedIncludes    (as) read     ['tx-power', 'appearance', 'local-name']
    |  SupportedInstances    (y) read      '''

#print(help(bluezLEAdvertisingManager))
pprint.pprint(bluezLEAdvertisingManager.SupportedIncludes)


#########################################################################
# Media ## Media ## Media ## Media ## Media ## Media ## Media ## Media #
#########################################################################
''' Media 
    |  Methods:
        |  RegisterEndpoint(self, endpoint:o, properties:a{sv})
        |  RegisterPlayer(self, player:o, properties:a{sv})
        |  UnregisterEndpoint(self, endpoint:o)
        |  UnregisterPlayer(self, player:o)     '''

# print(help(bluezMedia))

#########################################################################
# NetworkServer ## NetworkServer ## NetworkServer ## NetworkServer #
#########################################################################
''' NetworkServer
    |  Methods:
        |  Register(self, uuid:s, bridge:s)
        |  Unregister(self, uuid:s)          '''

# print(help(bluezNetworkServer))
