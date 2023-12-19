import os
import sys

if os.geteuid() != 0:
    sys.exit("Script must be run as root")