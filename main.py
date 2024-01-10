import os
import sys
import tests
from datetime import datetime

def get_functions():
    list_cve = [func for func in dir(tests) if callable(getattr(tests, func)) and func.startswith('cve_')]
    indexing = {str(index + 1): func for index, func in enumerate(list_cve)}
    return indexing

def get_ovs_version():
    output = os.popen('ovs-vsctl --version').read()
    ovs_version = output.split()[3]
    return ovs_version

def start_tests():
    all_cve = get_functions()

    print('Available CVE Tests')
    for num, cve in all_cve.items():
        print('{}. {}'.format(num, cve))

    usr_input = input("Enter the number(s) of the CVE test(s) to run (e.g. 1 or 1,2,3 or 'all'): ")
    
    test_results = {}
    if usr_input == 'all':
        for cve in all_cve.values():
            print('Running {}...'.format(cve))
            func = getattr(tests, cve)
            func()
            test_results[cve] = func()
    else:
        usr_input = usr_input.split(',')
        for num in usr_input:
            num = num.strip()
            if num in all_cve.keys():
                print('Running {}...'.format(all_cve[num]))
                func = getattr(tests, all_cve[num])
                func()
                test_results[all_cve[num]] = func()
            else:
                print("Invalid input. Please enter valid number(s) separated by commas or 'all'.")
                sys.exit(1)

    return test_results

def main():

    if os.geteuid() != 0:
        sys.exit("This Script must be run as root")

    ovs_version = get_ovs_version()
    print('Current Open vSwitch version: {}'.format(ovs_version))
    test_results = start_tests()

    folder_path = 'test_results'
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_filename = 'test_results_{}.log'.format(timestamp)

    log_file_path = os.path.join(folder_path, log_filename)

    print('Test Results:')

    with open(log_file_path, 'w') as log_file:
        log_file.write('Open vSwitch version: {}\n'.format(ovs_version))
        for test, result in test_results.items():
            result_text = "vulnerable: {}".format('true' if result else 'false')
            print('{} {}'.format(test, result_text))
            log_file.write('{} {}\n'.format(test, result_text))


if __name__ == '__main__':
    main()