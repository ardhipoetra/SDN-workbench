
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def myNet():
    cPort1=6666
    cPort2=6667

    net = Mininet( topo=None, build=False)

    # Create nodes
    h1 = net.addHost( 'h1', mac='01:00:00:00:01:00', ip='192.168.0.1/24' )
    h2 = net.addHost( 'h2', mac='01:00:00:00:02:00', ip='192.168.0.2/24' )
    h3 = net.addHost( 'h3', mac='01:00:00:00:03:00', ip='192.168.0.3/24' )
    h4 = net.addHost( 'h4', mac='01:00:00:00:04:00', ip='192.168.0.4/24' )

    # Create switches
    s1 = net.addSwitch( 's1', listenPort=6634, mac='00:00:00:00:00:01' )
    s2 = net.addSwitch( 's2', listenPort=6634, mac='00:00:00:00:00:02' )
    s3 = net.addSwitch( 's3', listenPort=6634, mac='00:00:00:00:00:03' )
    s4 = net.addSwitch( 's4', listenPort=6634, mac='00:00:00:00:00:04' )

    print "*** Creating links"
    net.addLink(h1, s1, )
    net.addLink(h2, s2, )
    net.addLink(s1, s2, )
    net.addLink(s2, s3, )
    net.addLink(h3, s3, )
    net.addLink(h4, s4, )
    net.addLink(s3, s4, )

    # Add Controllers
    con1 = net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=cPort1)
    con2 = net.addController( 'c1', controller=RemoteController, ip='127.0.0.1', port=cPort2)


    net.build()

    # Connect each switch to a different controller
    s1.start( [con1] )
    s2.start( [con1] )
    s3.start( [con2] )
    s4.start( [con2] )

    # s1.cmdPrint('ovs-vsctl show')

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNet()
