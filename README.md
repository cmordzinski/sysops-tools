# sysops-tools

This repository aims to show the general ansible structure I am familiar with when managing configurations with ansible. 
Obviosuly, this repository is pretty bare bones and is more meant to serve as an example than anything else.

* ansible - main ansible directory, inventory, roles, etc live here
* bin - scripts that will get synced to /opt/adm/bin and added to system wide path. Typically shell scripts, or wrapper scripts to call python code in the tools dir.
* sbin - scripts that will get synced to /opt/adm/sbin. Typically shell scripts, or wrapper scripts to call python code in the tools dir.
* tools - python code that will get synced to /opt/adm/tools. Scripts in this directory will typically be invoked by a wrapper script located in /opt/adm/bin or /opt/adm/sbin.
