import os
import sys
import tests

# Checks if the script is run as root
if os.geteuid() != 0:
    sys.exit("This Script must be run as root")

def main():
    tests.cve_2016_10377()

if __name__ == '__main__':
    main()