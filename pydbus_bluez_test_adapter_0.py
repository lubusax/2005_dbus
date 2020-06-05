# adapted from
# https://github.com/LEW21/pydbus/blob/master/examples/systemctl.py
# and bluez 5.50 / test

from pydbus import SystemBus
import sys
import pprint
import logging, logging.config
from pprint import pformat
import gi
from gi.repository import GObject

class testObject(object):
  pass

logging.config.fileConfig(fname='./data/bluez_0.conf', disable_existing_loggers=False)
logging.debug(('running on python version: {v}').format(v= sys.version))

logging.debug('PyGObject version '+pformat(gi.version_info))

bus = SystemBus()
bluezAdapter = bus.get('org.bluez','/org/bluez/hci0')['org.bluez.Adapter1']
logging.debug(pformat(bluezAdapter))

test00 = testObject
logging.debug(pformat(test00))
#adapter = bluezAdapter
#addr = adapter.Get("org.bluez.Adapter1", "Address")
#print("Address", addr)




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
