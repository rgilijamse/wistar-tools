#!/usr/bin/env python
"""
Small hack to iterate over all Wistar bridges and enable LLDP/LACP (see https://github.com/Juniper/wistar/issues/12)
"""

import subprocess
import re

BR_INFO = subprocess.Popen("ifconfig | grep t1_br", shell=True, stdout=subprocess.PIPE).stdout.read() # returns all bridges that contain t1_br
BRIDGES = re.findall('(t1_br.*?) ', BR_INFO, re.DOTALL) # regex creates a list of only the bridge names

for bridge in BRIDGES:
  command = "echo 65535 > /sys/class/net/" + bridge + "/bridge/group_fwd_mask"
  subprocess.call(command, shell=True)
