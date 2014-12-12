#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

from pox.boot import boot

import time
import Queue
from threading import Thread,Event
import sys

class POXThread(Thread):
	def __init__(self,port):
		Thread.__init__(self)
		self.port = port
		self.stop  = Event()
		# print 'run ' + str(port)

	def run(self):
		portargs = "--port=%d" % (self.port)
		print 'run ' + portargs
		boot([ '--verbose' ,'openflow.of_01', portargs,'forwarding.l2_learning'])
		# boot(['forwarding.l2_learning'])

	def pleasestop(self):
		self.stop.set()
		exit(0)

def myNet(c1,c2):
	cPort1=6666
	cPort2=6667

	net = Mininet( topo=None, build=False)

	con1 = net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=cPort1)
	con2 = net.addController( 'c1', controller=RemoteController, ip='127.0.0.1', port=cPort2)

	for x in range(0, 3):
		hostname = "h%d" %(x)
		ip1 = "192.168.0.%d" %(x)
		hostname2 = "h1%d" %(x)
		ip2 = "192.168.0.1%d" %(x)
		switchname = "s%d" %(x)
		host = net.addHost( hostname,  ip=ip1)
		host2 = net.addHost( hostname2 , ip=ip2)
		switch = net.addSwitch( switchname, listenPort=6634)

		net.addLink(host,switch,)
		net.addLink(host2,switch,)
		switch.start([con1, con2])
		
		net.build()
		# host2.cmdPrint('ping -c 3', ip2, '>', ('tmp%d' %(x)),' &')

	
	time.sleep(3)
	CLI( net )
	net.stop()
	# c1.interrupt()
	c1.pleasestop()
	c1.join()

	c2.pleasestop()
	c2.join()
	# c2.stop()

def boot_p():
	argv = sys.argv[1:]
	

if __name__ == '__main__':
	setLogLevel( 'info' )

	c1_pox = POXThread(6666)
	c1_pox.daemon = True
	c1_pox.start()
	time.sleep(2)

	c2_pox = POXThread(6667)
	c2_pox.daemon = True
	c2_pox.start()
	time.sleep(2)

	myNet(c1_pox,c2_pox)

	# t.process.terminate()