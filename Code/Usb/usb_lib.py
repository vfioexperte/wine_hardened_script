#!/usr/bin/env python
#Copyright (C) 2021  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#this is a fork from https://github.com/kritzsie/steam-on-docker

version = "0.1a"

import platform
import os
import sys
import string
import subprocess
import time
import math
import json
jason_data = {};

lsusb_temp_file = "/tmp/873264832654893775963457967hsdifhreufgdurbgfkuseb"
tmpfile = "/tmp/lsscsi1i3u45hz835z8345z3-384534875z3485z487"

def system(cmd):
    try:
        #out = subprocess.check_output(cmd, shell=True).decode().split("\n")
        os.system(cmd)
        #return out
    except subprocess.CalledProcessError:
        return []

def system(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True).decode().split("\n");
        return output;
    except subprocess.CalledProcessError:
        return "";
    except FileNotFoundError:
        return "";

def check_device_isopen(filepath):
    try:
        tmp = os.open(filepath, os.O_RDONLY);
        os.close(tmp);
        return 1;
    except PermissionError:
        return 0;
    except TypeError:
        return 0;
    except FileNotFoundError:
        return 0;
    return 1;

def check_device_isopen_hidraw(filepath):
    try:
        tmp = os.open(filepath, os.O_RDONLY);
        os.close(tmp);
        return 1;
    except PermissionError:
        return 1;
    except TypeError:
        return 1;
    except FileNotFoundError:
        return 0;
    return 1;

def read_hidraw_device(suche):
    i = 0;
    dev = [];
    while True:
        if(i >= 100):
            break;
        if(check_device_isopen_hidraw("/dev/hidraw" + str(i)) == 0):
            i = i +1;
            continue;
        try:
            output = subprocess.check_output("/usr/bin/cat < /sys/class/hidraw/hidraw" + str(i) +  "/device/uevent | /usr/bin/grep \"" + suche + "\"", shell=True).decode();
            if(len(output) != 0):
                #system("sudo chmod 700 " + "/dev/hidraw" + str(i));
                dev.append("/dev/hidraw" + str(i));
        except subprocess.CalledProcessError:
            pass;
        i = i +1;
    if(os.path.isfile(tmpfile) == True):
        os.remove(tmpfile);
    return dev;

def read_steam_Controller():
    devs = ["/dev/input/by-id/usb-Valve_Software_Steam_Controller-event-mouse", "/dev/input/by-id/usb-Valve_Software_Steam_Controller-if01-event-joystick", "/dev/input/by-id/usb-Valve_Software_Steam_Controller-if01-joystick", "/dev/input/by-id/usb-Valve_Software_Steam_Controller-mouse"];
    i = 0;
    devices_add = [];
    while True:
        if(i >= len(devs)):
            break;
        if(check_device_isopen(devs[i]) == 1):
            devices_add.append(os.path.realpath(devs[i]));
        i = i +1;
    i = 0;
    while True:
        if(i >= 100):
            break;
        if(check_device_isopen("/dev/input/event" + str(i) == 1)):
            devices_add.append("/dev/input/event" + str(i));
        if(check_device_isopen("/dev/input/js" + str(i) == 1)):
            devices_add.append("/dev/input/js" + str(i));
        if(check_device_isopen("/dev/input/mouse" + str(i) == 1)):
            devices_add.append("/dev/input/mouse" + str(i));
        i = i +1;
    return devices_add;


def usb_pasthrough(name):
    if(name == ""):
        system("lsusb >"+ lsusb_temp_file);
    else:
        system("lsusb | grep \"" + name + "\" >"+ lsusb_temp_file);
    if(os.path.isfile(lsusb_temp_file) == False):
        print("usb_pasthrough() ERROR not find file: lsusb_temp_file: "+ lsusb_temp_file);
        return 0;
    file1 = open(lsusb_temp_file, "r");
    file1.seek(0, 2);
    size = file1.tell();
    file1.seek(0, 0);
    b1 = file1.read(size);
    i = 0;
    bus = [];
    bus_temp = "";
    dev = [];
    dev_temp = "";
    l1 = -1;
    while True:
        if(i >= len(b1)):
            break;
        if(i+ 2 < len(b1) and  (b1[i] == 'B' and b1[i + 1] == 'u') and b1[i + 2] == 's'):
            l1 = 0;
            i = i +3;
        elif(i+ 5 < len(b1) and (b1[i] == 'D' and b1[i + 1] == 'e') and (b1[i + 2] == 'v' and b1[i + 3] == 'i') and (b1[i + 4] == 'c' and b1[i + 5] == 'e')):
            l1 = 1;
            i = i +6;
        elif(l1 == 0):
            if(b1[i] == ' '):
                l1 = -1;
            else:
                bus_temp = bus_temp + b1[i];

        elif(l1 == 1):
            if(b1[i] == ' '):
                l1 = -1;
            elif(b1[i] == ':'):
                l1 = -1;
            else:
                dev_temp = dev_temp + b1[i];
        elif(b1[i] == '\n'):
            if(bus_temp != "" and dev_temp != ""):
                bus.append(bus_temp);
                dev.append(dev_temp);
                bus_temp = "";
                dev_temp = "";
        i = i +1;
    if(os.path.isfile(lsusb_temp_file) == True):
        os.remove(lsusb_temp_file);
    return [bus, dev];
