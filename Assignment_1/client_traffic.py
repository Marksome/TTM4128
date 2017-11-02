#!/bin/src/python
import os, time
from subprocess import check_output as out

def gatherData():
	sysName = 'snmpwalk -v 2c -c ttm4128 localhost sysName.0'.split(' ')
	name = out(sysName).split()[-1]
	
	sysPcks = 'snmpwalk -v 2c -c ttm4128 localhost ipInReceives.0'.split(' ')
	traffic = out(sysPcks).split()[-1]
	
	return name, traffic

def sendTrap(name, traffic):
	trap = "snmptrap -v 2c -c ttm4128 localhost '' NTNU-NOTIFICATION-MIB::luisnotif "
	
	if name:
		trap += "SNMPv2-MIB::sysName.0 s '" + name + "'"

	if traffic:
		trap += " IP-MIB::ipInReceives.0 c '" + str(traffic) + "'"
	
	os.system(trap)

def main():
	name, pcks = gatherData()
	while True:
		name, temp_pcks = gatherData()
		traffic = int(temp_pcks) - int(pcks)
		if traffic < 600:
			time.sleep(10)
		else:
			sendTrap(name, temp_pcks)
			pcks = temp_pcks

main()
