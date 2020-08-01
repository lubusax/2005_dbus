from pydbus import SystemBus
import pprint

pp = pprint.PrettyPrinter(indent=2)

bus = SystemBus()
systemd = bus.get(".systemd1")

help(systemd)



doNotShow = ['dead','exited']

i=1
for unit in systemd.ListUnits():
  if unit[4] not in doNotShow:
    if "luetooth" in unit[0]:
      pp.pprint('%d --- --- ---' % i)
      pp.pprint(unit)
      i +=1