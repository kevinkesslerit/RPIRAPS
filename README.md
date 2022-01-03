# RPiRAPS
## Raspberry Pi Rogue Access Point Script


This project was made for Raspbian GNU/Linux 11 (bullseye) Tested on Ubuntu 20.04, Raspberry Pi OS (bullseye).

### Required modules
netifaces <br />
errno <br />
shutil <br />
subprocess <br />
sys <br />
os

### Setup
`sudo python3 setup.py` <br />
From here you'll choose your network interfaces and go through the install process.

### Configurations -- BEFORE YOU RUN
You'll need to edit the three (3) configuration files in the root RPiRAPS folder. dnsmasq.conf, dhcpcd.conf, and hostapd.conf.
These files need their interface changed to the interface you wish to use as your output. This could be a name like wlan0, or (as I recommend, use predictable iface names)


That's it. This project could also be used as a repeater with a WPA2 AP. Just set that up in hostapd. (It's currently commented out for convenience)