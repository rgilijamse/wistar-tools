# Wistar tools
Tools om [wistar](https://github.com/Juniper/wistar/) te installeren volgens mijn eigen specificaties:
* Apache2 frontend
* EVE-NG kernel (met LACP hack en UKMS)

## Installatie
Installeer wistar met de volgende commando's:

```bash
apt-get install ansible
ansible-playbook install-wistar.yml
```

Dit werkt (getest) met Ubuntu 16.04 LTS.

## LLDP/LACP fix
Na deployen van een topologie kan je LLDP en LACP fixen door het onderstaande pythonscript te draaien:
```bash
./fix_bridges.py
```