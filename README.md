# sysops-tools

This repository aims to show the general ansible structure I am familiar with using when managing configurations with ansible, obviously it is very bare bones and is more meant to serve as an example than anything else.

* ansible
* bin - shell scripts that will get synced to /opt/adm/bin and added to system wide path
* sbin - shell scripts that will get synced to /opt/adm/sbin
* tools - python code that will get synced to /opt/adm/tools. Scripts in this directory will typically be invoked by a wrapper script located in /opt/adm/bin or /opt/adm/sbin.
