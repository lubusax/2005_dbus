# https://github.com/LEW21/pydbus/blob/master/doc/tutorial.rst
# https://dbus.freedesktop.org/doc/dbus-specification.html

from pydbus import SystemBus, SessionBus
from gi.repository import GLib
import pprint
import dbus
import time
import inspect


pp = pprint.PrettyPrinter(indent=2)

systemBus = SystemBus()

hci0 = systemBus.get('org.bluez', '/org/bluez/hci0' )
# help(hci0)
Adapter1 = hci0['org.bluez.Adapter1']
Adapter1.Powered = True
Adapter1.Discoverable = True
Adapter1.DiscoverableTimeout= 100 #in seconds

LEAdvertisingManager1 = hci0['org.bluez.LEAdvertisingManager1']
GattManager1 = hci0['org.bluez.GattManager1']

#help(Adapter1)
#help(LEAdvertisingManager1)

class Advertisement():
  
  '''
    <node>
      <interface name='org.bluez.example.advertisement'>
        <property name="LocalName" type="s" access="readwrite"/>
        <property name="Type" type="s" access="read"/>
        <property name="ServiceUUIDs" type="as" access="read"/>
        <property name="Includes" type="as" access="read"/>
      </interface>
    </node>
  '''

  def __init__(self):
    self.LocalName = 'thingsintouch-pydbus-Gate'
    self.Type = "peripheral" # "peripheral" "broadcast"
    self.ServiceUUIDs = ['12345678-1234-5678-1234-56789abcdfff']
    self.Includes = ["tx-power", "local-name"] # "tx-power" "appearance" "local-name"

class Application():
  
  '''
    <node>
      <interface name='org.bluez.example.application'>
        <property name="Services" type="as" access="read"/>
        <method name='GetManagedObjects'>
					<arg type='a{sv}' name='response' direction='out'/>
				</method>
      </interface>
    </node>
  '''

  def __init__(self):
    self.Services = ['12345678-1234-5678-1234-56789abcdfff']
  
  def GetManagedObjects(self):
    response = {'/org/bluez/example/service0':{ 'org.bluez.GattService1': {
                                                'UUID': '12345678-1234-5678-1234-56789abcdfff',
                                                'Primary': True,
                                                'Characteristics':['/org/bluez/example/service0/characteristic0']
                                                }
                                              }
                }
#{dbus.ObjectPath('/org/bluez/example/service0/char0'): {'org.bluez.GattCharacteristic1': {'UUID': '12345678-1234-5678-1234-56789abcd800', 'Service': dbus.ObjectPath('/org/bluez/example/service0'), 'Descriptors': dbus.Array([], signature=dbus.Signature('o')), 'Flags': ['read', 'write']}}, dbus.ObjectPath('/org/bluez/example/service0'): {'org.bluez.GattService1': {'UUID': '12345678-1234-5678-1234-56789abcdfff', 'Primary': True, 'Characteristics': [dbus.Array([dbus.ObjectPath('/org/bluez/example/service0/char0')], signature=dbus.Signature('o'))]}}}
    print("was here .......")
    # for service in self.Services:
    #     response[service.get_path()] = service.get_properties()
    #     chrcs = service.get_characteristics()
    #     for chrc in chrcs:
    #         response[chrc.get_path()] = chrc.get_properties()
    print("x"*80)
    print(response)
    print("x"*80)        
    return response

class Service():
  
  '''
    <node>
      <interface name='org.bluez.example.service0'>
        <property name="UUID" type="s" access="read"/>
        <property name="Primary" type="b" access="read"/>        
      </interface>
    </node>
  '''

  def __init__(self):
    self.UUID = '12345678-1234-5678-1234-56789abcdfff'
    self.Primary = True
    self.Characteristics = ['12345678-1234-5678-1234-56789abcd800']
    self.path = "/org/bluez/example/service0"
    self.Characteristics_Paths =["/org/bluez/example/service0/characteristic0"]

  def get_properties(self):
      return { 'org.bluez.GattService1': {
                      'UUID': '12345678-1234-5678-1234-56789abcdfff',
                      'Primary': True,
                      'Characteristics':['/org/bluez/example/service0/characteristic0']
                      }
              }

  def get_path(self):
      return self.path  

class Characteristic():
  
  '''
    <node>
      <interface name='org.bluez.example.service0.characteristic0'>
        <property name="UUID" type="s" access="read"/>
        <property name="Service" type="s" access="read"/>
        <property name="Value" type="ay" access="read"/>
        <property name="Flags" type="as" access="read"/>
				<method name='ReadValue'>
					<arg type='a{sv}' name='options' direction='in'/>
					<arg type='ay' name='value' direction='out'/>
				</method>
        <method name='WriteValue'>
					<arg type='ay' name='value' direction='in'/>
					<arg type='a{sv}' name='options' direction='in'/>
				</method>
      </interface>
    </node>
  '''

  def __init__(self):
    self.UUID     = '12345678-1234-5678-1234-56789abcd800'
    self.Service  = '12345678-1234-5678-1234-56789abcdfff'
    self.ValueString = "ABCD"
    self.Value = self.ValueString.encode('ascii')
    self.Flags = ["broadcast", "read"]

  def ReadValue(self,options):
    print('TestCharacteristic Read: ' + repr(self.Value))
    return self.Value

  def WriteValue(self, value, options):
      valueString = ""
      for i in range(0,len(value)):
          valueString+= str(value[i])
      print('TestCharacteristic on was written : '+valueString)
      
      self.Value = value
      self.ValueString = valueString


sessionBus = SessionBus()
sessionBus.publish('org.bluez.example.advertisement', Advertisement()) # we are only allowed to publish on the Session Bus

sessionBus.publish('org.bluez.example.service0', Service())
sessionBus.publish('org.bluez.example.service0.characteristic0', Characteristic())

#sessionBus.request_name('org.bluez.example.application',"/")

sessionBus.publish('org.bluez.example.application', Application())

appBus = systemBus.get('org.freedesktop.DBus','/org/bluez/example/application')
advBus = sessionBus.get('org.freedesktop.DBus','/org/bluez/example/advertisement')
# help(advBus)
# appIface =appBus['org.bluez.example.application']
# print("-"*60+"/n")
# print("-"*60+"/n")
# print("-"*60+"/n")

LEAdvertisingManager1.RegisterAdvertisement('/org/bluez/example/advertisement', {})


#GattManager1.RegisterApplication('/', {})


loop = GLib.MainLoop()

try:
  loop.run()
except KeyboardInterrupt:
  LEAdvertisingManager1.UnregisterAdvertisement('/org/bluez/example/advertisement')



'''
# help(hci0)
# hci0.RemoveDevice('/org/bluez/hci0/dev_C0_E4_34_A6_5C_36') # GATT Service created on another RPI 
# hci0.RemoveDevice('/org/bluez/hci0/dev_B8_27_EB_4D_68_70') # Another Rpi : begins with B8_27_EB

# help(bluezService)
# help(bus.request_name)

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