#!/usr/bin/env python
#Copyright (C) 2022  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#this is a fork from https://github.com/kritzsie/steam-on-docker

version = "0.3d"
#0.3d add new file /etc/user_patched2.bash and fix faketime 0.1a

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

def patching_pulse_audio_config(id):
    s0 = "#version 0.1\n"
    s1 = "default-server = unix:/run/user/" + id + "/pulse/native\n";
    s2 = "autospawn = no\n";
    s3 = "daemon-binary = /bin/true\n";
    s4 = "enable-shm = false\n"
    file1 = open("pulse-client.conf", "w");
    file1.write(s0);
    file1.write(s1);
    file1.write(s2);
    file1.write(s3);
    file1.write(s4);
    file1.close();
    print("patching_pulse_audio_config ok");
    return 0;


def patching_user(docker_user, command2, command, id, hidraw_acs_overrides_patch, ipv6_privacy, faketime, wine_32bit_speed_hak):
    s0 = "#!/bin/bash\n#version=0.1\n";
    s1 = "usermod -u "+ id + " "  + docker_user + "\n";
    s1 = s1 + "usermod -aG input " + docker_user + "\n";
    s1 = s1 + "usermod -aG optical " + docker_user + "\n";
    s1 = s1 + "usermod -aG cdemu " + docker_user + "\n";
    s1 = s1 + "usermod -aG video " + docker_user + "\n";
    s1 = s1 + "usermod -aG audio " + docker_user + "\n";
    s1 = s1 + "usermod -aG render " + docker_user + "\n";
    #freesync patch vsync on
    s1 = s1 + "export vblank_mode=3" + "\n";
    s1 = s1 + "echo 'vblank_mode=3' >> /etc/environment" + "\n";
    #s1_2 = "rm /dev/input/* \n";
    #s1 = s1  + s1_2;
    s2 = "/root/chmod_check.py '" + docker_user + "' '" + id + "' \n";
    if(hidraw_acs_overrides_patch == 1):
        s2 = s2 + "/root/hidraw_acs_overrides_patch.py\n";
    if(ipv6_privacy >= 1):
        s2 = s2 + "sysctl net.ipv6.conf.eth0.use_tempaddr=2\n"
    if(ipv6_privacy == 2):
        s2 = s2 + "sysctl net.ipv6.conf.all.use_tempaddr=2\n"
    if(wine_32bit_speed_hak == 1):
        s2 = s2 + "sysctl -w abi.vsyscall32=0\n"
    #steam fix PWD 1
    s2 = s2 + "export PWD=/home/" + docker_user + "\n";
    #s2 = "chown -R "+ docker_user +":users /home/" + docker_user + "\n";
    s2 = s2 + "chown -R root:video /dev/dri\n";
    s3 = "";
    if(faketime != ""):
        if(command == "su"):
            s3 = s3 + "/usr/bin/faketime --exclude-monotonic \"" + faketime + "\" bash /etc/user_patched2.bash";
        else:
            if(command2 == ""):
                s3 = s3 + "/usr/bin/faketime --exclude-monotonic \"" + faketime + "\" bash /etc/user_patched2.bash";
            else:
                s3 = s3 + "su " + docker_user + " - -c 'FAKETIME_DONT_RESET=1 FAKETIME=\"" + faketime + "\" LD_PRELOAD=/usr/lib/faketime/libfaketime.so.1 bash -c /etc/user_patched2.bash'";
    else:
        if(command == "su"):
            s3 = s3 + "bash /etc/user_patched2.bash";
        else:
            if(command2 == ""):
                s3 = s3 + "bash /etc/user_patched2.bash";
            else:
                s3 = s3 + "su " + docker_user + " - -c 'bash /etc/user_patched2.bash'";

    s4 = "#!/bin/bash\n#version=0.1\n";
    if(command2 != ""):
        s4 = s4 + command + "\n";
    else:
        s4 = s4 + command + "\n";
    file1 = open("user_patched.bash", "w");
    file1.write(s0);
    file1.write(s1);
    file1.write(s2);
    file1.write(s3);
    file1.close();
    file1 = open("user_patched2.bash", "w");
    file1.write(s4);
    file1.close();
    print("patching_user ok");
    patching_pulse_audio_config(id);
    system("chmod +x user_patched.bash");
    system("chmod +x user_patched2.bash");
    return 0;



def listpath(path, rpath, array, idarray, patharray, ctime):
        #File list
        j = array[0];
        sdir = array[1];
        list = os.listdir(path)
        size = len(list);
        sout = "";
        i = 0;
        if(size == 0):
            return [j, sdir, idarray, patharray, ctime];
        while True:
            spath = path + "/" + list[i];
            if(os.path.islink(spath) == True):
                i = i+ 1;
                j = j +1;
                if( i== size):
                    break;
            elif(os.path.isdir(spath) == True):
                rpath2 = rpath + "/" + list[i];
                i =  i+1;
                array = [j, sdir];
                array = listpath(spath, rpath2, array, idarray, patharray, ctime);
                idarray = array[2];
                patharray = array[3];
                ctime = array[4];
                j = array[0];
                sdir = array[1];
                if( i== size):
                    break;
            else:
                sdir = sdir + "ID: " + str(j) + " | " + rpath + "/" + list[i] + "\n";
                idarray.append(j);
                s1 = rpath + "/" + list[i];
                patharray.append(s1);
                ctime.append("");
                i = i+ 1;
                j = j +1;
                if( i== size):
                    break;
        return [j, sdir, idarray, patharray, ctime]

def device_folder_passthrough(folder, base_args):
    array = [0, ""];
    array = listpath(folder, "", array, [], [], [])
    patharray = array[3];
    for tmp in patharray:
        base_args.append("--device")
        base_args.append(folder + tmp)
    return base_args;
