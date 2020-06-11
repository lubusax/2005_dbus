# https://gist.github.com/pdixon/3970107
# dbus based python library

import contextlib
import threading

import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GObject

class Agent(dbus.service.Object):
    @dbus.service.method("org.bluez.Agent",
                         in_signature="",
                         out_signature="")
    def Release(self):
        print("Release")

    @dbus.service.method("org.bluez.Agent",
                         in_signature="os",
                         out_signature="")
    def Authorize(self, device, uuid):
        print("Sure, I'll Authorize that...")
        return

    @dbus.service.method("org.bluez.Agent",
                         in_signature="o",
                         out_signature="s")
    def RequestPinCode(self, device):
        print("RequestPinCode (%s)" % (device))
        return "1234"

    @dbus.service.method("org.bluez.Agent",
                         in_signature="o",
                         out_signature="u")
    def RequestPasskey(self, device):
        print("RequestPasskey (%s)" % (device))
        passkey = raw_input("Enter passkey: ")
        return dbus.UInt32(passkey)

    @dbus.service.method("org.bluez.Agent",
                         in_signature="ou",
                         out_signature="")
    def DisplayPasskey(self, device, passkey):
        print("Passkey ({}, {:06d})".format(device, passkey))

    @dbus.service.method("org.bluez.Agent",
                         in_signature="os",
                         out_signature="")
    def DisplayPinCode(self, device, pincode):
        print("PinCode ({}, {})".format(device, pincode))

    @dbus.service.method("org.bluez.Agent",
                         in_signature="ou",
                         out_signature="")
    def RequestConfirmation(self, device, passkey):
        print("RequestConfirmation ({}, {:06d})".format(device, passkey))
        return

    @dbus.service.method("org.bluez.Agent",
                         in_signature="s",
                         out_signature="")
    def ConfirmModeChange(self, mode):
        print("ConfirmModeChange ({})".format(mode))
        return

    @dbus.service.method("org.bluez.Agent",
                         in_signature="",
                         out_signature="")
    def Cancel(self):
        print("Cancel")

def run_agent():
    loop = GObject.MainLoop()
    GObject.threads_init()
    agent = Agent(dbus.SystemBus(), "/test/agent")
    loop.run()

class Adapter(object):
    def __init__(self, path=None):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        dbus.mainloop.glib.threads_init()
        self.bus = dbus.SystemBus()
        self.mainloop = GObject.MainLoop()
        GObject.threads_init()

        agent_thread = threading.Thread(target=run_agent)
        agent_thread.daemon = True
        agent_thread.start()

        manager = self.bluez_object('Manager', '/')
        if path is None:
            path = manager.DefaultAdapter()
        self.adapter = self.bluez_object('Adapter', path)

    def bluez_object(self, obj, path):
        return dbus.Interface(self.bus.get_object('org.bluez', path),
                              'org.bluez.{}'.format(obj))

    @contextlib.contextmanager
    def pair(self, addr):
        def create_device_reply(device):
            print("Created device: {}".format(device))
            self.mainloop.quit()

        def create_device_error(error):
            print("Error creating device: {}".format(error))
            self.mainloop.quit()

        dev_path = None

        try:
            dev_path = self.adapter.FindDevice(addr)
        except:
            pass

        if (dev_path is not None):
            print("Device exits. Removing...")
            self.adapter.RemoveDevice(dev_path)
            dev_path = None

        device = self.adapter.CreatePairedDevice(addr,
                                                 '/test/agent',
                                                 '',
                                                 reply_handler=create_device_reply,
                                                 error_handler=create_device_error)
        self.mainloop.run()

        dev_path = self.adapter.FindDevice(addr)

        yield Device(self.bus, dev_path)

        self.adapter.RemoveDevice(dev_path)


class Device(object):
    def __init__(self, bus, path):
        self.bus = bus
        self.path = path

    def bluez_object(self, obj, path):
        return dbus.Interface(self.bus.get_object('org.bluez', path),
                              'org.bluez.{}'.format(obj))

    @contextlib.contextmanager
    def open_channel(self, channel):
        serial = self.bluez_object('Serial', self.path)

        node = serial.Connect(channel)

        yield node

        serial.Disconnect(node)

''' Example to connect

#!/usr/bin/python3

import bluetooth

DONGLE_MAC = '00:03:19:xx:xx:xx' # Your mac goes here.

def main():
    adapter = bluetooth.Adapter()

    with adapter.pair(DONGLE_MAC) as device, device.open_channel('4') as path, open(path, 'w') as f:
        print(device, path, f)

if __name__ == '__main__':
    main()

'''