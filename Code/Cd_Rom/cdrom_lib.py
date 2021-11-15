#!/usr/bin/env python
#Copyright (C) 2021  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#this is a fork from https://github.com/kritzsie/steam-on-docker

version = "0.1b"

import platform
import os
import sys
import string
import subprocess
import time
import math
import json
jason_data = {};



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


def link_device(device, i):
    abspath = os.path.abspath(sys.argv[0]);
    basename = os.path.basename(abspath);
    dirname = os.path.dirname(abspath);
    scsi_fodler = dirname + "/scsi";
    if(os.path.isdir(scsi_fodler) == False):
        system("mkdir "+ scsi_fodler)
    system("ln -sf " + device + " \"" +scsi_fodler + "/" + str(i)+ "\"");
    return (scsi_fodler + "/" + str(i));


def read_scsi(device_name):
    dev = [];
    dev2 = [];
    sg = [];
    try:
        output = subprocess.check_output("lsscsi -g | grep " + device_name, shell=True).decode().split("\n");
        for tmp in output:
            if(len(tmp) != 0):
                #print(tmp.split())
                scssiport = tmp.split()[0];
                #print(scssiport)
                scssiport = scssiport.split("[")[1].split("]")[0];
                scssiport = "/dev/bsg/" + scssiport;
                dev2.append(scssiport)
                #print(scssiport)
                cdromdev = tmp.split("/dev")[1].split(" ")[0];
                #print(cdromdev)
                cdromdev = "/dev" + cdromdev;
                dev.append(cdromdev)
        i = 0;
        for tmp in dev2:
            sg.append(link_device(tmp, i));
            i = i +1;
        return [dev, sg];
    except subprocess.CalledProcessError:
        return [dev, sg]
    except FileNotFoundError:
        return [dev, sg]


def create_a_cdrom_mount_file_per_dev(devarray, docker_user):
    dev = devarray[0];
    sg = devarray[1];
    if(os.path.isdir("daten/") == False):
        system("mkdir -p daten");
    file1 = open("daten/cdrom.bash", "w");
    file1.write("#!/bin/bash\n");
    file1.write("usermod -aG optical " + docker_user + "\n");
    file1.write("usermod -aG cdemu " + docker_user + "\n");
    i = 0;
    buchstabe = list(string.ascii_lowercase);
    buchstabe_i = 3;
    while True:
        if(i >= len(dev)):
            break;
        if(buchstabe_i >= 26):
            print("ERROR to much cdrom dirve can not patch " + "/mnt/cdrom"+ str(i+1))
            buchstabe_i = buchstabe_i +1;
            i = i +1;
            continue;
        tmp = dev[i];
        tmp2 = sg[i];
        if(i == 0):
            file1.write("ln -sf " + tmp + " /dev/cdrom\n");
        file1.write("mkdir "+ " /mnt/cdrom"+ str(i+1) + "\n");
        file1.write("mount "+ tmp +" /mnt/cdrom"+ str(i+1) + "\n");
        patch_wine_fodler_cdrom(tmp ,"/mnt/cdrom"+ str(i+1), buchstabe[buchstabe_i], tmp2);
        buchstabe_i = buchstabe_i +1;
        i = i +1;
    file1.write("su " + docker_user + "\n");
    file1.close();
    file2 = open("with_cdrom.bash", "w");
    file2.write("#!/bin/bash\n");
    file2.write("./command_root \"/home/empty/daten/cdrom.bash\"\n");
    file2.close();
    abspath = os.path.abspath(sys.argv[0]);
    basename = os.path.basename(abspath);
    dirname = os.path.dirname(abspath);
    system("chmod 777 " + dirname + "/daten/cdrom.bash");
    #system("chmod +x daten/cdrom.bash");
    return 0;


def patch_wine_fodler_cdrom(device, mountpoint, buchstabe, sg):
    #patch wine folder in home user folder home/.wine use cdrom DRM in wine folder
    abspath = os.path.abspath(sys.argv[0]);
    basename = os.path.basename(abspath);
    dirname = os.path.dirname(abspath);
    if(os.path.isdir("home/.wine/dosdevices/") == False):
        return 0;

    print("sg", sg);
    print("buchstabe", buchstabe)
    print("mountpoint", mountpoint)
    #print(device);
    #print(mountpoint);
    #print("ln -sf "+ device + " home/.wine/dosdevices/" + buchstabe + "::");
    system("rm home/.wine/dosdevices/" + buchstabe + "::")
    system("rm home/.wine/dosdevices/" + buchstabe + ":")
    print("ln -sf "+ sg + " home/.wine/dosdevices/" + buchstabe + "::")
    system("ln -sf "+ sg + " home/.wine/dosdevices/" + buchstabe + "::");
    print("ln -sf "+ mountpoint + " home/.wine/dosdevices/" + buchstabe +":");
    system("ln -sf "+ mountpoint + " home/.wine/dosdevices/" + buchstabe +":");
    print("wine fodler gepatch");
    return 0;
