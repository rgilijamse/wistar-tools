#!/usr/bin/env python
"""
This script will apply settings defined in a yaml file to add delay/jitter/loss to Wistar links

"""
import sys
import subprocess
import re
import yaml

WAN_FILE = sys.argv[1]

# load variables from yaml file specified als argument
BRIDGES = dict()
with open(WAN_FILE, "r") as ymlfile:  # this would require some error handling
    BRIDGES.update(yaml.load(ymlfile))

for bridge in BRIDGES['bridges']:
    # find nics in the bridge
    command = "brctl show " + bridge['name']
    BR_INFO = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
    # regex creates a list of only the vnet nic names
    NICS = re.findall('(vnet[0-9]+?)', BR_INFO, re.DOTALL)

    # set wan profile
    if 'latency' in bridge:
        delay = "delay " + str(bridge['latency']) + "ms "
    else:
        delay = ""
    if 'jitter' in bridge:
        jitter = str(bridge['jitter']) + "ms distribution normal "
    else:
        jitter = ""
    if 'loss' in bridge:
        loss = "loss " + str(bridge['loss']) + "% "
    else:
        loss = ""
    if 'corrupt' in bridge:
        corrupt = "corruption " + str(bridge['corrupt']) + "% "
    else:
        corrupt = ""

    profile = delay + jitter + loss + corrupt

    # log to commandline
    print("applying " + profile + " to bridge " + bridge['name'])

    # iterate over nics
    for nic in NICS:
        line = "tc qdisc add dev " + nic + " " + profile
        # apply config
        subprocess.call(line, shell=True)
