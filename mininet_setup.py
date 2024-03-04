import os
from time import sleep
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info


class MininetNetwork:

    def __init__(self):
        self.net = None

    # Mininet setup with 2 hosts and 1 switch
    def mininet_2h_1s(self):
        self.net = Mininet()

        #self.net.addController('c0', controller=Controller)

        h1 = self.net.addHost('h1', ip='10.0.0.1', mac='00:00:00:00:00:01')
        h2 = self.net.addHost('h2', ip='10.0.0.2', mac='00:00:00:00:00:02')
        s1 = self.net.addSwitch('s1')

        self.net.addLink(h1, s1)
        self.net.addLink(h2, s1)

        self.net.start()
        self.flow_rules(s1)
    
        #CLI(self.net)

    # Mininet setup with 1 host and 1 switch
    def mininet_1h_1s(self):
        self.net = Mininet()

        #self.net.addController('c0', controller=Controller)
    
        h1 = self.net.addHost('h1', ip='10.0.0.1', mac='00:00:00:00:00:01')
        s1 = self.net.addSwitch('s1')

        self.net.addLink(h1, s1)

        self.net.start()
        self.flow_rules(s1)
        #CLI(self.net)

    def flow_rules(self, bridge):
        os.system("sudo ovs-ofctl del-flows {}".format(bridge))
        # os.system("sudo ovs-ofctl add-flow {} priority=0,actions=CONTROLLER".format(bridge))
        os.system("sudo ovs-ofctl add-flow {} priority=0,actions=NORMAL".format(bridge))

    # Stops Mininet
    def stop_mininet(self):
        if self.net:
            self.net.stop()

    # Cleans up the network and the controller
    def cleanup_network(self):
        os.system('sudo mn -c')
        os.system('sudo fuser -k 6653/tcp')

# This is for testing purposes:
if __name__ == '__main__':
    setLogLevel('info')

    mininet = MininetNetwork()
    #mininet.mininet_1h_1s()
    #mininet.mininet_2h_1s() 
    #sleep(5)
    mininet.stop_mininet()
    mininet.cleanup_network()