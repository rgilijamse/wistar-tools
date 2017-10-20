#!/usr/bin/env python
"""
Small hack to iterate over all Wistar bridges and enable LLDP/LACP
(see https://github.com/Juniper/wistar/issues/12)
"""

import subprocess
import re

# return all bridges that contain _br*
BR_INFO = subprocess.Popen("ifconfig | grep _br", shell=True, stdout=subprocess.PIPE).stdout.read()
# regex creates a list of only the bridge names
BRIDGES = re.findall('(t[0-9]+_br[0-9]+?) ', BR_INFO, re.DOTALL)

for bridge in BRIDGES:
    print("fixing bridge " + bridge)
    command = "echo 65535 > /sys/class/net/" + bridge + "/bridge/group_fwd_mask"
    subprocess.call(command, shell=True)
