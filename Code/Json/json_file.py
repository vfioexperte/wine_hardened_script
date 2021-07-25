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

def brechen_config(name, value):
    return [name, value]

def file_write_json(sfile, docker_user, gpu_render, disk_device_name, zugriff_auf_media, sav_home_docker_folder, share_folder_daten, share_folder1_aktiv, share_folder1, network_disable, steam_controller_bool, usb_sharing, usb_name, usb_hidraw_name, docker_build, maxmemory, maxcpus, network_host, portforwding, dbus_rw, pacman_cache, dns, ipv4, wireguard_fix, nosudo, run_in_background, ttyon, pacman_pakgage_install, docker_input):
    jason_data['sav_data'] = {'docker_user': docker_user, 'gpu_render' : gpu_render, 'disk_device_name' : disk_device_name, "zugriff_auf_media": zugriff_auf_media, "sav_home_docker_folder" : sav_home_docker_folder, "share_folder_daten" : share_folder_daten, "share_folder1_aktiv" : share_folder1_aktiv, "network_disable" : network_disable, "steam_controller_bool" : steam_controller_bool, "usb_sharing": usb_sharing, "usb_name" : usb_name, "usb_hidraw_name" : usb_hidraw_name, "docker_build" : docker_build , "docker_input" : docker_input, "maxmemory" : maxmemory, "maxcpus" : maxcpus, "network_host" : network_host, "portforwding" : portforwding, "dbus_rw" : dbus_rw, "pacman_cache" : pacman_cache, "dns" : dns, "ipv4" : ipv4, "wireguard_fix" : wireguard_fix, "nosudo" : nosudo, "run_in_background" : run_in_background, "ttyon": ttyon, "pacman_pakgage_install" : pacman_pakgage_install, "share_folder1": share_folder1};
    with open(sfile, "w") as write_file:
        json.dump(jason_data, write_file);
        write_file.close();
    return 0;

def file_read_json(sfile):
    if(os.path.isfile(sfile) == False):
        return [];
    out = [];
    with open(sfile, "r") as read_file:
        try:
            jason_data  = json.load(read_file)
            out.append(brechen_config('docker_user', jason_data['sav_data']['docker_user']))
            out.append(brechen_config('gpu_render', jason_data['sav_data']['gpu_render']))
            out.append(brechen_config('disk_device_name', jason_data['sav_data']['disk_device_name']))
            out.append(brechen_config('zugriff_auf_media', jason_data['sav_data']['zugriff_auf_media']))
            out.append(brechen_config('sav_home_docker_folder', jason_data['sav_data']['sav_home_docker_folder']))
            out.append(brechen_config('share_folder_daten', jason_data['sav_data']['share_folder_daten']))
            out.append(brechen_config('share_folder1_aktiv', jason_data['sav_data']['share_folder1_aktiv']))
            out.append(brechen_config('share_folder1', jason_data['sav_data']['share_folder1']))
            out.append(brechen_config('network_disable', jason_data['sav_data']['network_disable']))
            out.append(brechen_config('steam_controller_bool', jason_data['sav_data']['steam_controller_bool']))
            out.append(brechen_config('usb_sharing', jason_data['sav_data']['usb_sharing']))
            out.append(brechen_config('usb_name', jason_data['sav_data']['usb_name']))
            out.append(brechen_config('usb_hidraw_name', jason_data['sav_data']['usb_hidraw_name']))
            out.append(brechen_config('docker_build', jason_data['sav_data']['docker_build']))
            out.append(brechen_config('maxmemory', jason_data['sav_data']['maxmemory']))
            out.append(brechen_config('maxcpus', jason_data['sav_data']['maxcpus']))
            out.append(brechen_config('network_host', jason_data['sav_data']['network_host']))
            out.append(brechen_config('portforwding', jason_data['sav_data']['portforwding']))
            out.append(brechen_config('dbus_rw', jason_data['sav_data']['dbus_rw']))
            out.append(brechen_config('pacman_cache', jason_data['sav_data']['pacman_cache']))
            out.append(brechen_config('dns', jason_data['sav_data']['dns']))
            out.append(brechen_config('ipv4', jason_data['sav_data']['ipv4']))
            out.append(brechen_config('wireguard_fix', jason_data['sav_data']['wireguard_fix']))
            out.append(brechen_config('nosudo', jason_data['sav_data']['nosudo']))
            out.append(brechen_config('run_in_background', jason_data['sav_data']['run_in_background']))
            out.append(brechen_config('ttyon', jason_data['sav_data']['ttyon']))
            out.append(brechen_config('pacman_pakgage_install', jason_data['sav_data']['pacman_pakgage_install']))
            out.append(brechen_config('docker_input', jason_data['sav_data']['docker_input']))
            read_file.close();
            return out;
        except json.decoder.JSONDecodeError:
            return [];
    return [];
