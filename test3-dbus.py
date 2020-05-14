import pydbus
import json
import sys
import logging, logging.config


BLUEZ =          'org.bluez'
DBUS =           'org.freedesktop.DBus.ObjectManager'
LE_ADVERTISING = 'org.bluez.LEAdvertisingManager1'
GATT =           'org.bluez.GattManager1'


def getBLEinterfaces():
  systemBus = pydbus.SystemBus()
  interfaceToDbus = DBUS
  orgBluezProxy = systemBus.get(BLUEZ, '/')
  orgBluezInterface = orgBluezProxy[interfaceToDbus]
  orgBluezObjects = orgBluezInterface.GetManagedObjects()
  #
    # Returns the subordinate objects paths and
    # their supported interfaces and properties.
    # returns: array{path array{string array {variant string}}}
    # print(json.dumps(orgBluezObjects, indent = 2))

    # i = 1
    # for o, props in orgBluezObjects.items(): # this list all objects (for debug)
    #   print("object nr.",i, "- Object", o)
    #   print('properties props: ', json.dumps(props, indent = 2), "-"*30, "\n")
    #   i += 1
  
  for path, properties in orgBluezObjects.items():
    if (LE_ADVERTISING in properties) and (GATT in properties):
      logging.debug(('Returning GATT and BLE-Advertising '+\
        'interfaces on Path {p}').format(p= path))
      BLEobject = systemBus.get(BLUEZ, path)
      return (  systemBus,
                BLEobject[GATT],
                BLEobject[LE_ADVERTISING]  )
    logging.debug('Skip Object with Path :', path)
  logging.error('No Object Path (Adapter) Found with'+ \
    'BLE Advertisement and GATT Interfaces')
  raise Exception('No BLE Object found with'+ \
    'BLE Advertisement and GATT Interfaces')
  return None

def main():

  systemBus, AttributesInterface, AdvertisingInterface  = getBLEinterfaces()

  logging.debug('Got GATT Interface:'+\
    ' {i}'.format(i=AttributesInterface))
  logging.debug('Got BLE Advertising'+\
    ' Interface: {i}'.format(i=AdvertisingInterface))


if __name__ == '__main__':
  logging.config.fileConfig(fname='./data/logging.conf', disable_existing_loggers=False)
  logging.debug(('running on python version: {v}').format(v= sys.version))
  main()
