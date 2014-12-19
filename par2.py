#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

import time
import os
import signal
import subprocess 
import csv
import StringIO
import Queue

HOSTS = 3

p1_log = open('log.p1.txt', 'w')
p2_log = open('log.p2.txt', 'w')

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
	print 'Applying master..'
	time.sleep(10)
	# print 'pre-kill p1'
	# time.sleep(5)
	# print 'kill p1'
	# os.killpg(p1.pid, signal.SIGTERM)
	# time.sleep(5)

	# hosts[0].cmd('iperf -s -P 1 -u > log.s.txt &')
	# hosts[1].cmd('iperf -u -c ',hosts[0].IP(),' -i 1 -t 25 > log.c.txt &')

	# print 'iperf both running'
	# status = 1
	# while True:
	# 	print 'waiting for next round'
	# 	time.sleep(2)
	# 	if status == 1:
	# 		print 'kill c1'
	# 		os.killpg(p1.pid, signal.SIGINT)
	# 		time.sleep(5)
	# 		kill+=1
	# 		status = 2
	# 		break
	# 	# elif status == 2:
	# 	# 	print 'summon again, c1'
	# 	# 	p1 = subprocess.Popen(['pox/pox.py', "master66"],stdout=p1_log,stderr=p1_log,preexec_fn=os.setpgrp)
	# 	# 	print 'sleep 1s'
	# 	# 	time.sleep(1)
	# 	# 	status = 1

	# 	# if kill > 2:
	# 	# 	break
	# print 'waiting for iperf..'
	# hosts[0].cmd("wait %iperf")
	# hosts[1].cmd("wait %iperf")
	
	print 'iperf done'
	# net.build()
	# net.pingAll()
	
	# f = StringIO.StringIO(con1.cmd("ovs-vsctl -f csv list controller"))
	# reader = csv.reader(f, delimiter=',')
	# rownum = 0

	# con66 = []
	# con67 = []
	# for row in reader:
	#     if rownum == 0:
	#         header = row
	#     else:
	#         colnum = 0
	#         for col in row:
	#             # print '%-8s: %s' % (header[colnum], col)
	#             colnum += 1
            
	#         uuid = row[0]
	#         target = row[15]
	#         print uuid, ' cs ', target
	#         if '6666' in target:
	#         	con66.append(uuid)
	#         elif '6667' in target:
	#         	con67.append(uuid)
	#     rownum += 1

	
	# for muid in con66:
	# 	con1.cmd('ovs-vsctl set controller ',muid,'role=slave')

	# for suid in con67:
	# 	con1.cmd('ovs-vsctl set controller ',suid,'role=master')		

	# someInput = raw_input("import pox.openflow.nicira as nx");

	# p1.stdin.write('import pox.openflow.nicira as nx\n')
	# p1.stdin.write('for i in range(0,100):\n')
	# p1.stdin.write('\tprint "au ",i\n')
	# p1.stdin.write('\n')
	CLI(net)
	print 'SET ROLE C1 LEARNING MID '
	p1.stdin.write("import pox.openflow.nicira as nx\n")
	p1.stdin.write("for connection in core.openflow.connections:\n")
	p1.stdin.write("\tconnection.send(nx.nx_role_request(slave='true'))\n")
	p1.stdin.write('\n')
	# p1.stdin.flush()
	# p1.communicate("print 'asy'")
	# p1.stdin.write("\n")
	# p1.stdin.close()
	# print p1.stdout.read()
	
	# time.sleep(5)
	# hosts[0].cmdPrint('ping -c 10',hosts[1].IP())
	# p1.sendSignal(signal.SIGUSR1)
	# p2.sendSignal(signal.SIGUSR1)
	# time.sleep(3)
	# hosts[0].cmdPrint('ping -c 10',hosts[1].IP())
	# time.sleep(4)
	# hosts[0].cmd('ping -c 30',hosts[1].IP())
	# time.sleep(4)
		
	print 'SET ROLE C2 LEARNING MID '
	p2.stdin.write("import pox.openflow.nicira as nx\n")
	p2.stdin.write("for connection in core.openflow.connections:\n")
	p2.stdin.write("\tconnection.send(nx.nx_role_request(master='true'))\n")
	p2.stdin.write('\n')

	CLI(net)
	net.stop()
	print 'stopping pox..'

	# p1.terminate()
	# p2.terminate()


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def getOutput(outQueue):
    outStr = ''
    try:
        while True: #Adds output from the Queue until it is empty
            outStr+=outQueue.get_nowait()

    except Queue.Empty:
        return outStr

if __name__ == '__main__':
	setLogLevel( 'info' )
	
	p1 = subprocess.Popen(['pox/pox.py', "master66"],stdin=subprocess.PIPE, stdout=p1_log,stderr=p1_log,preexec_fn=os.setpgrp)
	print 'c1 runs, master'
	p2 = subprocess.Popen(['pox/pox.py',"slave67"],stdin=subprocess.PIPE, stdout=p2_log,stderr=p2_log,preexec_fn=os.setpgrp)
	print 'c2 runs, slave'

	# print 'wait for 3 seconds...'
	time.sleep(3)
	
	# p1.terminate()
	myNet()

	print 'close pox logs..'
	p1_log.close()
	p2_log.close()

	print 'bye'
	# t.process.terminate()