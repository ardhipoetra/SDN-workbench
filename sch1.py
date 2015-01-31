#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

import time
import os
import subprocess 
import csv
import StringIO
import iptc

HOSTS = 3

p1_log = open('logs-example/log.p1.txt', 'w')
p2_log = open('logs-example/log.p2.txt', 'w')

def closePort(port):
	rule=iptc.Rule()
	rule.protocol = "tcp"
	match = rule.create_match("tcp")
	match.dport = str(port)
	chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
	rule.target = rule.create_target("DROP")
	chain.insert_rule(rule)

def unClosePort(port):
	rule=iptc.Rule()
	rule.protocol = "tcp"
	match = rule.create_match("tcp")
	match.dport = str(port)
	chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
	rule.target = rule.create_target("DROP")
	chain.delete_rule(rule)

def myNet():
	global p1
	global p2
	global p3
	global p4

	cPort1=6666
	cPort2=6667
	hosts=[]

	kill = 0

	net = Mininet( topo=None, build=False, autoSetMacs=True)

	con1 = net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=cPort1)
	con2 = net.addController( 'c1', controller=RemoteController, ip='127.0.0.1', port=cPort2)

	for x in range(0, HOSTS):
		hostname = "h%d" %(x)
		switchname = "s%d" %(x)
		host = net.addHost(hostname)
		switch = net.addSwitch(switchname)

		if (x!=0):
			net.addLink(switch, lastswitch)
			
		lastswitch = switch
		net.addLink(host,switch)

		net.build()
		switch.start([con1,con2])
		hosts.append(host)

	net.start()

	tping = time.time()
	print 'h0 ping : %.10f' % tping

	hosts[0].cmdPrint('hping3 -c 200 -i u20000 ',hosts[1].IP(),' > logs-example/log.ping12.txt 2>&1 &')  
	#20ms every ping * 200 -> 4s


	# while True:
	# 	tcur = time.time()
	# 	if tcur - tping > 2: # after 2s running

	# 		# print 'SET ROLE C1 SLAVE '
	# 		# p1.stdin.write("import pox.openflow.nicira as nx\n")
	# 		# p1.stdin.write("for connection in core.openflow.connections:\n")
	# 		# p1.stdin.write("\tconnection.send(nx.nx_role_request(slave='true'))\n")
	# 		# p1.stdin.write('\n')

	# 		print 'close port %i in %.10f' %(cPort1,tcur)
	# 		closePort(cPort1)
	# 		break


	# print 'SET ROLE C2 AS MASTER at %.10f' %time.time()
	# p2.stdin.write("import pox.openflow.nicira as nx\n")
	# p2.stdin.write("for connection in core.openflow.connections:\n")
	# p2.stdin.write("\tconnection.send(nx.nx_role_request(master='true'))\n")
	# p2.stdin.write('\n')

	# while True:
	# 	p = subprocess.Popen(["ovs-vsctl", "-f", "csv", "list", "controller"], stdout=subprocess.PIPE)
	# 	output, err = p.communicate()
	# 	f = StringIO.StringIO(output)

	# 	reader = csv.reader(f, delimiter=',')
	# 	rownum = 0

	# 	con66 = [] # not using this for now
	# 	con67 = []

	# 	for row in reader:
	# 		uuid = row[0]
	# 		target = row[15]
	# 		role = row[13]
	# 		i = target.find(str(cPort2))
	# 		if i != -1:
	# 			if (role == 'master'):
	# 				con67.append(uuid)

	# 	f.close()
		
	# 	if len(con67) == HOSTS:
	# 		uptime = time.time()
	# 		print 'new master ready at %.10f' %uptime
	# 		break

	CLI(net)
	print 'now wait for hping3 to finish..'
	hosts[0].cmdPrint('wait %hping3')
	print 'hping3 finished at %.10f' %time.time()

	print 'open the port..'
	unClosePort(cPort1)

	print 'stopping mininet'
	net.stop()
	
	print 'stopping pox(s)..'
	p1.terminate()
	p2.terminate()

	print 'timestamp difference %.10f' %(uptime-tcur)

if __name__ == '__main__':
	setLogLevel( 'info' )
	
	p1 = subprocess.Popen(['pox/pox.py', "master66"],stdin=subprocess.PIPE, stdout=p1_log,stderr=p1_log,preexec_fn=os.setpgrp)
	print 'c1 runs, master'
	p2 = subprocess.Popen(['pox/pox.py',"slave67"],stdin=subprocess.PIPE, stdout=p2_log,stderr=p2_log,preexec_fn=os.setpgrp)
	print 'c2 runs, slave'

	print 'wait for 3 seconds...'
	time.sleep(3)
	
	myNet()

	print 'close pox logs..'
	p1_log.close()
	p2_log.close()

	print 'bye'
	# t.process.terminate()