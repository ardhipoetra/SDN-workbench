
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

    # Create switches
    s1 = net.addSwitch( 's1', listenPort=6634, mac='00:00:00:00:00:01' )
    s2 = net.addSwitch( 's2', listenPort=6634, mac='00:00:00:00:00:02' )

    print "*** Creating links"
    net.addLink(h1, s1, )
    net.addLink(h2, s2, )   
    net.addLink(s1, s2, )  

    # Add Controllers
    odl_ctrl = net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=cPort1)

    fl_ctrl = net.addController( 'c1', controller=RemoteController, ip='127.0.0.1', port=cPort2)


    net.build()

    # Connect each switch to a different controller
    s1.start( [odl_ctrl, fl_ctrl] )
    s2.start( [odl_ctrl, fl_ctrl] )

    s1.cmdPrint('ovs-vsctl show')

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNet()
