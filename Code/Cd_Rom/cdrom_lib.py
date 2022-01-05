#!/usr/bin/env python
#Copyright (C) 2021  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#this is a fork from https://github.com/kritzsie/steam-on-docker

version = "0.2c"

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


def create_a_cdrom_mount_file_per_dev(devarray, docker_user, folder):
    if(os.path.isdir(os.path.join(folder, "home")) == False):
        return 0;
    print(os.path.join(folder, "home"));
    array = find_wine_prefix(os.path.join(folder, "home"));
    print("find_wine_prefix return: ", array)
    wine_dir = array[0];
    proton_dir = array[1];
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
        for tmp in wine_dir:
            patch_wine_fodler_cdrom(tmp ,"/mnt/cdrom"+ str(i+1), buchstabe[buchstabe_i], tmp2, tmp);
        for tmp in proton_dir:
            patch_wine_fodler_cdrom(tmp ,"/mnt/cdrom"+ str(i+1), buchstabe[buchstabe_i], tmp2, os.path.join(tmp, "pfx"));
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


def patch_wine_fodler_cdrom(device, mountpoint, buchstabe, sg, folder = ""):
    if(folder == ""):
        folder = "home/.wine";
    #patch wine folder in home user folder home/.wine use cdrom DRM in wine folder
    abspath = os.path.abspath(sys.argv[0]);
    basename = os.path.basename(abspath);
    dirname = os.path.dirname(abspath);
    if(os.path.isdir(folder + "/dosdevices/") == False):
        return 0;

    print("sg", sg);
    print("buchstabe", buchstabe)
    print("mountpoint", mountpoint)
    #print(device);
    #print(mountpoint);
    #print("ln -sf "+ device + " home/.wine/dosdevices/" + buchstabe + "::");
    system("rm " + folder + "/dosdevices/" + buchstabe + "::")
    system("rm " + folder + "/dosdevices/" + buchstabe + ":")
    print("ln -sf "+ sg + " " + folder + "/dosdevices/" + buchstabe + "::")
    system("ln -sf "+ sg + " " + folder + "/dosdevices/" + buchstabe + "::");
    print("ln -sf "+ mountpoint + " " + folder +"/dosdevices/" + buchstabe +":");
    system("ln -sf "+ mountpoint + " " + folder +"/dosdevices/" + buchstabe +":");
    print("wine fodler gepatch");
    return 0;


def listpath_only_dirs(path, rpath, array, idarray, patharray, ctime):
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
                if(rpath != ""):
                    rpath2 = rpath + "/" + list[i];
                else:
                    rpath2 = rpath + list[i];
                tmp = spath;
                s3 = os.path.join(tmp, "pfx")
                if(os.path.isdir(s3) == True):
                    s1 = os.path.join(s3, "dosdevices")
                    s2 = os.path.join(s3, "drive_c")
                    if(os.path.isdir(s1) == True):
                        if(os.path.isdir(s2) == True):
                            sdir = sdir + "ID: " + str(j) + " | " + rpath + "/" + list[i] + "\n";
                            idarray.append(j);
                            s1 = rpath + "/" + list[i];
                            patharray.append(spath);
                            ctime.append("");
                            i =  i+1;
                            if( i== size):
                                break;
                            continue;


                else:
                    s1 = os.path.join(s3, "dosdevices")
                    s2 = os.path.join(s3, "drive_c")
                    if(os.path.isdir(s1) == True):
                        if(os.path.isdir(s2) == True):
                            sdir = sdir + "ID: " + str(j) + " | " + rpath + "/" + list[i] + "\n";
                            idarray.append(j);
                            s1 = rpath + "/" + list[i];
                            patharray.append(spath);
                            ctime.append("");
                            i =  i+1;
                            if( i== size):
                                break;
                            continue;
                i =  i+1;
                array = [j, sdir];
                array = listpath_only_dirs(spath, rpath2, array, idarray, patharray, ctime);
                idarray = array[2];
                patharray = array[3];
                ctime = array[4];
                j = array[0];
                sdir = array[1];
                if( i== size):
                    break;
            else:
                #sdir = sdir + "ID: " + str(j) + " | " + rpath + "/" + list[i] + "\n";
                #idarray.append(j);
                #s1 = rpath + "/" + list[i];
                #patharray.append(s1);
                #ctime.append("");
                i = i+ 1;
                j = j +1;
                if( i== size):
                    break;
        return [j, sdir, idarray, patharray, ctime]

def find_wine_prefix(folder):
    array = [0, ""];
    array = listpath_only_dirs(folder, "", array, [], [], [])
    patharray = array[3];
    wine_dir = [];
    proton_dir = [];
    for tmp in patharray:
        s3 = os.path.join(tmp, "pfx")
        if(os.path.isdir(s3) == True):
            proton_dir.append(tmp);
        else:
            wine_dir.append(tmp);
    return [wine_dir, proton_dir];
