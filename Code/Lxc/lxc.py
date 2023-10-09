#!/usr/bin/env python
#Copyright (C) 2022  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#this is a fork from https://github.com/kritzsie/steam-on-docker

version = "0.2a lxc"

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



def lxc_question_use_bridge_network(text):
    from PyQt6 import QtWidgets
    from PyQt6 import QtGui
    from PyQt6 import QtCore
    import time
    import datetime
    app = QtWidgets.QApplication(sys.argv);
    class lxc_auswahl(QtWidgets.QWidget):
        def __init__(self):
            QtWidgets.QWidget.__init__(self)
            self.text = text;
        def start(self, test):
            text2, okPressed = QtWidgets.QInputDialog.getText(self, "Get text", self.text);
            if(okPressed and text2 != ""):
                return text2;
            else:
                exit(-1);
    mainwindow = lxc_auswahl()
    return mainwindow.start(text);

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

    #f1.write("lxc.init_cmd = /sbin/init systemd.legacy_systemd_cgroup_controller=yes\n");

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

def applay_path(paths, dockername, vars, ttyon, dirname, staticip, lxc_readonly, network_disable, lxc_network_mac, dns, build_b1, paths2
, network_host, lxc_string_add_config, docker_build, docker_username, docker_username_id, optcommands):
    if(os.path.isfile("/var/lib/lxc/" + dockername +"/config") == False):
        print("applay_path error fiel not found!");
        return 0;
    f1 = open("/var/lib/lxc/" + dockername +"/config", "w");
    dockername2 = "";
    if(len(optcommands) >= 1):
        dockername2 = optcommands[0]
    #f1.write("raw.lxc 'lxc.init_cmd = /sbin/init systemd.legacy_systemd_cgroup_controller=yes'\n")

    os.system("mkdir -p " + dirname + "/etc")
    #os.system("cp /var/lib/lxc/" + docker_build + "/rootfs/etc/group " + dirname + "/etc/group")
    #os.system("cp /var/lib/lxc/" + docker_build + "/rootfs/etc/group- " + dirname + "/etc/group-")
    #os.system("sudo cp /var/lib/lxc/" + docker_build + "/rootfs/etc/passwd " + dirname + "/etc/passwd")
    os.system("sudo chmod 777 " +  dirname + "/etc/passwd");
    #os.system("cp /var/lib/lxc/" + docker_build + "/rootfs/etc/shadow " + dirname + "/etc/shadow")
    #os.system("cp /var/lib/lxc/" + docker_build + "/rootfs/etc/gshadow " + dirname + "/etc/gshadow")
    #f1.write("lxc.mount.entry = " + dirname + "/etc/group" + " " + "etc/group" + " none bind,optional,create=file,rw\n");
    #f1.write("lxc.mount.entry = " + dirname + "/etc/group-" + " " + "etc/group-" + " none bind,optional,create=file,rw\n");
    f1.write("lxc.mount.entry = " + dirname + "/etc/passwd" + " " + "etc/passwd" + " none bind,optional,create=file,rw\n");
    #f1.write("lxc.mount.entry = " + dirname + "/etc/shadow" + " " + "etc/shadow" + " none bind,optional,create=file,rw\n");
    #f1.write("lxc.mount.entry = " + dirname + "/etc/gshadow" + " " + "etc/gshadow" + " none bind,optional,create=file,rw\n");

    f1.write("lxc.apparmor.profile = unconfined\n");

    if(build_b1 == 1):
        if(dockername2 != ""):
            f1.write("lxc.rootfs.path = dir:/var/lib/lxc/" +dockername2+ "\n");
        else:
            #is builing
            #f1.write("lxc.rootfs.path = dir:/var/lib/lxc/" +dockername+ "/rootfs\n");
            f1.write("lxc.rootfs.path = dir:/var/lib/lxc/" +dockername+ "/rootfs\n");
    elif(build_b1 == 2):
        f1.write("lxc.rootfs.path = dir:/var/lib/lxc/" +dockername+ "/rootfs/mnt/2\n");
    else:
        if(dockername2 != ""):
            f1.write("lxc.rootfs.path = dir:/var/lib/lxc/" +dockername2+ "\n")
        else:
            #not builing
            #f1.write("lxc.rootfs.path = dir:/var/lib/lxc/" +dockername+ "/rootfs\n");
            #f1.write("lxc.rootfs.path = dir:/var/lib/lxc/" +dockername+ "/rootfs\n");
            #f1.write("lxc.rootfs.path = dir:/var/lib/lxc/" +dockername+ "/rootfs\n");
            #f1.write("lxc.rootfs.path = dir:/var/lib/lxc/" +dockername+ "/rootfs/mnt/2\n");
            f1.write("lxc.rootfs.path = dir:/var/lib/lxc/" +dockername+ "/rootfs\n")
    if(lxc_readonly == 1):
        lxc_edit_passwd_empty_user_id(dirname, docker_username, docker_username_id)#docker_username_id
    f1.write("lxc.include = /usr/share/lxc/config/common.conf\n");
    f1.write("lxc.include = /usr/share/lxc/config/userns.conf\n");
    f1.write("lxc.mount.entry = tmpfs tmp tmpfs defaults\n​");

    f1.write("lxc.cgroup.devices.allow = c 11:* rwm\n")
    f1.write("lxc.cgroup.devices.allow = c 21:* rwm\n")
    f1.write("lxc.cgroup.devices.allow = c 243:* rwm\n")

    f1.write("lxc.arch = x86_64\n");

    #f1.write("lxc.rootfs.path = dir:/var/lib/lxc/" +dockername+ "/rootfs\n");

    f1.write("lxc.mount.entry = " + dirname + "/tmp " + "media" + " none bind,optional,create=dir,rw\n");
    for tmp in paths2:
        b1 = 0;
        if(tmp.find(":") == -1):
            if(os.path.isdir(tmp) == True):
                if(b1 == 0):
                    b1 = 1;
                    f1.write("lxc.mount.entry = " + tmp + " " + lxc_brechne_mount_path(tmp[1::], docker_build, 1) + " none bind,optional,create=dir,rw\n");
                    lxc_mount_path_create_dir_fix(lxc_brechne_mount_path(tmp[1::], docker_build, 1), docker_build);
            else:
                if(b1 == 0):
                    b1 = 1;
                    f1.write("lxc.mount.entry = " + tmp + "  " + lxc_brechne_mount_path(tmp[1::], docker_build, 0) + " none bind,optional,create=file,rw\n");
                    lxc_mount_path_create_file_fix(lxc_brechne_mount_path(tmp[1::], docker_build, 0), docker_build);
        else:
            s1 = tmp.split(":");
            if(len(s1) == 2):
                if(os.path.isdir(s1[0]) == True):
                    if(b1 == 0):
                        b1 = 1;
                        f1.write("lxc.mount.entry = " + s1[0] +"  " +  lxc_brechne_mount_path(s1[1][1::], docker_build, 1) + " none bind,optional,create=dir,rw\n");
                        lxc_mount_path_create_dir_fix(lxc_brechne_mount_path(s1[1][1::], docker_build, 1), docker_build);
                else:
                    if(b1 == 0):
                        b1 = 1;
                        f1.write("lxc.mount.entry = " + s1[0] +"  " +  lxc_brechne_mount_path(s1[1][1::], docker_build, 0) + " none bind,optional,create=file,rw\n");
                        lxc_mount_path_create_file_fix(lxc_brechne_mount_path(s1[1][1::], docker_build, 0), docker_build);
            elif(len(s1) == 3):
                if(s1[2] == "rw"):
                    if(os.path.isdir(s1[0]) == True):
                        if(b1 == 0):
                            b1 = 1;
                            f1.write("lxc.mount.entry = " + s1[0] +"  " +  lxc_brechne_mount_path(s1[1][1::], docker_build, 1) + " none bind,optional,create=dir,rw\n");
                            lxc_mount_path_create_dir_fix(lxc_brechne_mount_path(s1[1][1::], docker_build, 1), docker_build);
                    else:
                        if(b1 == 0):
                            b1 = 1;
                            f1.write("lxc.mount.entry = " + s1[0] +"  " +  lxc_brechne_mount_path(s1[1][1::], docker_build, 0) + " none bind,optional,create=file,rw\n");
                            lxc_mount_path_create_file_fix(lxc_brechne_mount_path(s1[1][1::], docker_build, 0), docker_build);
                if(s1[2] >= "ro"):
                    if(os.path.isdir(s1[0]) == True):
                        if(b1 == 0):
                            b1 = 1;
                            f1.write("lxc.mount.entry = " + s1[0] +"  " +  lxc_brechne_mount_path(s1[1][1::], docker_build, 1) + " none bind,optional,create=dir,ro\n");
                            lxc_mount_path_create_dir_fix(lxc_brechne_mount_path(s1[1][1::], docker_build, 1), docker_build);
                    else:
                        if(b1 == 0):
                            b1 = 1;
                            f1.write("lxc.mount.entry = " + s1[0] +"  " +  lxc_brechne_mount_path(s1[1][1::], docker_build, 0) + " none bind,optional,create=file,ro\n");
                            lxc_mount_path_create_file_fix(lxc_brechne_mount_path(s1[1][1::], docker_build, 0), docker_build);
            elif(len(s1) >= 3):
                if(b1 == 0):
                    b1 = 1;
                    f1.write("lxc.mount.entry = " + tmp + " " + lxc_brechne_mount_path(tmp[1::], docker_build, 0) + " none bind,optional,create=file,rw\n");
                    lxc_mount_path_create_file_fix(lxc_brechne_mount_path(tmp[1::], docker_build, 0), docker_build);

    #f1.write("lxc.rootfs.backend = dir\n");
    #f1.write("lxc.mount.entry = "  +  "/var/lib/lxc/" +dockername+ "/rootfs " + " none bind,optional,create=dir,ro\n")

    #f1.write("lxc.mount.entry = " + "/var/lib/lxc/" +dockername+ "/rootfs" + "  none bind,optional,create=dir,rw\n");
    #f1.write("lxc.mount.entry = " + "/proc /proc none bind,optional,create=dir,ro\n");

    #f1.write("lxc.rootfs.options = rw\n");
    f1.write("lxc.uts.name = " +dockername+ "\n");
    if(network_disable == 0):
        if(network_host != ""):
            f1.write("lxc.net.0.type = veth\n");
            f1.write("lxc.net.0.link = " + network_host + "\n");
            #f1.write("lxc.net.0.flags = up\n");
            if(lxc_network_mac == ""):
                pass;
            elif(lxc_network_mac == "0"):
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
    else:
        pass;
        f1.write("lxc.net.0.type=empty\n")


    #f1.write("lxc.hook.pre-start=" + dirname + "/user_patched.bash\n")
    f1.write("lxc.mount.entry = " + dirname + "/user_patched.bash" +"  " +  dirname + "/user_patched.bash" + " none bind,optional,create=file,ro\n")

    for tmp in paths:
        b1 = 0;
        if(tmp.find(":") == -1):
            if(os.path.isdir(tmp) == True):
                if(b1 == 0):
                    b1 = 1;
                    f1.write("lxc.mount.entry = " + tmp + " " + lxc_brechne_mount_path(tmp[1::], docker_build, 1) + " none bind,optional,create=dir,rw\n");
                    lxc_mount_path_create_dir_fix(lxc_brechne_mount_path(tmp[1::], docker_build, 1), docker_build);
            else:
                if(b1 == 0):
                    b1 = 1;
                    f1.write("lxc.mount.entry = " + tmp + "  " + lxc_brechne_mount_path(tmp[1::], docker_build, 0) + " none bind,optional,create=file,rw\n");
                    lxc_mount_path_create_file_fix(lxc_brechne_mount_path(tmp[1::], docker_build, 0), docker_build);
        else:
            s1 = tmp.split(":");
            if(len(s1) == 2):
                if(os.path.isdir(s1[0]) == True):
                    if(b1 == 0):
                        b1 = 1;
                        f1.write("lxc.mount.entry = " + s1[0] +"  " +  lxc_brechne_mount_path(s1[1][1::], docker_build, 1) + " none bind,optional,create=dir,rw\n");
                        lxc_mount_path_create_dir_fix(lxc_brechne_mount_path(s1[1][1::], docker_build, 1), docker_build);
                else:
                    if(b1 == 0):
                        b1 = 1;
                        f1.write("lxc.mount.entry = " + s1[0] +"  " +  lxc_brechne_mount_path(s1[1][1::], docker_build, 0) + " none bind,optional,create=file,rw\n");
                        lxc_mount_path_create_file_fix(lxc_brechne_mount_path(s1[1][1::], docker_build, 0), docker_build);
            elif(len(s1) == 3):
                if(s1[2] == "rw"):
                    if(os.path.isdir(s1[0]) == True):
                        if(b1 == 0):
                            b1 = 1;
                            f1.write("lxc.mount.entry = " + s1[0] +"  " +  lxc_brechne_mount_path(s1[1][1::], docker_build, 1) + " none bind,optional,create=dir,rw\n");
                            lxc_mount_path_create_dir_fix(lxc_brechne_mount_path(s1[1][1::], docker_build, 1), docker_build);
                    else:
                        if(b1 == 0):
                            b1 = 1;
                            f1.write("lxc.mount.entry = " + s1[0] +"  " +  lxc_brechne_mount_path(s1[1][1::], docker_build, 0) + " none bind,optional,create=file,rw\n");
                            lxc_mount_path_create_file_fix(lxc_brechne_mount_path(s1[1][1::], docker_build, 0), docker_build);
                if(s1[2] >= "ro"):
                    if(os.path.isdir(s1[0]) == True):
                        if(b1 == 0):
                            b1 = 1;
                            f1.write("lxc.mount.entry = " + s1[0] +"  " +  lxc_brechne_mount_path(s1[1][1::], docker_build, 1) + " none bind,optional,create=dir,ro\n");
                            lxc_mount_path_create_dir_fix(lxc_brechne_mount_path(s1[1][1::], docker_build, 1), docker_build);
                    else:
                        if(b1 == 0):
                            b1 = 1;
                            f1.write("lxc.mount.entry = " + s1[0] +"  " +  lxc_brechne_mount_path(s1[1][1::], docker_build, 0) + " none bind,optional,create=file,ro\n");
                            lxc_mount_path_create_file_fix(lxc_brechne_mount_path(s1[1][1::], docker_build, 0), docker_build);
            elif(len(s1) >= 3):
                if(b1 == 0):
                    b1 = 1;
                    f1.write("lxc.mount.entry = " + tmp + " " + lxc_brechne_mount_path(tmp[1::], docker_build, 0) + " none bind,optional,create=file,rw\n");
                    lxc_mount_path_create_file_fix(lxc_brechne_mount_path(tmp[1::], docker_build, 0), docker_build);


    for tmp in paths:
        if(tmp.find(":") == -1):
            if(os.path.isdir(tmp) == True):
                lxc_mount_path_create_dir_fix(lxc_brechne_mount_path(tmp[1::], docker_build, 0), docker_build);
        else:
            s1 = tmp.split(";");
            if(os.path.isdir(s1[0]) == True):
                lxc_mount_path_create_dir_fix(lxc_brechne_mount_path(s1[1][1::], docker_build, 0), docker_build);
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
    f1.write("lxc.cgroup2.devices.allow = c 21:0 rwm\n")

    #https://linuxcontainers.org/lxc/getting-started/#creating-unprivileged-containers-as-a-user
    #MS_UID = system("grep \"$(id -un)\" /etc/subuid  | cut -d : -f 2");
    #ME_UID = system("grep \"$(id -un)\" /etc/subuid  | cut -d : -f 3");

    #MS_GID = system("grep \"$(id -un)\" /etc/subgid  | cut -d : -f 2");
    #ME_GID = system("grep \"$(id -un)\" /etc/subgid  | cut -d : -f 3");
    #f1.write("lxc.idmap = u 0 100000 65536\n");
    #f1.write("lxc.idmap = g 0 100000 65536\n");


    #f1.write("lxc.cgroup2.devices.allow = c\n")
    f1.write("lxc.mount.auto=cgroup-full:rw\n")
    f1.write(lxc_string_add_config);
    f1.write("lxc.mount.entry = /dev/disk dev/disk none bind,optional,create=dir,ro\n");


    #muss zu lestz gemounten werden

    if(False):
        f1.write("lxc.rootfs.path = dir:/\n");
        lxc_readonly = 1;
        s1 = "/var/lib/lxc/" + dockername + "/rootfs";
        s2 = s1 + "/usr";
        f1.write("lxc.mount.entry = " + s2 + " " + s2[1::] + " none bind,optional,create=file,ro\n");
        s2 = dirname + "/root";
        if(os.path.isdir(s2) == False):
            os.system("mkdir -p " + s2);
        f1.write("lxc.mount.entry = " + s2 + " " + s2[1::] + " none bind,optional,create=file,rw\n");
        #
        s2 = s1 + "/etc";
        f1.write("lxc.mount.entry = " + s2 + " " + s2[1::] + " none bind,optional,create=file,rw\n");
        #
        s2 = s1 + "/mnt";
        f1.write("lxc.mount.entry = " + s2 + " " + s2[1::] + " none bind,optional,create=file,rw\n");
        #
        s2 = dirname + "/tmp";
        if(os.path.isdir(s2) == False):
            os.system("mkdir -p " + s2);
        f1.write("lxc.mount.entry = " + s2 + " " + s2[1::] + " none bind,optional,create=file,rw\n");
        #
        s2 = dirname + "/home";
        if(os.path.isdir(s2) == False):
            os.system("mkdir -p " + s2);
        f1.write("lxc.mount.entry = " + s2 + " " + s2[1::] + " none bind,optional,create=file,rw\n");
        #

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
    f1.write("lxc.autodev=1\nlxc.autodev.tmpfs.size=500000000\n");
    f1.write("")

    #f1.write("lxc.mount.entry = " + "/dev/null" + " dev/null "  + " none bind,optional,create=file,rw\n");
    #f1.write("lxc.mount.entry = " + "/dev/block" + " dev/block "  + " none bind,optional,create=file,ro\n");
    if(build_b1 == 0):
        if(lxc_readonly == 1):
            f1.write("lxc.rootfs.options = ro\n");
            pass;
    else:
        pass;

    f1.write("lxc.start.auto=1\n")
    f1.close();
    os.system("sudo sysctl kernel.unprivileged_userns_clone=1");

    #os.system("echo \"lxc.idmap = u 0 " + MS_UID[0] +  " " +  ME_UID[0] + "\" >> /var/lib/lxc/" + dockername +"/config");
    #os.system("echo \"lxc.idmap = g 0 " + MS_GID[0] + " " + ME_GID[0] + " >> /var/lib/lxc/" + dockername +"/config");
    #exit();
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
    devices = [];
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
            devices.append(args[i+1]);
            #paths.append(args[i+1]);
            i = i +1;
            continue;
        if(tmp == "-e"):
            variable.append(args[i+1]);
            i = i +1;
            continue;
    return [paths, variable, paths2, devices];

def lxc_brechne_mount_path(s1, docker_build, isdir):
    print(s1);
    s2 = s1.split("/");
    sout = ""
    if(len(s2) >= 2):
        if(s2[0] == "run"):
            if(s2[1] == "media"):
                sout= lxc_path_remove_run(s1);
    if(len(s2) >= 2):
        if(s2[0] == "run"):
            if(s2[1] == "user"):
                sout = "etc/" + s1;
    if(len(s2) >= 2):
        if(s2[0] == "tmp"):
                sout = "etc/" + s1;
    if(sout == ""):
        sout = s1;
    #if(s1.find("/tmp") != -1):
    #    return "/etc" + s1;
    if(isdir == 1):
        lxc_mount_path_create_dir_fix(sout, docker_build)
    return sout;

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

def lxc_exist_newtworkdevice(device):
    b1 = 1;
    out = system("ip a");
    for tmp2 in out:
        tmp = tmp2.split();
        if(len(tmp) >= 3 and tmp[0] == str(b1) + ":"):
            b1 = b1 + 1;
            if(b1 >= 2):
                if(tmp[1] == device + ":"):
                    return 1;
    return 0;


def lxc_find_eth0_network_Device():
    while True:
        try:
            b1 = 1;
            out = system("ip a");
            out2 = [];
            out2_up = [];
            for tmp2 in out:
                tmp = tmp2.split();
                if(len(tmp) >= 3 and tmp[0] == str(b1) + ":"):
                    b1 = b1 + 1;
                    if(b1 >= 2):
                        out2.append(tmp[1].split(":")[0]);
                        out2_up.append(tmp[2].split(":")[0]);
            if(len(out2) == 0):
                return -1;
            out3 = [];
            out3_up = [];
            for i in range(len(out2)):
                tmp = out2[i];
                tmp2 = out2_up[i];
                if(tmp.find("br") != -1):
                    continue;
                if(tmp.find("docker") != -1):
                    continue;
                if(tmp.find("lxc") != -1):
                    continue;
                if(tmp.find("lo") != -1):
                    continue;
                if(tmp.find("anbox") != -1):
                    continue;
                if(tmp.find("eth") != -1):
                    out3.append(tmp);
                    out3_up.append(tmp2);
                if(tmp.find("en") != -1):
                    out3.append(tmp);
                    out3_up.append(tmp2);
                if(tmp.find("wl") != -1):
                    out3.append(tmp);
                    out3_up.append(tmp2);
            if(len(out3) == 1):
                return out3[0];
            text = "your network bridge link internet:"
            text = text + "choice:\n";
            for i in range(len(out3)):
                tmp = out3[i];
                text = text + "[" + str(i) + "]" + tmp + "\n"
            text = text + "your eth0 network:"
            br = lxc_question_use_bridge_network(text);
            br1 = int(br);
            if(br1 >= 0):
                if(br1 < len(out3)):
                    return out3[br1];
            print("EROOR auswahl not found!")
            return "";
        except ValueError:
            print("EROOR auswahl no int found!")


def lxc_wait_file_look(docker_build):
    i = 0;
    while True:
        if(os.path.isfile("/var/lib/lxc/look.file.tmp") == False):
            os.system("sudo echo \"1\" >/var/lib/lxc/ "+ docker_build + "/look.file.tmp");
            return 0;
        time.sleep(5);
        i = i + 1;
        if(i == 20):
            break;
    return 0;


def lxc_create_a_new_vm_copy(docker_build, id):
    os.system("sudo mkdir -p /var/lib/lxc/" + docker_build + "_backing" +str(id) + "/rootfs");
    os.system("sudo chown -R  100000:100000  /var/lib/lxc/" + docker_build + "_backing" +str(id) + "")
    os.system("sudo chmod -R 777   /var/lib/lxc/" + docker_build + "_backing" +str(id) + "")
    os.system("sudo mount -B /var/lib/lxc/" + docker_build + "/rootfs/mnt/2  /var/lib/lxc/" + docker_build + "_backing" +str(id) + "/rootfs -o ro");
    os.system("echo 1 > /var/lib/lxc/" + docker_build + "_backing" +str(id) + "/config")
    return 0;

def lxc_remove_look_file(docker_build):
    os.system("sudo rm /var/lib/lxc/ "+ docker_build + "/look.file.tmp");
    return  0;

def lxc_remove_a_new_vm_copy(docker_build, id):
    os.system("sudo umount /var/lib/lxc/" + docker_build + "_backing" +str(id) +"/rootfs");
    os.system("sudo rm -r /var/lib/lxc/" + docker_build + "_backing" +str(id));
    return 0;

def lxc_create_a_new_vm_copy_auto(docker_build):
    i = 1;
    while True:
        if(os.path.isdir("/var/lib/lxc/" + docker_build + "_backing" +str(i)) == False):
            lxc_create_a_new_vm_copy(docker_build, i);
            return i;
        i = i +1;
    return -1;

def lxc_find_eth0_network_bridge():
    while True:
        b1 = 1;
        out2 = [];
        out = system("brctl  show")[1::];
        for tmp in out:
            tmp2 = tmp.split();
            if(len(tmp2) >= 3):
                out2.append(tmp2[0])
        if(len(out2) == 1):
            return out2;
        else:
            if(len(out2) == 0):
                return "";
        text = "choice:\n";
        for tmp in out2:
            text = text + tmp + "\n"
        text = text + "your bridge network:"
        br = lxc_question_use_bridge_network(text);
        for tmp in out2:
            if(tmp == br):
                return tmp;
        print("EROOR auswahl not found!")


def lxc_remove_all_vms(docker_build):
    i = 1;
    while True:
        if(os.path.isdir("/var/lib/lxc/" + docker_build + "_backing" +str(i)) == True):
            os.system("sudo lxc-stop -n " + docker_build + "_backing" +str(i) + " -k");
            lxc_remove_a_new_vm_copy(docker_build, i);
        i = i +1;
        if( i == 10000):
            break;
    return -1;


def lxc_path_remove_run(s1):
    s2 = s1.split("/");
    out = "";
    for tmp in s2:
        if(tmp == "run"):
            continue;
        if(tmp == "tmp"):
            continue;
        if(tmp == ""):
            continue;
        out = out + tmp + "/";
    return out;

def lxc_covert_device_array_to_string(array, docker_build):
    out =  "";
    out_vm = "";
    out_lxc_string = "";
    for tmp in array:
        if(tmp.find(":") == -1):
            out = out + "sudo lxc-device -n " + docker_build + " add " + tmp + "\n";
            out_vm = out_vm + "chmod 777 " + tmp + "\n";
            out = out + "sudo mknod -m 666 /var/lib/lxc/docker_build" + tmp + " c 21 3\n";
            out_lxc_string = out_lxc_string + lxc_device_path_convert_to_device_id(tmp) + "\n";
        else:
            tmp2 = tmp.split(":");
            if(len(tmp2) >= 2):
                out = out + "sudo lxc-device -n " + docker_build + " add " + tmp2[0] + "\n";
                out = out + "sudo mknod -m 666 /var/lib/lxc/docker_build" + tmp2[0] + " c 21 3\n";
                out_vm = out_vm + "chmod 777 " + tmp2[0] + "\n";
                out_lxc_string = out_lxc_string + lxc_device_path_convert_to_device_id(tmp2[0]) + "\n";
    return [out, out_vm, out_lxc_string];

def lxc_device_path_convert_to_device_id(s1):
    out = system("ls -la " + s1);
    out2 = [];
    out2_2 = [];
    for tmp in out:
        tmp2 = tmp.split();
        for i in range(len(tmp2)):
            tmp3 = tmp2[i];
            if(tmp3.find(",") != -1):
                out2.append(tmp3.split(",")[0]);
                out2_2.append(tmp2[i+ 1]);
                break;
    out3 = "";
    for i in range(len(out2)):
        tmp = out2[i];
        tmp2 = out2_2[i];
        out3 = out3 + "lxc.cgroup.devices.allow: c " + s1 + "  rwm\n";
        #out3 = out3 + "lxc.cgroup.devices.allow: a " + tmp + ":" + tmp2 + "  rwm\n";
        #out3 = out3 + "lxc.cgroup.devices.allow: c " + tmp + ":" + tmp2 + "  rwm\n";
    return out3;

def lxc_dri_prime_to_dvice_paths(driprime, baseargs):
    baseargs.append("-v");
    baseargs.append("/dev/dri/card" + str(driprime) + ":/dev/dri/card0:rw")
    baseargs.append("-v");
    baseargs.append("/dev/dri/renderD" + str(int(driprime) + 128) + ":/dev/dri/renderD" + str(128)+":rw")
    return baseargs;

def lxc_edit_passwd_empty_user_id(dirname , username, id):
    f1 = open(dirname + "/etc/passwd", "r");
    f1.seek(0, 2);
    size = f1.tell();
    f1.seek(0, 0);
    b1 = f1.read(size);
    f1.close();
    b2 = b1.split("\n");
    out = "";
    for tmp in b2:
        tmp2 = tmp.split(":");
        if(tmp2[0] ==  username):
            out = out + "empty:x:"+ str(id) + ":984::/home/empty:/bin/bash\n"
        else:
            out = out + tmp + "\n";
    f1 = open(dirname + "/etc/passwd", "w");
    f1.write(out);
    f1.close();
    return 0;

def lxc_create_a_new_random_mac_addr():
    #beta 0.1a
    out = system("openssl rand -hex 6 ")[0][::-1]
    out2 = "";
    b1 = 1;
    for tmp in out:
        if(b1 == 1):
            b1 = 0;
            out2 = out2 + tmp;
        else:
            b1 = 1;
            out2 = out2 + tmp + ":";
    return out2[:-1];


def lxc_mount_path_create_file_fix(path, docker_build):
    s1 = path.split("/");
    s2 = "";
    i = 0;
    while True:
        tmp = s1[i]
        if(i + 1 >= len(s1)):
            #s2 = s2 + tmp;
            break;
        s2 = s2 + tmp + "/";
        i = i +1
    return lxc_mount_path_create_dir_fix_Create_dir(s2[::1], docker_build);

def lxc_mount_path_create_dir_fix(path, docker_build):
    return lxc_mount_path_create_dir_fix_Create_dir(path, docker_build);
    s1 = path.split("/");
    s2 = "";
    for i in range(len(s1)):
        tmp = s1[i]
        if(i + 1 >= len(s1)):
            s2 = s2 + tmp;
            break;
        s2 = s2 + tmp + "/";
    return lxc_mount_path_create_dir_fix_Create_dir(s2, docker_build);

def lxc_mount_path_create_dir_fix_Create_dir(path, docker_build):
    b1 = 0;
    if(len(path) >= 2 and path[0] == "/"):
        b1 = 1;
    scmd = "";
    if(b1 == 0):
        scmd = "/var/lib/lxc/" + docker_build + "/rootfs/" + path;
    else:
        scmd = "/var/lib/lxc/" + docker_build + "/rootfs" + path;
    os.system("sudo mkdir -p " + scmd);
    if(os.path.isdir("/var/lib/lxc/" + docker_build + "/rootfs/mnt/2/usr") == True):
        if(b1 == 0):
            scmd = "/var/lib/lxc/" + docker_build + "/rootfs/mnt/2/" + path;
        else:
            scmd = "/var/lib/lxc/" + docker_build + "/rootfs/mnt/2" + path;
        os.system("sudo mkdir -p " + scmd);
    print(scmd);
    return 0;

def lxc_edit_passwd_empty_user_id(dirname , username, id):
    if(os.path.isfile(dirname + "/etc/passwd") == False):
        return 1;
    f1 = open(dirname + "/etc/passwd", "r");
    f1.seek(0, 2);
    size = f1.tell();
    f1.seek(0, 0);
    b1 = f1.read(size);
    f1.close();
    b2 = b1.split("\n");
    out = "";
    b1 = 0;
    for tmp in b2:
        tmp2 = tmp.split(":");
        if(tmp2[0] ==  username):
            out = out + "empty:x:"+ str(id) + ":984::/home/empty:/bin/bash\n"
            b1 = 1;
        elif(tmp != ""):
            out = out + tmp + "\n";
    if(b1 == 0):
        print("error docker user not found!")
        return -1;
        #out = out + "empty:x:"+ str(id) + ":984::/home/empty:/bin/bash\n"
    #out = out + "\n";
    os.system("sudo rm " + dirname + "/etc/passwd");
    f1 = open(dirname + "/etc/passwd", "w");
    f1.write(out);
    f1.close();
    return 0;

def lxc_edit_shadow_empty_user_id(dirname , username, id):
    if(os.path.isfile(dirname + "/etc/shadow") == False):
        return 1;
    f1 = open(dirname + "/etc/shadow", "r");
    f1.seek(0, 2);
    size = f1.tell();
    f1.seek(0, 0);
    b1 = f1.read(size);
    f1.close();
    b2 = b1.split("\n");
    out = "";
    b1 = 0;
    for tmp in b2:
        tmp2 = tmp.split(":");
        if(tmp2[0] == username):
            out = out + username + ':'+ "1234" + ':19161:0:99999:7:::\n'
            b1 = 1;
        elif(tmp != ""):
            out = out + tmp + "\n";
    if(b1 == 0):
        #out = out + "empty:!*:" + str(id) + "::::::\n";
        #out = out + username + ":*:19161:0:99999:7:::\n"
        out = out + username + ':'+ "1234" + ':19161:0:99999:7:::\n'
        #out = out + "empty:x:"+ str(id) + ":984::/home/empty:/bin/bash\n"
    #out = out + "\n";
    os.system("sudo rm " + dirname + "/etc/shadow");
    f1 = open(dirname + "/etc/shadow", "w");
    f1.write(out);
    f1.close();
    return 0;


def pci_ide_to_drmcard_id(pciid):
    pci = pciid.split(":")
    amdeviceid = subprocess.check_output("cat < /sys/class/drm/card0/device/driver/0000\:" + pci[0] + "\:" +pci[1] + "/device", shell=True).decode().split();
    #print(amdeviceid);
    return amdeviceid;

def pci_ids_to_device_name( pciid):
        amdeviceid = subprocess.check_output("lspci -k  -s " + pciid, shell=True).decode();
        s1 = amdeviceid.split("VGA compatible controller: ");
        s2 = s1[1].split("\n");
        s3 = s2[0].split("\t")
        #print(s3);
        return s3[0];

def check_device_id_dound( deviceid):
        i = 0;
        while True:
            if(i > 16):
                break;
            try:
                amdeviceid = subprocess.check_output("cat < /sys/class/drm/card" + str(i) + "/device/device", shell=True).decode().split();
                #print(amdeviceid);
                #print(deviceid)
                if(amdeviceid == deviceid):
                    return i;
            except subprocess.CalledProcessError:
                break;
            i = i +1;
        return -1;

def amd_gup_pci_ids():
        amd_pci_ids = subprocess.check_output("lspci | grep -E \"^.*(VGA|Display).*\[AMD\/ATI\].*$\" | grep -Eo \"^([0-9a-fA-F]+:[0-9a-fA-F]+.[0-9a-fA-F])\"", shell=True).decode().split()
        #amd_pci_ids = subprocess.check_output("lspci | grep -E \"^.*(VGA|Display).*\[AMD\/ATI\].*$\" ", shell=True).decode().split()
        #info = [];
        deviceid = []
        devicename = [];
        cardid = [];
        for pci_id in amd_pci_ids:
            did = pci_ide_to_drmcard_id(pci_id);
            deviceid.append(did);
            devicename.append(pci_ids_to_device_name(pci_id));
        #print(deviceid);
        for id in deviceid:
            i = check_device_id_dound(id);
            if(i != -1):
                cardid.append(i);
            else:
                print("ERROR deviceid not found!");
                exit(-1);
        print(cardid);
        return [amd_pci_ids, deviceid, devicename, cardid];

def remove_space(s1):
    out = "";
    for tmp in s1:
        if(tmp != " "):
            out = out + tmp;
    return out;


def suche_vulkandevice(vkdevicename, out):
    pciids = out[0];
    deviceids = out[1]
    names = out[2];
    cards = out[3];
    #print(out)
    for i in range(len(names)):
        tmp = names[i]
        s1 = tmp.split("[")[2].split("]")[0].lower();
        print(s1)
        if(s1.find(vkdevicename) != -1):
            return deviceids[i];
    return 0;
    os.system("MESA_VK_DEVICE_SELECT='list' vkcube 2>pipe.tmp");
    f1 = open("pipe.tmp", "r");
    f1.seek(0, 2);
    size = f1.tell();
    f1.seek(0, 0);
    s1 = f1.read(size);
    f1.close();
    #print(s1);
    s2 = s1.split("\n");
    #print(s2)
    b1 = 0;
    for tmp in s2:
        s3 = tmp.split();
        if(b1 == 0):
            if(len(s3) >= 2):
                if(s3[0] == "selectable"):
                    if(s3[1] == "devices:"):
                        b1 = 1;
                        print("b1 = 1")
        elif(b1 == 1):
            if(len(s3) >= 6):
                device_name = s3[5].split("\"")[0];
                device_id = s3[2];
                if(device_name == vkdevicename):
                    return device_id;
                if(device_name.upper() == vkdevicename):
                    return device_id;
                if(device_name.lower() == vkdevicename):
                    return device_id;
    return 0;


def lxc_podman_find_gpu_amd_Card_Nummber(amdgpuname):
    out = amd_gup_pci_ids();
    print(out)
    print(amdgpuname)
    for i in range(len(out[2])):
        if(out[2][i].lower().find(amdgpuname.lower()) != -1):
            #return out[3][i];
            return i;
    for tmp2 in out[2]:
        tmp3 = tmp2.lower();
        print(tmp3)
        b1 = 0;
        for tmp in amdgpuname.lower().split(" "):
            print(tmp)
            if(tmp3.find(tmp) != -1):
                b1 = b1 + 1;
        print("b1:", b1)
        if(b1 >= 2):
            return i;
    return -1;


def lxc_find_gpu_amd_Card_Nummber(amdgpuname):
    return lxc_podman_find_gpu_amd_Card_Nummber(amdgpuname);
    out = amd_gup_pci_ids();
    deviceid = suche_vulkandevice(amdgpuname, out);
    print(deviceid)
    if(deviceid == 0):
        return 0;
    for i in range(len(out[1])):
        if(deviceid == out[1][i]):
            return out[3][i];
    return -1;

def lxc_mount_path_create_dir_fix(path, docker_build):
    s1 = path.split("/");
    s2 = "";
    for i in range(len(s1)):
        tmp = s1[i]
        if(i + 1 >= len(s1)):
            s2 = s2 + tmp;
            break;
        s2 = s2 + tmp + "/";
    return lxc_mount_path_create_dir_fix_Create_dir(s2, docker_build);

def lxc_mount_path_create_dir_fix_Create_dir(path, docker_build):
    scmd = "/var/lib/lxc/" + docker_build + "/rootfs" + path;
    os.system("sudo mkdir -p " + scmd);
    print(scmd);
    return 0;

def lxc_edit_passwd_empty_user_id(dirname , username, id):
    if(os.path.isfile("passwd+") == False):
        return 1;
    f1 = open(dirname + "passwd+", "r");
    f1.seek(0, 2);
    size = f1.tell();
    f1.seek(0, 0);
    b1 = f1.read(size);
    f1.close();
    b2 = b1.split("\n");
    out = "";
    b1 = 0;
    for tmp in b2:
        tmp2 = tmp.split(":");
        if(tmp2[0] ==  username):
            out = out + "empty:x:"+ str(id) + ":984::/home/empty:/bin/bash\n"
            b1 = 1;
        elif(tmp != ""):
            out = out + tmp + "\n";
    if(b1 == 0):
        print("error docker user not found!")
        return -1;
        #out = out + "empty:x:"+ str(id) + ":984::/home/empty:/bin/bash\n"
    out = out + "\n";
    os.system("sudo rm " + "passwd");
    f1 = open("passwd", "w");
    f1.write(out);
    f1.close();
    return 0;


def lxc_brechne_groups_docker_user(docker_user, array):
    out = "";
    for tmp in array:
        out = out + "usermod -aG " + tmp + " empty\n";
    return out;

def lxc_add_groups_docker_user(basename, docker_build, docker_user):
    if(basename == "system_only" or basename == "system_only2" or basename == "build"):
        return 0;
    os.system("./system_only2 'cp /etc/group /etc/tmp/pipe.tmp'")
    f1 = open("pipe.tmp", "r");
    f1.seek(0, 2);
    size = f1.tell();
    f1.seek(0, 0);
    s1 = f1.read(size);
    f1.close();
    s2 = s1.split("\n");
    out = [];
    for tmp in s2:
        if(tmp == ""):
            continue;
        s3 = tmp.split(":")[0];
        out.append(s3);
    return lxc_brechne_groups_docker_user(docker_user, out)


def list_all_lspci_vga_device():
    out = system("lspci -v | grep \"VGA compatible controller: \"")
    ids = [];
    name = [];
    for tmp in out:
        tmp2 = tmp.split();
        if(len(tmp2) >= 2):
            ids.append(tmp2[0])
            print(tmp2)
            name.append(tmp.split("VGA compatible controller: ")[1])
    print(ids)
    print(name)
    return [ids, name]

def pciid_to_deviceid(pciid):
    out = system("lspci -n")
    for tmp in out:
        if(tmp.find(pciid) != -1):
            tmp2 = tmp.split();
            print(tmp2);
            return tmp2[2];
    return -1;


def find_vulkan_device_id_for_gamescope(amdgpuname):
    tmp1 = list_all_lspci_vga_device();
    pciid = tmp1[0];
    pciname = tmp1[1];
    j = -1;
    for i in range(len(pciname)):
        tmp1 = pciid[i];
        tmp2 = pciname[i];
        tmp3 = tmp2.lower();
        print(tmp3)
        b1 = 0;
        for tmp in amdgpuname.lower().split():
            print(tmp)
            if(tmp3.find(tmp) != -1):
                b1 = b1 + 1;
        if(b1 >= 2):
            device_id = pciid_to_deviceid(pciid[i])
            return device_id;
    return -1;
