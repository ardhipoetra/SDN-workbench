#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

import time
import os
import subprocess 

HOSTS = 5

def myNet(p1,p2):
	cPort1=6666
	cPort2=6667

	net = Mininet( topo=None, build=False, autoSetMacs=True)

	con1 = net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=cPort1)
	con2 = net.addController( 'c1', controller=RemoteController, ip='127.0.0.1', port=cPort2)

	for x in range(0, HOSTS):
		hostname = "h%d" %(x)
		# ip1 = "192.168.0.%d" %(x)
		# hostname2 = "h1%d" %(x)
		# ip2 = "192.168.0.1%d" %(x)
		switchname = "s%d" %(x)
		host = net.addHost(hostname)
		# host2 = net.addHost( hostname2)
		switch = net.addSwitch(switchname)

		if (x!=0):
			net.addLink(switch, lastswitch)
			
		lastswitch = switch
		net.addLink(host,switch)

		net.build()
		switch.start([con1,con2])
		# host2.cmdPrint('ping -c 3', host.IP() , '>', ('tmp%d' %(x)),' &')

	net.start()
	# net.build()
	# net.pingAll()
	CLI( net )
	net.stop()
	print 'stopping pox..'

	p1.terminate()
	p2.terminate()
	

if __name__ == '__main__':
	setLogLevel( 'info' )
	
	p1_log = open('p1_log.txt', 'w')
	p2_log = open('p2_log.txt', 'w')
	p1 = subprocess.Popen(['pox/pox.py', "master"],stdout=p1_log,stderr=p1_log,preexec_fn=os.setpgrp)
	# time.sleep(3)
	p2 = subprocess.Popen(['pox/pox.py',"slave"],stdout=p2_log,stderr=p2_log,preexec_fn=os.setpgrp)
	time.sleep(3)
	
	# p1.terminate()
	myNet(p1,p2)

	print 'close pox logs..'
	p1_log.close()
	p2_log.close()

	print 'bye'
	# t.process.terminate()