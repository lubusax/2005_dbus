# copied from
# https://github.com/LEW21/pydbus/blob/master/examples/systemctl.py

from pydbus import SystemBus

bus = SystemBus()

systemd = bus.get(".systemd1")
#systemd = bus.get("org.freedesktop.systemd1")

manager = systemd[".Manager"]
#manager = systemd["org.freedesktop.systemd1.Manager"]
#manager = systemd # works but may break if systemd adds another interface

import sys

try:
  if len(sys.argv) < 2:
    #print(help(manager)) # prints all methods of systemd manager
    i=1
    for unit in manager.ListUnits():
      if unit[4]=="running": # print only units running
        print(i, unit[0]," - ", unit[1])
        i+=1
      if unit[0]=="bluetooth.service": bluetoothUnit = unit
    print("bluetooth service unit: ", bluetoothUnit)
  else:
    if sys.argv[1] == "--help":
      help(manager)
    else:
      command = sys.argv[1]
      command = "".join(x.capitalize() for x in command.split("-"))
      result = getattr(manager, command)(*sys.argv[2:])

    for var in result:
      if type(var) == list:
        for line in var: print(line)
      else: print(var)
except Exception as e:
	print(e)

"""
Examples:
python -m pydbus.examples.systemctl
sudo python -m pydbus.examples.systemctl start-unit cups.service replace
"""