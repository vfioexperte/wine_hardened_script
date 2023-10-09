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

def docker_run_to_docker_compose(bash_args):
    out = "version: \"3.0\"\n";
    out = out + "services:\n";
    out = out + "\tapp:\n";
    out = out + "image: ubuntu:latest\n";
    out = out + "network_mode: bridge\n";
    ports = [];
    envirement = [];
    volumes = [];
    dns_server = [];
    devices = [];
    group_add = [];
    i = 0;
    while True:
        if(i >= len(bash_args)):
            break;
        tmp = bash_args[i];
        if(tmp == "-p"):
            i = i + 1;
            tmp = bash_args[i];
            ports.append(tmp)
        elif(tmp == "-e"):
            i = i + 1;
            tmp = bash_args[i];
            envirement.append(tmp)
        elif(tmp == "-v"):
            i = i + 1;
            tmp = bash_args[i];
            volumes.append(tmp)
        elif(tmp == "--dns"):
            i = i + 1;
            tmp = bash_args[i];
            dns_server.append(tmp)
        elif(tmp == "docker"):
            pass;
        elif(tmp == "--privileged"):
            pass;
        elif(tmp == "-h"):
            i = i + 1;
            tmp = bash_args[i];
            out = out + "\thostname:\n";
            out = out + "\t\t" + tmp + "\n";
        elif(tmp == "--device"):
            i = i + 1;
            tmp = bash_args[i];
            devices.append(tmp)
        else:
            print(tmp)
            exit(-1);
        i = i + 1;

    if(len(ports) >= 1):
        out = out + "\tports:\n"
        for tmp in ports:
            out = out + "\t\t" + tmp + "\n";

    if(len(envirement) >= 1):
        out = out + "\tenvirement:\n"
        for tmp in envirement:
            out = out + "\t\t" + tmp + "\n";

    if(len(volumes) >= 1):
        out = out + "\tvolumes:\n"
        for tmp in volumes:
            out = out + "\t\t" + tmp + "\n";

    if(len(devices) >= 1):
        out = out + "\tdevices:\n"
        for tmp in devices:
            out = out + "\t\t" + tmp + "\n";

    if(len(dns_server) >= 1):
        out = out + "\tdns:\n"
        for tmp in dns_server:
            out = out + "\t\t" + tmp + "\n";
    f1.write("docker-compose.yml", "w");
    f1.write(out);
    f1.close();
    exit()
    print(out);
    return out;
