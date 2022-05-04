#!/usr/bin/env python3
#Copyright (C) 2022  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#this is a fork from https://github.com/kritzsie/steam-on-docker
#start project 13.03.2022

import platform
import os
import sys
import string
import subprocess
import time

#last edit 04.05.2022

version = "0.1b"
appname = "docker install script"

abspath = os.path.abspath(sys.argv[0])
basename = os.path.basename(abspath)
dirname = os.path.dirname(abspath)

def system(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True).decode().split("\n");
        return output;
    except subprocess.CalledProcessError:
        return "";
    except FileNotFoundError:
        return "";

def intsall(config):
    system("chmod +x build");
    system("ln -sf build login_root");
    system("ln -sf build login");
    system("ln -sf build run");
    system("ln -sf build openra-ra");
    system("ln -sf build firefox");
    system("ln -sf build command");
    system("ln -sf build command_root");
    system("ln -sf build edit_config");
    system("ln -sf build manager");
    sdir = os.path.join(dirname, "archlinux_std_docker", "archlinux_std_docker_big", "archlinux_std_docker");
    os.chdir(sdir);
    #cd archlinux_std_docker/archlinux_std_docker_big/archlinux_std_docker/
    system("ln -sf ../../../build build");
    system("ln -sf ../../../Code Code");
    system("cp ../../../hidraw_acs_overrides_patch.py hidraw_acs_overrides_patch.py");
    system("cp ../../../chmod_check.py chmod_check.py");
    system("cp ../../../pacman.conf pacman.conf");
    system("cp ../../../mirrorlist mirrorlist");
    if(config == 0):
        system("cp config_file_json_big config_file_json");
    elif(config == 1):
        system("cp config_file_json_min config_file_json");
    else:
        system("cp config_file_json_big config_file_json");
    system("ln -sf build login");
    system("ln -sf build manager");
    system("ln -sf build edit_config");
    os.system("./manager");
    os.system("./edit_config");
    sdir2 = os.path.join(sdir, "archlinux_std_docker");
    os.chdir(sdir2);
    system("ln -sf build login");
    system("ln -sf build manager");
    system("ln -sf build edit_config");
    system("chmod +x build");
    os.chdir(dirname);
    return 0;

def main():
    while True:
        s1 = input("config big[0] or config min[1]?");
        if(s1 == "0"):
            intsall(0);
            exit();
        elif(s1 == "1"):
            intsall(1);
            exit();
        else:
            print("ERROR wrong input!");

main();
