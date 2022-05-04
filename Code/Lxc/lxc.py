#!/usr/bin/env python
#Copyright (C) 2022  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#this is a fork from https://github.com/kritzsie/steam-on-docker

version = "0.1d hotfix 10 lxc"

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



def read_all_cups():
    out = system("cat /proc/cpuinfo | grep 'Processor'")
    return len(out) -1;

def kilobyte_to_kibibyte(int1):
    j = 0;
    bak1 = int1;
    while True:
        if(bak1 >= 1024):
            bak1 = bak1 / 1024;
            j = j +1;
        else:
            break;
    bak2 = bak1;
    for i in range(j):
        bak2 = round(bak2 * 1000);
    return bak2;


def read_memory_infos():
    out = system("cat /proc/meminfo | grep 'MemTotal:' ")
    return round(kilobyte_to_kibibyte(int(out[0].split()[1])) -  5000000);

def create_xml_vm_file(mount, name, cpus, memorylimt, brigenetwork, mac, tty, docker_build):
    #is old
    f1 = open("1.xml", "w");
    f1.write('<domain type="lxc">\n');
    f1.write("\t<name>" + docker_build + "</name>\n");
    f1.write("\t<uuid>86211112-1111-1122-1111-123456789012</uuid>\n");
    if(memorylimt == -1):
        memorylimt = read_memory_infos();
    f1.write('\t<memory unit="KiB">' + str(memorylimt) +  '</memory>\n');
    if(cpus == -1):
        cpus = read_all_cups();
    f1.write('\t<vcpu placement="static">' + str(cpus) + '</vcpu>\n');
    ##
    f1.write("\t<os>\n");
    f1.write('\t\t<type arch="x86_64">exe</type>\n');
    f1.write('\t\t<init>/bin/bash</init>\n');
    f1.write('\t\t<initarg>/root/user_patched.bash</initarg>\n');
    f1.write("\t</os>\n");
    f1.write('\t<features>\n');
    f1.write('\t\t <privnet/>\n');
    f1.write('\t</features>\n');
    f1.write('\t<on_poweroff>destroy</on_poweroff>\n');
    f1.write('\t<on_reboot>restart</on_reboot>\n');
    f1.write('\t<on_crash>destroy</on_crash>\n');

    f1.write('\t<devices>\n')
    for tmp in mount:
        tmp2 = tmp.split(":");
        dir = 1;
        if(os.path.isdir(tmp2[0]) == False):
            dir = 0;
        if(dir == 1):
            f1.write('\t\t<filesystem type="mount" accessmode="mapped">\n');
        else:
            f1.write('\t\t<filesystem type="file" accessmode="mapped">\n')
        f1.write('\t\t\t<source dir="' + tmp2[0] + '"/>\n');
        if(len(tmp2) >= 2):
            f1.write('\t\t\t<target dir="' + tmp2[1] + '"/>\n');
        else:
            f1.write('\t\t\t<target dir="' + tmp2[0] + '"/>\n')
        if(len(tmp2) >= 3):
            if(tmp2[2] == "ro"):
                f1.write('\t\t\t<readonly/>\n');
        f1.write('\t\t</filesystem>\n');

    if(brigenetwork == ""):
        f1.write('\t\tlxc.network.type=empty\n');
    if(brigenetwork == "0"):
        brigenetwork = "br0"
    f1.write('\t\t<interface type="bridge">\n');
    if(mac != ""):
        f1.write('\t\t\t<mac address="' + mac + '"/>\n');
    f1.write('\t\t\t<source bridge="' + brigenetwork +  '"/>\n');
    f1.write('\t\t</interface>\n');

    if(tty == 1):
        f1.write('\t\t<console type="pty">\n');
        f1.write('\t\t\t<target type="lxc" port="0"/>\n');
        f1.write('\t\t</console>\n')

    f1.write("\t</devices>\n");
    f1.write('</domain>\n');
    f1.close();
    return 0;


def array_add_aarray(array1, addarraay):
    for tmp in addarraay:
        array1.append(tmp);
    return array1;

def applay_path(paths, dockername, vars, ttyon, dirname, staticip, lxc_readonly, network_disable, lxc_network_mac, dns, build_b1, paths2):
    if(os.path.isfile("/var/lib/lxc/" + dockername +"/config") == False):
        print("applay_path error fiel not found!");
        return 0;

    f1 = open("/var/lib/lxc/" + dockername +"/config", "w");
    f1.write("lxc.include = /usr/share/lxc/config/common.conf\n");
    f1.write("lxc.include = /usr/share/lxc/config/userns.conf\n");
    f1.write("lxc.mount.entry = tmpfs tmp tmpfs defaults\n​");
    f1.write("lxc.arch = x86_64\n");

    #f1.write("lxc.rootfs.path = dir:/var/lib/lxc/" +dockername+ "/rootfs\n");

    f1.write("lxc.mount.entry = " + dirname + "/tmp " + "etc/sharfolder" + " none bind,optional,create=dir,rw\n");
    for tmp in paths2:
        #paths2 prio 2
        if(tmp.find(":") == -1):
            if(os.path.isdir(tmp) == True):
                f1.write("lxc.mount.entry = " + tmp + " " + (tmp[1::]) + " none bind,optional,create=dir,rw\n");
            else:
                f1.write("lxc.mount.entry = " + tmp + "  " + (tmp[1::]) + " none bind,optional,create=file,rw\n");
        else:
            s1 = tmp.split(":");
            if(len(s1) == 2):
                if(os.path.isdir(s1[0]) == True):
                    f1.write("lxc.mount.entry = " + s1[0] +"  " +  (s1[1][1::]) + " none bind,optional,create=dir,rw\n");
                else:
                    f1.write("lxc.mount.entry = " + s1[0] +"  " +  (s1[1][1::]) + " none bind,optional,create=file,rw\n");
            elif(len(s1) == 3):
                if(s1[2] == "rw"):
                    if(os.path.isdir(s1[0]) == True):
                        f1.write("lxc.mount.entry = " + s1[0] +"  " +  (s1[1][1::]) + " none bind,optional,create=dir,rw\n");
                    else:
                        f1.write("lxc.mount.entry = " + s1[0] +"  " +  (s1[1][1::]) + " none bind,optional,create=file,rw\n");
                if(s1[2] == "ro"):
                    if(os.path.isdir(s1[0]) == True):
                        f1.write("lxc.mount.entry = " + s1[0] +"  " +  (s1[1][1::]) + " none bind,optional,create=dir,ro\n");
                    else:
                        f1.write("lxc.mount.entry = " + s1[0] +"  " +  (s1[1][1::]) + " none bind,optional,create=file,ro\n");

    #f1.write("lxc.rootfs.backend = dir\n");
    #f1.write("lxc.mount.entry = "  +  "/var/lib/lxc/" +dockername+ "/rootfs " + " none bind,optional,create=dir,ro\n")

    #f1.write("lxc.mount.entry = " + "/var/lib/lxc/" +dockername+ "/rootfs" + "  none bind,optional,create=dir,rw\n");
    #f1.write("lxc.mount.entry = " + "/proc /proc none bind,optional,create=dir,ro\n");

        #f1.write("lxc.rootfs.options = rw\n");
    f1.write("lxc.uts.name = " +dockername+ "\n");
    if(network_disable == 0):
        f1.write("lxc.net.0.type = veth\n");
        f1.write("lxc.net.0.link = br0\n");
        #f1.write("lxc.net.0.flags = up\n");
        if(lxc_network_mac == ""):
            pass;
        else:
            f1.write("lxc.net.0.hwaddr = " + lxc_network_mac +"\n");
        if(staticip != ""):
            f1.write("lxc.net.0.ipv4.address=" + staticip + "\n")
        #f1.write("lxc.net.0.ipv4.dns=" + dns + "\n")
        if(dns == ""):
            f1.write("lxc.mount.entry = " + "/etc/resolv.conf" +" etc/resolv.conf" + " none bind,optional,create=file,ro\n")
        else:
            f1.write("lxc.mount.entry = " + "/etc/resolv.conf" +" etc/resolv.conf" + " none bind,optional,create=file,ro\n")
    else:
        pass;
        f1.write("lxc.net.0.type=empty\n")


    #f1.write("lxc.hook.pre-start=" + dirname + "/user_patched.bash\n")
    f1.write("lxc.mount.entry = " + dirname + "/user_patched.bash" +"  " +  dirname + "/user_patched.bash" + " none bind,optional,create=file,ro\n")

    for tmp in paths:
        if(tmp.find(":") == -1):
            if(os.path.isdir(tmp) == True):
                f1.write("lxc.mount.entry = " + tmp + " " + lxc_brechne_mount_path(tmp[1::]) + " none bind,optional,create=dir,rw\n");
            else:
                f1.write("lxc.mount.entry = " + tmp + "  " + lxc_brechne_mount_path(tmp[1::]) + " none bind,optional,create=file,rw\n");
        else:
            s1 = tmp.split(":");
            if(len(s1) == 2):
                if(os.path.isdir(s1[0]) == True):
                    f1.write("lxc.mount.entry = " + s1[0] +"  " +  lxc_brechne_mount_path(s1[1][1::]) + " none bind,optional,create=dir,rw\n");
                else:
                    f1.write("lxc.mount.entry = " + s1[0] +"  " +  lxc_brechne_mount_path(s1[1][1::]) + " none bind,optional,create=file,rw\n");
            elif(len(s1) == 3):
                if(s1[2] == "rw"):
                    if(os.path.isdir(s1[0]) == True):
                        f1.write("lxc.mount.entry = " + s1[0] +"  " +  lxc_brechne_mount_path(s1[1][1::]) + " none bind,optional,create=dir,rw\n");
                    else:
                        f1.write("lxc.mount.entry = " + s1[0] +"  " +  lxc_brechne_mount_path(s1[1][1::]) + " none bind,optional,create=file,rw\n");
                if(s1[2] == "ro"):
                    if(os.path.isdir(s1[0]) == True):
                        f1.write("lxc.mount.entry = " + s1[0] +"  " +  lxc_brechne_mount_path(s1[1][1::]) + " none bind,optional,create=dir,ro\n");
                    else:
                        f1.write("lxc.mount.entry = " + s1[0] +"  " +  lxc_brechne_mount_path(s1[1][1::]) + " none bind,optional,create=file,ro\n");
    #f1.write("lxc.cgroup.devices.allow: c 226:0 rwm\n");
    #f1.write("lxc.cgroup.devices.allow: c 226:1 rwm\n");
    #f1.write("lxc.cgroup.devices.allow: c 226:128 rwm\n");
    #f1.write("lxc.cgroup.devices.allow: c 226:129 rwm\n");

    #f1.write("lxc.autodev: 1\n");
    #f1.write("lxc.hook.autodev: /var/lib/lxc/mount_hook.sh\n");

    #f1.write("lxc.cgroup2.devices.allow = c 226:0 rwm\n");
    #f1.write("lxc.cgroup2.devices.alloww = c 226:1 rwm\n");
    #f1.write("lxc.cgroup2.devices.allow = c 226:128 rwm\n");
    #f1.write("lxc.cgroup2.devices.allow = c 226:129 rwm\n");

    #f1.write("lxc.mount.entry = /dev/video0 dev/video0 none bind,optional,create=file\n");
    f1.write("lxc.cgroup2.devices.allow = /tmp/.X11-unix/X1 rwm\n");
    f1.write("lxc.cgroup2.devices.allow = /etc/resolv.conf rwm\n");
    f1.write("lxc.mount.auto=cgroup-full\n")


    #muss zu lestz gemounten werden
    if(build_b1 == 1):
        #is builing
        f1.write("lxc.rootfs.path = dir:/var/lib/lxc/" +dockername+ "/rootfs\n");
    else:
        #not builing
        f1.write("lxc.rootfs.path = dir:/var/lib/lxc/" +dockername+ "/rootfs\n");

    if(lxc_readonly == 1):
        f1.write("lxc.rootfs.options = ro\n");
        pass;
    else:
        pass;
    #https://linuxcontainers.org/lxc/manpages//man5/lxc.container.conf.5.html


    for tmp in vars:
        #lxc.environment = XAUTHORITY=/root/.Xauthority
        f1.write("lxc.environment = " + tmp + "\n");
    if(ttyon == 1):
        #f1.write("lxc.tty = y\n");
        pass;
    else:
        #f1.write("lxc.tty = n\n");
        pass;

    f1.close();
    return 0;

def alnalsye_user_id(x11user):
    try:
        cmd = subprocess.check_output("su " + x11user +" -c id ", shell=True).decode().split();
        for tmp in cmd:
            if(tmp.find("uid=") != -1):
                s1 = tmp.split("=");
                s2 = s1[1].split("(");
                print(s2[0])
                return int(s2[0]);
        return -1;
    except subprocess.CalledProcessError:
        return -1;
    except FileNotFoundError:
        return -1;
    except IndexError:
        return -1;


def lxc_converter_docker_array_reading(args):
    paths = [];
    paths2 = [];
    variable = [];
    for i in range(len(args)):
        tmp = args[i];
        if(tmp == "-v"):
            paths.append(args[i+1]);
            i = i +1;
            continue;
        if(tmp == "-v2"):
            paths2.append(args[i+1]);
            i = i +1;
            continue;
        if(tmp == "--device"):
            paths.append(args[i+1]);
            i = i +1;
            continue;
        if(tmp == "-e"):
            variable.append(args[i+1]);
            i = i +1;
            continue;
    return [paths, variable, paths2];

def lxc_brechne_mount_path(s1):
    print(s1);
    s2 = s1.split("/");
    if(len(s2) >= 2):
        if(s2[0] == "run"):
            if(s2[1] == "media"):
                return "etc/sharefolder/" + s1;
    if(len(s2) >= 2):
        if(s2[0] == "run"):
            if(s2[1] == "user"):
                return "etc/" + s1;
    #if(s1.find("/tmp") != -1):
    #    return "/etc" + s1;
    return s1;

def lxc_find_a_new_snapshot_name(s1, docker_build):
    out = system("sudo lxc-snapshot -L -n " + docker_build);
    for tmp in out:
        if(tmp[0] == "No"):
            if(tmp[1] == "snapshots"):
                return "1";


def lxc_create_a_snapshot(docker_build):
    os.system("sudo lxc-snapshot -n " + docker_build + " -N " +docker_build + "_sav")
    return 0;

def lxc_create_a_snapshot_back(docker_build):
    os.system("sudo lxc-snapshot -d=" +docker_build + "_sav")
    os.system("sudo lxc-snapshot -n " + docker_build + " --restore=" +docker_build + "_sav");
    return 0;
