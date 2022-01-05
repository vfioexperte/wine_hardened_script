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


def patching_user(docker_user, command, id):
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
    #steam fix PWD 1
    s2 = s2 + "export PWD=/home/" + docker_user + "\n";
    #s2 = "chown -R "+ docker_user +":users /home/" + docker_user + "\n";
    s2 = s2 + "chown -R root:video /dev/dri\n";
    s3 = "";
    if(command != ""):
        s3 = command + "\n";
    else:
        s3 = "su - " + "\n";
    file1 = open("user_patched.bash", "w");
    file1.write(s0);
    file1.write(s1);
    file1.write(s2);
    file1.write(s3);
    file1.close();
    print("patching_user ok");
    patching_pulse_audio_config(id);
    system("chmod +x user_patched.bash");
    return 0;