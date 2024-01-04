import os
from time import sleep
from datetime import datetime

def start_valgrind(log_filename):
    os.system('sudo service openvswitch-switch stop')
    sleep(2)

    #ovsdb_server_logs = '../logs/ovsdb_server.log'
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    ovs_vswitchd_logs = f'../logs/{log_filename}_{timestamp}.log'

    os.system('sudo valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes --verbose ovsdb-server --remote=punix:/var/run/openvswitch/db.sock --remote=db:Open_vSwitch,Open_vSwitch,manager_options --detach')
    os.system(f'sudo valgrind --trace-children=yes --leak-check=full --show-leak-kinds=all --track-origins=yes --verbose --log-file={ovs_vswitchd_logs} ovs-vswitchd unix:/var/run/openvswitch/db.sock --detach')

def valgrind_cleanup():
    os.system("ps aux | grep '[o]vs-vswitchd' | awk '{print $2}' | xargs -r sudo kill -9")
    os.system("ps aux | grep '[o]vsdb-server' | awk '{print $2}' | xargs -r sudo kill -9")
    
    sleep(2)

    os.system('sudo service openvswitch-switch start')

# This is for testing purposes:
if __name__ == '__main__':
    start_valgrind('test')
    sleep(10)
    valgrind_cleanup()