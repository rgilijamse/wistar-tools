# Wistar tools

Tools to tune [wistar](https://github.com/Juniper/wistar/) according to my specifications:

* Apache2 frontend
* EVE-NG kernel (with LACP hack and UKMS)

## Installation

Install wistar using these commands:

```bash
apt-get install ansible
ansible-playbook install-wistar.yml
```

This works (tested) with Ubuntu 16.04 LTS.

## LLDP/LACP fix

After deploying a topology you can enable LLDP and LACP/STP frames by running this python script:

```bash
sudo ./fix_bridges.py
```