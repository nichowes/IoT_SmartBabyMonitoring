import time
from pprint import pformat as pf
from pyHS100 import Discover, SmartPlug

def parseIP(output):
    pluglocalIP = output.partition("192.168.")[1] + output.partition("192.168.")[2].partition(" ")[0]
    print(pluglocalIP)
    return pluglocalIP

def parseName(output):
    plugName = output.partition("(")[2].partition(")")[0]
    print(plugName)
    return plugName

def plugInfo(name):
    plug = SmartPlug(deviceList[name])
    print("Hardware: %s" % pf(plug.hw_info))
    print("Full sysinfo: %s" % pf(plug.get_sysinfo()))

    print("Current state: %s" % plug.state)
    
def plugTurnOn(name):
    plug = SmartPlug(deviceList[name])
    plug.turn_on()

def plugTurnOff(name):
    plug = SmartPlug(deviceList[name])
    plug.turn_off()

deviceList = {
    }
for dev in Discover.discover().values():
    print(dev)
    output = str(dev)
    deviceList[parseName(output)] = parseIP(output)

plugTurnOff("Heater")
plugTurnOff("Fan")

time.sleep(3)

plugTurnOn("Heater")
plugTurnOn("Fan")




