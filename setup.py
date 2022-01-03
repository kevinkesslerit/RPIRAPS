#!/usr/bin/env python3
from subprocess import STDOUT, check_call, call, run
import os, errno, sys, netifaces
from shutil import copy

# Check for root access
if os.geteuid() != 0:
    exit("Must be root!")

# GLOBALS #

#Packages installed?


#pre-req. packages
packages = ["dhcpcd", "hostapd"]
#dnsmasq is broken for "which" command, add later.


# Functions

def configure(dhcpcd, dnsmasq, hostapd):
    #rename old config files.

    #rename and install dhcpcd
    if dhcpcd == True:
        print ("Backing up /etc/dhcpcd.conf")
        os.rename("/etc/dhcpcd.conf", "/etc/dhcpcd.conf.bak")
    elif dhcpcd == False:
        #Install it!
        print ("Checking for package: dhcpcd5...")
        check_call(['apt', 'install', '-y', 'dhcpcd5'],
    stdout=open(os.devnull,'wb'), stderr=STDOUT)

    #rename and install dnsmasq
    #need a better way to check for dnsmasq installation.
    if dnsmasq == True:
        print ("Backing up /etc/dnsmasq.conf")
        os.rename("/etc/dnsmasq.conf", "/etc/dnsmasq.conf.bak")
    elif dnsmasq == False:
        #Install it!
        print ("Checking for package: dnsmasq...")
        check_call(['apt', 'install', '-y', 'dnsmasq'],
     stdout=open(os.devnull,'wb'), stderr=STDOUT)

    #rename and install hostapd
    if hostapd == True:
        print ("Backing up /etc/hostapd/hostapd.conf")
        os.rename("/etc/hostapd/hostapd.conf", "/etc/hostapd/hostapd.conf.bak")
    elif hostapd == False:
        #Install it!
        print ("Checking for package: hostapd...")
        check_call(['apt', 'install', '-y', 'hostapd'],
     stdout=open(os.devnull,'wb'), stderr=STDOUT)

    print ("Copying configuration files...")
    try:
        copy("dhcpcd.conf", "/etc/dhcpcd.conf")
    except:
        print("No config file for dhcpcd found.")

    try:
        copy("dnsmasq.conf", "/etc/dnsmasq.conf")
    except:
        print("No config file for dnsmasq found.")

    try:
        copy("hostapd.conf", "/etc/hostapd/hostapd.conf")
    except:
        print("No config file for hostapd found.")

def check_packages():
    #use which to check for installed packages.
    dhcpcd = False
    dnsmasq = False
    hostapd = False
    for package in packages:
        retVal = call(["which", package ])
        # 0 = installed
        if retVal == 0:
            #not using match case yet.
            if package  == "dhcpcd":
                dhcpcd = True
                print ("Skipping install of " + package)
            #if package  == "dnsmasq":
                #dnsmasq = True
                #print ("Skipping install of " + package)
                #dnsmasq does not actually fully uninstall,so we will try to install each time.
            if package  == "hostapd":
                hostapd = True
                print ("Skipping install of " + package)
    configure(dhcpcd, dnsmasq, hostapd)

#grab interfaces, and let user grab them by # choice.
def nftables():
    print("Available interfaces:")
    print(netifaces.interfaces())
    out_iface = input("Choose interface that users will connect to (output/rogue):")
    print (out_iface)
    in_iface = input("Choose interface that will forward internet (input/real):")
    run("nft add table nat", shell=True)
    run("nft 'add chain nat postrouting { type nat hook postrouting priority 100; }'", shell=True)
    run("nft add rule ip nat postrouting oifname \""+ in_iface +"\" masquerade", shell=True)
    run("nft add table ip filter", shell=True)
    run("nft 'add chain ip filter forward { type filter hook forward priority 0; policy accept; }'", shell=True)
    run("nft add rule ip filter forward iifname \""+ in_iface +"\" oifname \""+ out_iface +"\" ct state related,established  accept", shell=True)
    run("nft add rule ip filter forward iifname \""+ out_iface +"\" oifname \""+ in_iface +"\" accept", shell=True)
#init
check_packages()
nftables()