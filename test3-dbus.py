import pydbus
import json
import sys


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
      print ('Returning GATT and LE Advertising interfaces on Path ', path)
      BLEobject = systemBus.get(BLUEZ, path)
      return (  systemBus,
                BLEobject[GATT],
                BLEobject[LE_ADVERTISING]  )
    print('Skip Object with Path :', path)
  print('No Object Path (Adapter) Found with'+ \
    'BLE Advertisement and GATT Interfaces')
  raise 
  return None

def main():

  systemBus, AttributesInterface, AdvertisingInterface  = getBLEinterfaces()
  print(AttributesInterface)


if __name__ == '__main__':
  print('running on python version:', sys.version,"\n"+"-"*70+"\n" )
  main()
