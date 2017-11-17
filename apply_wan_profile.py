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
    if 'rate' in bridge:
        rate = str(bridge['rate']) + "kbit burst 15k limit 15k"
    else:
        rate = ""

    profile = delay + jitter + loss + corrupt

    # iterate over nics
    for nic in NICS:
        # assemble settings
        settings = []
        if profile:
            settings.append("netem " + profile)
        if rate:
            settings.append("tbf rate " + rate)

        # apply base profile
        base_profile = "tc qdisc add dev " + nic + " root handle 1: prio"
        print("applying WAN profle to bridge " + bridge['name'] + ":")
        subprocess.call(base_profile, shell=True)

        # apply WAN profile
        for nr, line in enumerate(settings):
            print("-> apply " + line + " to " + nic)
            profile_line = "tc qdisc add dev " + nic + " parent 1:" + str(nr+1) + " " + line
