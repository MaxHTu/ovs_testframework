import os
from time import sleep
from datetime import datetime

# Starts ovs-vswitchd and ovsdb-server with valgrind and save the logs to the logs folder
def start_valgrind(log_filename):
    os.system('sudo service openvswitch-switch stop')
    sleep(2)

    #ovsdb_server_logs = 'logs/ovsdb_server.log'
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    ovs_vswitchd_logs = "logs/{}_valgrind_{}.log".format(log_filename, timestamp)

    os.system('sudo valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes --verbose ovsdb-server --remote=punix:/var/run/openvswitch/db.sock --remote=db:Open_vSwitch,Open_vSwitch,manager_options --detach')
    os.system('sudo valgrind --trace-children=yes --leak-check=full --show-leak-kinds=all --track-origins=yes --verbose --log-file={} ovs-vswitchd unix:/var/run/openvswitch/db.sock --detach'.format(ovs_vswitchd_logs))
    
    os.chmod(ovs_vswitchd_logs, 0o666)

    return ovs_vswitchd_logs

# Kills ovs-vswitchd and ovsdb-server process running with valgrind and start ovs-vswitchd normally
def valgrind_cleanup():
    os.system("ps aux | grep '[o]vs-vswitchd' | awk '{print $2}' | xargs -r sudo kill -9")
    os.system("ps aux | grep '[o]vsdb-server' | awk '{print $2}' | xargs -r sudo kill -9")
    
    sleep(2)

    os.system('sudo service openvswitch-switch start')

def set_log_path(log_filename):
    os.system('sudo service openvswitch-switch stop')
    sleep(2)

    ovsdb_server_logs = 'logs/ovsdb_server.log'
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    ovs_vswitchd_logs = "logs/{}_{}.log".format(log_filename, timestamp)

    os.system('sudo ovsdb-server --log-file={} --remote=punix:/var/run/openvswitch/db.sock --remote=db:Open_vSwitch,Open_vSwitch,manager_options --detach'.format(ovsdb_server_logs))
    os.system('sudo ovs-vswitchd --log-file={} unix:/var/run/openvswitch/db.sock --detach'.format(ovs_vswitchd_logs))

    os.chmod(ovs_vswitchd_logs, 0o666)

    return ovs_vswitchd_logs


def reset_log_path():
    os.system("ps aux | grep '[o]vs-vswitchd' | awk '{print $2}' | xargs -r sudo kill -9")
    os.system("ps aux | grep '[o]vsdb-server' | awk '{print $2}' | xargs -r sudo kill -9")
    
    sleep(2)

    os.system('sudo rm logs/ovsdb_server.log')
    os.system('sudo service openvswitch-switch start')


# This is for testing purposes:
if __name__ == '__main__':
    #valgrind = start_valgrind('test')
    #print(valgrind)
    #sleep(10)
    valgrind_cleanup()
    #set_log_path('test')
    #sleep(2)
    reset_log_path()

