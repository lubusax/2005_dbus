from pydbus import SystemBus
import pprint

pp = pprint.PrettyPrinter(indent=2)

bus = SystemBus()

bus = SystemBus()
bluezService= bus.get('org.bluez', '/' )

managedObjects = bluezService.GetManagedObjects()
hci0 = bus.get('org.bluez', '/org/bluez/hci0' )
# help(hci0)
# hci0.RemoveDevice('/org/bluez/hci0/dev_C0_E4_34_A6_5C_36') # GATT Service created on another RPI 
# hci0.RemoveDevice('/org/bluez/hci0/dev_B8_27_EB_4D_68_70') # Another Rpi : begins with B8_27_EB


hci0.Powered = True

managedObjects = bluezService.GetManagedObjects()

pp.pprint(managedObjects)

# help(hci0)

'''
adapter1 = hci0['org.bluez.Adapter1']
LEAdvertisingManager1 = hci0['org.bluez.LEAdvertisingManager1']

# help(bluezService)
adapter1['Powered']= True

# pp.pprint(hci0)
help(LEAdvertisingManager1)

pp.pprint(hci0)




'UUIDs': ['00001112-0000-1000-8000-00805f9b34fb',
          '00001801-0000-1000-8000-00805f9b34fb',
          '0000110e-0000-1000-8000-00805f9b34fb',
          '00001800-0000-1000-8000-00805f9b34fb',
          '00001200-0000-1000-8000-00805f9b34fb',
          '0000110c-0000-1000-8000-00805f9b34fb',
          '0000110a-0000-1000-8000-00805f9b34fb',
          '0000111f-0000-1000-8000-00805f9b34fb']

'''