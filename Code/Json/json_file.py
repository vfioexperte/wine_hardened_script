#!/usr/bin/env python
#Copyright (C) 2022  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#this is a fork from https://github.com/kritzsie/steam-on-docker

version = "0.8a"
#0.4c lxc support 0.1a
#0.3l_hotfix_2 optional_array empty array[0] fix 0.1a
#0.3l optional_array and freesync, vsync
#0.3j optional_array and smart_acces_meomory add

import platform
import os
import sys
import string
import subprocess
import time
import math
import json

from Code.Crypt.rsa_lib import *
jason_data = {};

config_file = ".config";
config_file_json = "config.json";


def brechen_config(name, value):
    return [name, value]

def file_write_json(sfile, docker_user, gpu_render, disk_device_name, zugriff_auf_media, sav_home_docker_folder, share_folder_daten, share_folder1_aktiv, share_folder1, network_disable, steam_controller_bool, usb_sharing, usb_name, usb_hidraw_name, docker_build, maxmemory, maxcpus, network_host, portforwding, dbus_rw, pacman_cache, dns, ipv4, wireguard_fix, nosudo, run_in_background, ttyon, pacman_pakgage_install, docker_input, bluethoot_passthrough, hidraw_acs_overrides_patch, ipv6_privacy,
                    faketime, wine_32bit_speed_hak, read_only, read_only_password,  amd_gpu_raytrasing_allgpus, amd_gpu_raytrasing_rdan2_only, wine_fsr, manager_vm_fodler, optional_array):
    #print("read_only: ", read_only)
    #print("read_only_password: ", read_only_password)
    if(read_only == "1" and read_only_password != ""):
        key = rsa_gerate_keys();
        jason_data['sav_data'] = {'docker_user': rsa_encrypt_str(docker_user, key), 'gpu_render' : rsa_encrypt_str(gpu_render, key), 'disk_device_name' : rsa_encrypt_str(disk_device_name, key), "zugriff_auf_media": rsa_encrypt_str(zugriff_auf_media, key), "sav_home_docker_folder" : rsa_encrypt_str(sav_home_docker_folder, key), "share_folder_daten" : rsa_encrypt_str(share_folder_daten, key), "share_folder1_aktiv" : rsa_encrypt_str(share_folder1_aktiv, key), "network_disable" : rsa_encrypt_str(network_disable, key), "steam_controller_bool" : rsa_encrypt_str(steam_controller_bool, key), "usb_sharing": rsa_encrypt_str(usb_sharing, key), "usb_name" : rsa_encrypt_str(usb_name, key), "usb_hidraw_name" : rsa_encrypt_str(usb_hidraw_name, key), "docker_build" : rsa_encrypt_str(docker_build, key), "docker_input" : rsa_encrypt_str(docker_input, key), "maxmemory" : rsa_encrypt_str(maxmemory, key), "maxcpus" : rsa_encrypt_str(maxcpus, key), "network_host" : rsa_encrypt_str(network_host, key), "portforwding" : rsa_encrypt_str(portforwding, key), "dbus_rw" : rsa_encrypt_str(dbus_rw, key), "pacman_cache" : rsa_encrypt_str(pacman_cache, key), "dns" : rsa_encrypt_str(dns, key), "ipv4" : rsa_encrypt_str(ipv4, key), "wireguard_fix" : rsa_encrypt_str(wireguard_fix, key), "nosudo" : rsa_encrypt_str(nosudo, key), "run_in_background" : rsa_encrypt_str(run_in_background, key), "ttyon": rsa_encrypt_str(ttyon, key), "pacman_pakgage_install" : rsa_encrypt_str(pacman_pakgage_install, key), "share_folder1": rsa_encrypt_str(share_folder1, key), "bluethoot_passthrough" : rsa_encrypt_str(bluethoot_passthrough, key), "hidraw_acs_overrides_patch" : rsa_encrypt_str(hidraw_acs_overrides_patch, key), "ipv6_privacy" : rsa_encrypt_str(ipv6_privacy, key), "faketime": rsa_encrypt_str(faketime, key), "wine_32bit_speed_hak" : rsa_encrypt_str(wine_32bit_speed_hak, key), "read_only" : byte_to_hex(key), "read_only_password" : rsa_encrypt_str(read_only_password, key), "amd_gpu_raytrasing_allgpus" : rsa_encrypt_str(amd_gpu_raytrasing_allgpus, key) ,"amd_gpu_raytrasing_rdan2_only" : rsa_encrypt_str(amd_gpu_raytrasing_rdan2_only, key), "wine_fsr" : rsa_encrypt_str(wine_fsr, key), "manager_vm_fodler" : rsa_encrypt_str(manager_vm_fodler, key), "optional_array" : rsa_encrypt_str(optional_array, key), "sav_Version" :  "0.3j_crypt"};
        with open(sfile, "w") as write_file:
            json.dump(jason_data, write_file);
            write_file.close();
        return 0;
    else:
        jason_data['sav_data'] = {'docker_user': docker_user, 'gpu_render' : gpu_render, 'disk_device_name' : disk_device_name, "zugriff_auf_media": zugriff_auf_media, "sav_home_docker_folder" : sav_home_docker_folder, "share_folder_daten" : share_folder_daten, "share_folder1_aktiv" : share_folder1_aktiv, "network_disable" : network_disable, "steam_controller_bool" : steam_controller_bool, "usb_sharing": usb_sharing, "usb_name" : usb_name, "usb_hidraw_name" : usb_hidraw_name, "docker_build" : docker_build , "docker_input" : docker_input, "maxmemory" : maxmemory, "maxcpus" : maxcpus, "network_host" : network_host, "portforwding" : portforwding, "dbus_rw" : dbus_rw, "pacman_cache" : pacman_cache, "dns" : dns, "ipv4" : ipv4, "wireguard_fix" : wireguard_fix, "nosudo" : nosudo, "run_in_background" : run_in_background, "ttyon": ttyon, "pacman_pakgage_install" : pacman_pakgage_install, "share_folder1": share_folder1, "bluethoot_passthrough" : bluethoot_passthrough, "hidraw_acs_overrides_patch" : hidraw_acs_overrides_patch, "ipv6_privacy" : ipv6_privacy, "faketime": faketime, "wine_32bit_speed_hak" : wine_32bit_speed_hak, "read_only" : 0, "read_only_password" : "", "amd_gpu_raytrasing_allgpus" : amd_gpu_raytrasing_allgpus, "amd_gpu_raytrasing_rdan2_only": amd_gpu_raytrasing_rdan2_only, "wine_fsr": wine_fsr, "manager_vm_fodler": manager_vm_fodler, "optional_array": optional_array, "sav_Version" :  "0.3j"};
        with open(sfile, "w") as write_file:
            json.dump(jason_data, write_file);
            write_file.close();
        return 0;

def file_json_check_Version(sfile):
    if(os.path.isfile(sfile) == False):
        return -1;
    try:
        with open(sfile, "r") as read_file:
            jason_data  = json.load(read_file)
            sav_Verion = jason_data['sav_data']['sav_Version'];
            return sav_Verion;
    except json.decoder.JSONDecodeError:
        return "0.1";
    except PermissionError:
        return -1;
    except KeyError:
        return "0.1";
    return -1;


def loading_json_file(sfile):
    check = file_json_check_Version(sfile);
    if(check == "0.1"):
        return file_read_json_0_1(sfile);
    elif(check == "0.2d"):
        return file_read_json(sfile);
    elif(check == "0.2b"):
        return file_read_json(sfile);
    elif(check == "0.3a"):
        return file_read_json(sfile);
    elif(check == "0.3c"):
        return file_read_json(sfile);
    elif(check == "0.3e"):
        return file_read_json(sfile);
    elif(check == "0.3f"):
        return file_read_json(sfile);
    elif(check == "0.3g"):
        return file_read_json(sfile);
    elif(check == "0.3h"):
        return file_read_json(sfile);
    elif(check == "0.3i"):
        return file_read_json(sfile);
    elif(check == "0.3j"):
        return file_read_json(sfile);
    elif(check == "0.3f_crypt"):
        return file_read_json(sfile);
    elif(check == "0.3g_crypt"):
        return file_read_json(sfile);
    elif(check == "0.3h_crypt"):
        return file_read_json(sfile);
    elif(check == "0.3i_crypt"):
        return file_read_json(sfile);
    elif(check == "0.3j_crypt"):
        return file_read_json(sfile);
    elif(check == -1):
        return read_config();
    else:
        print("canot loading config file json to new!");
        exit(-1);

def file_read_json(sfile):
    if(os.path.isfile(sfile) == False):
        return [];
    out = [];
    try:
        with open(sfile, "r") as read_file:
            jason_data  = json.load(read_file)
            #out.append(brechen_config('sav_Version', jason_data['sav_data']['sav_Version']))
            sav_Verion = jason_data['sav_data']['sav_Version'];
            if(sav_Verion == "0.3f_crypt" or sav_Verion == "0.3g_crypt" or sav_Verion ==  "0.3h_crypt" or sav_Verion ==  "0.3i_crypt" or sav_Verion == "0.3j_crypt"):
                        key = hex_to_byte(jason_data['sav_data']['read_only']);
                        out = [];
                        out.append(brechen_config('read_only', 1));
                        out.append(brechen_config('read_only_password', rsa_decrypt_byte(jason_data['sav_data']['read_only_password'], key).decode("utf-8")))
                        out.append(brechen_config('wine_32bit_speed_hak', rsa_decrypt_byte(jason_data['sav_data']['wine_32bit_speed_hak'], key).decode("utf-8")))
                        out.append(brechen_config('faketime', rsa_decrypt_byte(jason_data['sav_data']['faketime'], key).decode("utf-8")))
                        out.append(brechen_config('ipv6_privacy', rsa_decrypt_byte(jason_data['sav_data']['ipv6_privacy'], key).decode("utf-8")))
                        out.append(brechen_config('hidraw_acs_overrides_patch', rsa_decrypt_byte(jason_data['sav_data']['hidraw_acs_overrides_patch'], key).decode("utf-8")))
                        out.append(brechen_config('docker_user', rsa_decrypt_byte(jason_data['sav_data']['docker_user'], key).decode("utf-8")))
                        out.append(brechen_config('gpu_render', rsa_decrypt_byte(jason_data['sav_data']['gpu_render'], key).decode("utf-8")));
                        out.append(brechen_config('disk_device_name', rsa_decrypt_byte(jason_data['sav_data']['disk_device_name'], key).decode("utf-8")))
                        out.append(brechen_config('zugriff_auf_media', rsa_decrypt_byte(jason_data['sav_data']['zugriff_auf_media'], key).decode("utf-8")))
                        out.append(brechen_config('sav_home_docker_folder', rsa_decrypt_byte(jason_data['sav_data']['sav_home_docker_folder'], key).decode("utf-8")))
                        out.append(brechen_config('share_folder_daten', rsa_decrypt_byte(jason_data['sav_data']['share_folder_daten'], key).decode("utf-8")))
                        out.append(brechen_config('share_folder1_aktiv', rsa_decrypt_byte(jason_data['sav_data']['share_folder1_aktiv'], key).decode("utf-8")))
                        out.append(brechen_config('share_folder1', rsa_decrypt_byte(jason_data['sav_data']['share_folder1'], key).decode("utf-8")))
                        out.append(brechen_config('network_disable', rsa_decrypt_byte(jason_data['sav_data']['network_disable'], key).decode("utf-8")))
                        out.append(brechen_config('steam_controller_bool', rsa_decrypt_byte(jason_data['sav_data']['steam_controller_bool'], key).decode("utf-8")))
                        out.append(brechen_config('usb_sharing', rsa_decrypt_byte(jason_data['sav_data']['usb_sharing'], key).decode("utf-8")))
                        out.append(brechen_config('usb_name', rsa_decrypt_byte(jason_data['sav_data']['usb_name'], key).decode("utf-8")))
                        out.append(brechen_config('usb_hidraw_name', rsa_decrypt_byte(jason_data['sav_data']['usb_hidraw_name'], key).decode("utf-8")))
                        out.append(brechen_config('docker_build', rsa_decrypt_byte(jason_data['sav_data']['docker_build'], key).decode("utf-8")))
                        out.append(brechen_config('maxmemory', rsa_decrypt_byte(jason_data['sav_data']['maxmemory'], key).decode("utf-8")))
                        out.append(brechen_config('maxcpus', rsa_decrypt_byte(jason_data['sav_data']['maxcpus'], key).decode("utf-8")))
                        out.append(brechen_config('network_host', rsa_decrypt_byte(jason_data['sav_data']['network_host'], key).decode("utf-8")))
                        out.append(brechen_config('portforwding', rsa_decrypt_byte(jason_data['sav_data']['portforwding'], key).decode("utf-8")))
                        out.append(brechen_config('dbus_rw', rsa_decrypt_byte(jason_data['sav_data']['dbus_rw'], key).decode("utf-8")))
                        out.append(brechen_config('pacman_cache', rsa_decrypt_byte(jason_data['sav_data']['pacman_cache'], key).decode("utf-8")))
                        out.append(brechen_config('dns', rsa_decrypt_byte(jason_data['sav_data']['dns'], key).decode("utf-8")))
                        out.append(brechen_config('ipv4', rsa_decrypt_byte(jason_data['sav_data']['ipv4'], key).decode("utf-8")))
                        out.append(brechen_config('wireguard_fix', rsa_decrypt_byte(jason_data['sav_data']['wireguard_fix'], key).decode("utf-8")))
                        out.append(brechen_config('nosudo', rsa_decrypt_byte(jason_data['sav_data']['nosudo'], key).decode("utf-8")))
                        out.append(brechen_config('run_in_background', rsa_decrypt_byte(jason_data['sav_data']['run_in_background'], key).decode("utf-8")))
                        out.append(brechen_config('ttyon', rsa_decrypt_byte(jason_data['sav_data']['ttyon'], key).decode("utf-8")))
                        out.append(brechen_config('pacman_pakgage_install', rsa_decrypt_byte(jason_data['sav_data']['pacman_pakgage_install'], key).decode("utf-8")))
                        out.append(brechen_config('docker_input', rsa_decrypt_byte(jason_data['sav_data']['docker_input'], key).decode("utf-8")))
                        out.append(brechen_config('bluethoot_passthrough', rsa_decrypt_byte(jason_data['sav_data']['bluethoot_passthrough'], key).decode("utf-8")))
                        out.append(brechen_config('sav_Version', jason_data['sav_data']['sav_Version']))
                        if(sav_Verion == "0.3g_crypt" or sav_Verion ==  "0.3h_crypt" or sav_Verion ==  "0.3i_crypt" or sav_Verion == "0.3j_crypt"):
                            out.append(brechen_config('amd_gpu_raytrasing_allgpus', rsa_decrypt_byte(jason_data['sav_data']['amd_gpu_raytrasing_allgpus'], key).decode("utf-8")))
                            out.append(brechen_config('amd_gpu_raytrasing_rdan2_only', rsa_decrypt_byte(jason_data['sav_data']['amd_gpu_raytrasing_rdan2_only'], key).decode("utf-8")))
                        if(sav_Verion ==  "0.3h_crypt" or sav_Verion ==  "0.3i_crypt" or "0.3j_crypt"):
                            out.append(brechen_config('wine_fsr', rsa_decrypt_byte(jason_data['sav_data']['wine_fsr'], key).decode("utf-8")))
                        if(sav_Verion ==  "0.3i_crypt" or sav_Verion == "0.3j_crypt"):
                            out.append(brechen_config('manager_vm_fodler', rsa_decrypt_byte(jason_data['sav_data']['manager_vm_fodler'], key).decode("utf-8")))
                        if(sav_Verion == "0.3j_crypt"):
                            optional_array =  rsa_decrypt_byte(jason_data['sav_data']['optional_array'], key).decode("utf-8")
                            out = optional_array_to_out(out, optional_array);
                            out.append(brechen_config("optional_array", optional_array));
                        read_file.close();
                        return out;
            if( sav_Verion ==  "0.3j"):
                optional_array =  jason_data['sav_data']['optional_array'];
                out = optional_array_to_out(out, optional_array);
                out.append(brechen_config("optional_array", optional_array));
            if(sav_Verion ==  "0.3i" or sav_Verion ==  "0.3j"):
                out.append(brechen_config('manager_vm_fodler', jason_data['sav_data']['manager_vm_fodler']))
            if(sav_Verion ==  "0.3h" or sav_Verion ==  "0.3i" or sav_Verion ==  "0.3j"):
                out.append(brechen_config('wine_fsr', jason_data['sav_data']['wine_fsr']))
            if(sav_Verion == "0.3g" or sav_Verion ==  "0.3h" or sav_Verion ==  "0.3i" or sav_Verion ==  "0.3j"):
                out.append(brechen_config('amd_gpu_raytrasing_allgpus', jason_data['sav_data']['amd_gpu_raytrasing_allgpus']))
                out.append(brechen_config('amd_gpu_raytrasing_rdan2_only', jason_data['sav_data']['amd_gpu_raytrasing_rdan2_only']))
            if(sav_Verion == "0.3f" or sav_Verion == "0.3g" or sav_Verion ==  "0.3h" or sav_Verion ==  "0.3i" or sav_Verion ==  "0.3j"):
                out.append(brechen_config('read_only', jason_data['sav_data']['read_only']))
                out.append(brechen_config('read_only_password', jason_data['sav_data']['read_only_password']))
            if(sav_Verion == "0.3e" or sav_Verion == "0.3f" or sav_Verion == "0.3g" or sav_Verion ==  "0.3h" or sav_Verion ==  "0.3i" or sav_Verion ==  "0.3j"):
                out.append(brechen_config('wine_32bit_speed_hak', jason_data['sav_data']['wine_32bit_speed_hak']))
            if(sav_Verion == "0.3c" or sav_Verion == "0.3e" or sav_Verion == "0.3f" or sav_Verion == "0.3g" or sav_Verion ==  "0.3h" or sav_Verion ==  "0.3i" or sav_Verion ==  "0.3j"):
                out.append(brechen_config('faketime', jason_data['sav_data']['faketime']))
            if(sav_Verion == "0.3a" or sav_Verion == "0.3c" or sav_Verion == "0.3e" or sav_Verion == "0.3f" or sav_Verion == "0.3g" or sav_Verion ==  "0.3h" or sav_Verion ==  "0.3i" or sav_Verion ==  "0.3j"):
                out.append(brechen_config('ipv6_privacy', jason_data['sav_data']['ipv6_privacy']))
            if(sav_Verion == "0.2d"or sav_Verion == "0.3a" or sav_Verion == "0.3c" or sav_Verion == "0.3e" or sav_Verion == "0.3f" or sav_Verion == "0.3g" or sav_Verion ==  "0.3h" or sav_Verion ==  "0.3i" or sav_Verion ==  "0.3j"):
                out.append(brechen_config('hidraw_acs_overrides_patch', jason_data['sav_data']['hidraw_acs_overrides_patch']))
            if(sav_Verion == "0.2b" or sav_Verion == "0.2d" or sav_Verion == "0.3a" or sav_Verion == "0.3c" or sav_Verion == "0.3e" or sav_Verion == "0.3f" or sav_Verion == "0.3g" or sav_Verion ==  "0.3h" or sav_Verion ==  "0.3i" or sav_Verion ==  "0.3j"):
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
                out.append(brechen_config('bluethoot_passthrough', jason_data['sav_data']['bluethoot_passthrough']))
                read_file.close();
            return out;
    except json.decoder.JSONDecodeError:
        return [];
    except PermissionError:
        return [];
    except KeyError:
        return [];
    return [];

def optional_array_to_out(out, array_str):
    if(array_str == ""):
        return out;
    array = array_str.split("^");
    if(len(array) >= 1 and array[0] != ""):
        out.append(brechen_config('smart_acces_meomory', array[0]));
    if(len(array) >= 2 and array[1] != ""):
        out.append(brechen_config('vulkan_device_name', array[1]));
    if(len(array) >= 3 and array[2] != ""):
        out.append(brechen_config('steam_proton_run_without_steam', array[2]));
    if(len(array) >= 4 and array[3] != ""):
        out.append(brechen_config('mango_hud', array[3]));
    if(len(array) >= 5 and array[4] != ""):
        out.append(brechen_config('vkbasalt', array[4]));
    if(len(array) >= 6 and array[5] != ""):
        out.append(brechen_config('freesync', array[5]));
    if(len(array) >= 7 and array[6] != ""):
        out.append(brechen_config('vsync', array[6]));
    if(len(array) >= 8 and array[7] != ""):
        out.append(brechen_config('docker_system', array[7]));
    if(len(array) >= 9 and array[8] != ""):
        out.append(brechen_config('lxc_readonly', array[8]));
    if(len(array) >= 10 and array[9] != ""):
        out.append(brechen_config('lxc_network_mac', array[9]));
    if(len(array) >= 11 and array[10] != ""):
        out.append(brechen_config('lxc_network_bridge_link', array[10]));
    if(len(array) >= 12 and array[11] != ""):
        out.append(brechen_config('docker_disable_ipv6', array[11]));
    if(len(array) >= 13 and array[12] != ""):
        out.append(brechen_config('nvidia_dlss', array[12]));
    if(len(array) >= 14 and array[13] != ""):
        out.append(brechen_config('nvidia_dlss_non_nvida_gpu', array[13]));
    if(len(array) >= 15 and array[14] != ""):
        out.append(brechen_config('wineesync_and_winefsync', array[14]));
    if(len(array) >= 16 and array[15] != ""):
        out.append(brechen_config('pulseaudio_stotterfix', array[15]));
    if(len(array) >= 17 and array[16] != ""):
        out.append(brechen_config('amdgpu_nohyperz', array[16]));
    if(len(array) >= 18 and array[17] != ""):
        out.append(brechen_config('amdgpu_pswave32', array[17]));
    if(len(array) >= 19 and array[18] != ""):
        out.append(brechen_config('amdgpu_nv_ms', array[18]));
    if(len(array) >= 20 and array[19] != ""):
        out.append(brechen_config('amdgpu_vrs', array[19]));
    if(len(array) >= 21 and array[20] != ""):
        out.append(brechen_config('pluseaudio_sdl_fix', array[20]));
    if(len(array) >= 22 and array[21] != ""):
        out.append(brechen_config('docker_auto_sav_folder', array[21]));
    if(len(array) >= 23 and array[22] != ""):
        out.append(brechen_config('dhcpv6', array[22]));
    if(len(array) >= 24 and array[23] != ""):
        out.append(brechen_config('amdgpu_mesh_shader_support', array[23]));
    if(len(array) >= 25 and array[24] != ""):
        out.append(brechen_config('podman_runs_root', array[24]));
    if(len(array) >= 26 and array[25] != ""):
        out.append(brechen_config('podman_set_route_gateway_ip', array[25]));
    if(len(array) >= 27 and array[26] != ""):
        out.append(brechen_config('ipv6', array[26]));
    if(len(array) >= 28 and array[27] != ""):
        out.append(brechen_config('amdgpu_gpl_pipline', array[27]));
    if(len(array) >= 29 and array[28] != ""):
        out.append(brechen_config('rest_config', array[28]));
    if(len(array) >= 30 and array[29] != ""):
        out.append(brechen_config('ubisoft_connect_mut_fix', array[29]));
    if(len(array) >= 31 and array[30] != ""):
        out.append(brechen_config('vk_khr_present_wait', array[30]));
    if(len(array) >= 32 and array[31] != ""):
        out.append(brechen_config('docker_user_password', array[31]));
    if(len(array) >= 33 and array[32] != ""):
        out.append(brechen_config('gamescope_bypass', array[32]));
    if(len(array) >= 34 and array[33] != ""):
        out.append(brechen_config('ryujinx_emu_crash_fix', array[33]));
    if(len(array) >= 35 and array[34] != ""):
        out.append(brechen_config('gamescope_render_auflosung', array[34]));
    return out;

def file_read_json_0_1(sfile):
    if(os.path.isfile(sfile) == False):
        return [];
    out = [];
    try:
            with open(sfile, "r") as read_file:
                jason_data  = json.load(read_file)
                #out.append(brechen_config('sav_Version', jason_data['sav_data']['sav_Version']))
                #sav_Verion = jason_data['sav_data']['sav_Version'];
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
                #out.append(brechen_config('bluethoot_passthrough', jason_data['sav_data']['bluethoot_passthrough']))
                read_file.close();
            return out;
    except json.decoder.JSONDecodeError:
        return [];
    except PermissionError:
        return [];
    except KeyError:
        return [];
    return [];

def read_config():
    if(os.path.isfile(config_file) == False):
        print("read_config() ERROR not found " + config_file + " file in the fodler");
        exit(1);
    file1 = open(config_file, "r");
    file1.seek(0, 2);
    size = file1.tell();
    file1.seek(0, 0);
    b1 = file1.read(size);
    file1.close();
    i = 0;
    config = [];
    config_temp = "";
    config_temp1 = [];
    l1 = -1;
    l2 = -1;
    while True:
        if(i >= len(b1)):
            break;
        if(i + 11 < len(b1) and (b1[i] == 'd' and b1[i+1] == 'o' ) and (b1[i+2] == 'c' and b1[i+3] == 'k' ) and (b1[i+4] == 'e' and b1[i+5] == 'r' ) and (b1[i+6] == '_' and b1[i+7] == 'u' ) and (b1[i+8] == 's' and b1[i+9] == 'e' ) and (b1[i+10] == 'r' )):
            l1 = 1;
        elif(i + 10 < len(b1) and (b1[i] == 'g' and b1[i+1] == 'p' ) and (b1[i+2] == 'u' and b1[i+3] == '_' ) and (b1[i+4] == 'r' and b1[i+5] == 'e' ) and (b1[i+6] == 'n' and b1[i+7] == 'd' ) and (b1[i+8] == 'e' and b1[i+9] == 'r' )):
             l1 = 2;
        elif(i + 15 < len(b1) and (b1[i] == 'd' and b1[i+1] == 'i' ) and (b1[i+2] == 's' and b1[i+3] == 'k' ) and (b1[i+4] == '_' and b1[i+5] == 'd' ) and (b1[i+6] == 'e' and b1[i+7] == 'v' ) and (b1[i+8] == 'i' and b1[i+9] == 'c' ) and (b1[i+10] == 'e'  and  b1[i+11] == '_' ) and   (b1[i+12] == 'n'  and  b1[i+13] == 'a' ) and (b1[i+14] == 'm'  and  b1[i+15] == 'e' )):
            l1 = 3;
        elif(i + 16 < len(b1) and (b1[i] == 'z' and b1[i+1] == 'u' ) and (b1[i+2] == 'g' and b1[i+3] == 'r' ) and (b1[i+4] == 'i' and b1[i+5] == 'f' ) and (b1[i+6] == 'f' and b1[i+7] == '_' ) and (b1[i+8] == 'a' and b1[i+9] == 'u' ) and (b1[i+10] == 'f'  and  b1[i+11] == '_' ) and   (b1[i+12] == 'm'  and  b1[i+13] == 'e' ) and (b1[i+14] == 'd'  and  b1[i+15] == 'i' ) and  b1[i+16] == 'a' ):
            l1 = 4;
        elif(i + 21 < len(b1) and (b1[i] == 's' and b1[i+1] == 'a' ) and (b1[i+2] == 'v' and b1[i+3] == '_' ) and (b1[i+4] == 'h' and b1[i+5] == 'o' ) and (b1[i+6] == 'm' and b1[i+7] == 'e' ) and (b1[i+8] == '_' and b1[i+9] == 'd' ) and (b1[i+10] == 'o'  and  b1[i+11] == 'c' ) and   (b1[i+12] == 'k'  and  b1[i+13] == 'e' ) and (b1[i+14] == 'r'  and  b1[i+15] == '_' ) and  (b1[i+16] == 'f' and b1[i+17] == 'o') and (b1[i+18] == 'l' and b1[i+19] == 'd') and  (b1[i+20] == 'e' and b1[i+21] == 'r') ):
            l1 = 5;
        elif(i + 11 < len(b1) and (b1[i] == 's' and b1[i+1] == 'h' ) and (b1[i+2] == 'a' and b1[i+3] == 'r' ) and (b1[i+4] == 'e' and b1[i+5] == '_' ) and (b1[i+6] == 'f' and b1[i+7] == 'o' ) and (b1[i+8] == 'l' and b1[i+9] == 'd' ) and (b1[i+10] == 'e'  and  b1[i+11] == 'r' )):
            if(i + 17 < len(b1) and (b1[i+12] == '_' and b1[i+13] == 'd' ) and (b1[i+14] == 'a' and b1[i+15] == 't' ) and (b1[i+16] == 'e' and b1[i+17] == 'n' )):
                l1 = 6;
            elif(i + 18 < len(b1) and (b1[i+12] == '1' and b1[i+13] == '_' ) and (b1[i+14] == 'a' and b1[i+15] == 'k' ) and (b1[i+16] == 't' and b1[i+17] == 'i' )  and (b1[i+18] == 'v')):
                l1 = 7;
            elif(i + 18 < len(b1) and (b1[i+12] == '1')):
                l1 = 8;
        elif(i + 13 < len(b1) and (b1[i] == 'n' and b1[i+1] == 'e' ) and (b1[i+2] == 't' and b1[i+3] == 'w' ) and (b1[i+4] == 'o' and b1[i+5] == 'r' ) and (b1[i+6] == 'k' and b1[i+7] == '_' ) and (b1[i+8] == 'd' and b1[i+9] == 'i' ) and (b1[i+10] == 's'  and  b1[i+11] == 'a' ) and   (b1[i+12] == 'b'  and  b1[i+13] == 'l' ) ):
            l1 = 9;
        elif(i + 20 < len(b1) and (b1[i] == 's' and b1[i+1] == 't' ) and (b1[i+2] == 'e' and b1[i+3] == 'a' ) and (b1[i+4] == 'm' and b1[i+5] == '_' ) and (b1[i+6] == 'c' and b1[i+7] == 'o' ) and (b1[i+8] == 'n' and b1[i+9] == 't' ) and (b1[i+10] == 'r'  and  b1[i+11] == 'o' ) and   (b1[i+12] == 'l'  and  b1[i+13] == 'l' ) and (b1[i+14] == 'e'  and  b1[i+15] == 'r' ) and (b1[i+16] == '_'  and  b1[i+17] == 'b' )and (b1[i+18] == 'o'  and  b1[i+19] == 'o' )and  b1[i+20] == 'l' ):
            l1 = 10;
        elif(i + 10 < len(b1) and (b1[i] == 'u' and b1[i+1] == 's' ) and (b1[i+2] == 'b' and b1[i+3] == '_' ) and (b1[i+4] == 's' and b1[i+5] == 'h' ) and (b1[i+6] == 'a' and b1[i+7] == 'r' ) and (b1[i+8] == 'i' and b1[i+9] == 'n' ) and (b1[i+10] == 'g' )):
            l1 = 11;
        elif(i + 7 < len(b1) and (b1[i] == 'u' and b1[i+1] == 's' ) and (b1[i+2] == 'b' and b1[i+3] == '_' ) and (b1[i+4] == 'n' and b1[i+5] == 'a' ) and (b1[i+6] == 'm' and b1[i+7] == 'e' ) ):
            l1 = 12;
        elif(i + 14 < len(b1) and (b1[i] == 'u' and b1[i+1] == 's' ) and (b1[i+2] == 'b' and b1[i+3] == '_' ) and (b1[i+4] == 'h' and b1[i+5] == 'i' ) and (b1[i+6] == 'd' and b1[i+7] == 'r' ) and (b1[i+8] == 'a' and b1[i+9] == 'w' ) and (b1[i+10] == '_'  and  b1[i+11] == 'n' ) and   (b1[i+12] == 'a'  and  b1[i+13] == 'm' ) and (b1[i+14] == 'e' )):
            l1 = 13;
        elif(i + 11 < len(b1) and (b1[i] == 'd' and b1[i+1] == 'o' ) and (b1[i+2] == 'c' and b1[i+3] == 'k' ) and (b1[i+4] == 'e' and b1[i+5] == 'r' ) and (b1[i+6] == '_' and b1[i+7] == 'b' ) and (b1[i+8] == 'u' and b1[i+9] == 'i' ) and (b1[i+10] == 'l' and b1[i+11] == 'd')):
            l1 = 14;
        elif(i + 11 < len(b1) and (b1[i] == 'd' and b1[i+1] == 'o' ) and (b1[i+2] == 'c' and b1[i+3] == 'k' ) and (b1[i+4] == 'e' and b1[i+5] == 'r' ) and (b1[i+6] == '_' and b1[i+7] == 'i' ) and (b1[i+8] == 'n' and b1[i+9] == 'p' ) and (b1[i+10] == 'u' and b1[i+11] == 't')):
            l1 = 15;
        elif(i + 15 < len(b1) and (b1[i] == 'd' and b1[i+1] == 'o' ) and (b1[i+2] == 'c' and b1[i+3] == 'k' ) and (b1[i+4] == 'e' and b1[i+5] == 'r' ) and (b1[i+6] == '_' and b1[i+7] == 'm' ) and (b1[i+8] == 'a' and b1[i+9] == 'x' ) and (b1[i+10] == 'm' and b1[i+11] == 'e')  and   (b1[i+12] == 'm' and b1[i+13] == 'o') and (b1[i+14] == 'r' and b1[i+15] == 'y') ):
            l1 = 16;#maxmemory
        elif(i + 13 < len(b1) and (b1[i] == 'd' and b1[i+1] == 'o' ) and (b1[i+2] == 'c' and b1[i+3] == 'k' ) and (b1[i+4] == 'e' and b1[i+5] == 'r' ) and (b1[i+6] == '_' and b1[i+7] == 'm' ) and (b1[i+8] == 'a' and b1[i+9] == 'x' ) and (b1[i+10] == 'c' and b1[i+11] == 'p')  and   (b1[i+12] == 'u' and b1[i+13] == 's') ):
            l1 = 17;#maxcpus
        elif(i + 11 < len(b1) and (b1[i] == 'n' and b1[i+1] == 'e' ) and (b1[i+2] == 't' and b1[i+3] == 'w' ) and (b1[i+4] == 'o' and b1[i+5] == 'r' ) and (b1[i+6] == 'k' and b1[i+7] == '_' ) and (b1[i+8] == 'h' and b1[i+9] == 'o' ) and (b1[i+10] == 's' and b1[i+11] == 't')  ):
            l1 = 18;#network_host
        elif(i + 11 < len(b1) and (b1[i] == 'p' and b1[i+1] == 'o' ) and (b1[i+2] == 'r' and b1[i+3] == 't' ) and (b1[i+4] == 'f' and b1[i+5] == 'o' ) and (b1[i+6] == 'r' and b1[i+7] == 'w' ) and (b1[i+8] == 'd' and b1[i+9] == 'i' ) and (b1[i+10] == 'n' and b1[i+11] == 'g')  ):
            l1 = 19;#portforwding
        elif(i + 6 < len(b1) and (b1[i] == 'd' and b1[i+1] == 'b' ) and (b1[i+2] == 'u' and b1[i+3] == 's' ) and (b1[i+4] == '_' and b1[i+5] == 'r' ) and (b1[i+6] == 'w' ) ):
            l1 = 20;#dbus_rw
        elif(i + 11 < len(b1) and (b1[i] == 'p' and b1[i+1] == 'a' ) and (b1[i+2] == 'c' and b1[i+3] == 'm' ) and (b1[i+4] == 'a' and b1[i+5] == 'n' ) and (b1[i+6] == '_' and  b1[i+7] == 'c') and (b1[i+8] == 'a' and  b1[i+9] == 'c') and (b1[i+10] == 'h' and  b1[i+11] == 'e') ):
            l1 = 21;#pacman_cache
        elif(i + 2 < len(b1) and (b1[i] == 'd' and b1[i+1] == 'n' ) and (b1[i+2] == 's') ):
            l1 = 22;#dns
        elif(i + 3 < len(b1) and (b1[i] == 'i' and b1[i+1] == 'p' ) and  (b1[i+2] == 'v' and b1[i+3] == '4' ) ):
            l1 = 23;#ipv4
        elif(i + 12 < len(b1) and (b1[i] == 'w' and b1[i+1] == 'i' ) and  (b1[i+2] == 'r' and b1[i+3] == 'e' ) and (b1[i+4] == 'g' and b1[i+5] == 'u' ) and (b1[i+6] == 'a' and b1[i+7] == 'r' )and (b1[i+8] == 'd' and b1[i+9] == '_' )and (b1[i+10] == 'f' and b1[i+11] == 'i' )and (b1[i+12] == 'x') ):
            l1 = 24;#wireguard_fix
        elif(i + 5 < len(b1) and (b1[i] == 'n' and b1[i+1] == 'o' ) and  (b1[i+2] == 's' and b1[i+3] == 'u' ) and (b1[i+4] == 'd' and b1[i+5] == 'o' )  ):
            l1 = 25#nosudo
        elif(i + 16 < len(b1) and (b1[i] == 'r' and b1[i+1] == 'u' ) and (b1[i+2] == 'n' and b1[i+3] == '_' ) and (b1[i+4] == 'i' and b1[i+5] == 'n' ) and (b1[i+6] == '_' and b1[i+7] == 'b' ) and (b1[i+8] == 'a' and b1[i+9] == 'c' ) and (b1[i+10] == 'k' and b1[i+11] == 'g')  and   (b1[i+12] == 'r' and b1[i+13] == 'o') and (b1[i+14] == 'u' and b1[i+15] == 'n') and (b1[i+16] == 'd') ):
            l1 = 26;#run_in_background
        elif(i + 4 < len(b1) and (b1[i] == 't' and b1[i+1] == 't' ) and (b1[i+2] == 'y' and b1[i+3] == 'o' ) and (b1[i+4] == 'n' )):
            l1 = 27;#ttyon
        elif(i + 21 < len(b1) and (b1[i] == 'p' and b1[i+1] == 'a' ) and (b1[i+2] == 'c' and b1[i+3] == 'm' ) and (b1[i+4] == 'a' and b1[i+5] == 'n' ) and (b1[i+6] == '_' and b1[i+7] == 'p' ) and (b1[i+8] == 'a' and b1[i+9] == 'k' ) and (b1[i+10] == 'g' and b1[i+11] == 'a')  and   (b1[i+12] == 'g' and b1[i+13] == 'e') and b1[i+14] == "_" and (b1[i+15] == 'i' and b1[i+16] == 'n') and (b1[i+17] == 's' and b1[i+18] == 't') and (b1[i+19] == 'a' and b1[i+20] == 'l') and (b1[i+21] == 'l' )):
            l1 = 28#pacman_pakgage_install
        elif(l1 >= 1):
            i = i +1;
            if(b1[i] != ' '):
                #config_temp = config_temp  + b1[i];
                i = i +1;
                while True:
                    if(i >= len(b1)):
                        break;
                    if(b1[i] == '\n'):
                        break;
                    if(b1[i] == '='):
                        l2 = 1;
                        if(b1[i+1] == ' '):
                            i = i +1;
                    elif(l2 == 1):
                        config_temp = config_temp  + b1[i];
                    i = i +1;
                if(l1 == 1):
                    config_temp1.append("docker_user");
                elif(l1 == 2):
                    config_temp1.append("gpu_render");
                elif(l1 == 3):
                    config_temp1.append("disk_device_name");
                elif(l1 == 4):
                    config_temp1.append("zugriff_auf_media");
                elif(l1 == 5):
                    config_temp1.append("sav_home_docker_folder");
                elif(l1 == 6):
                    config_temp1.append("share_folder_daten");
                elif(l1 == 7):
                    config_temp1.append("share_folder1_aktiv");
                elif(l1 == 8):
                    config_temp1.append("share_folder1");
                elif(l1 == 9):
                    config_temp1.append("network_disable");
                elif(l1 == 10):
                    config_temp1.append("steam_controller_bool");
                elif(l1 == 11):
                    config_temp1.append("usb_sharing");
                elif(l1 == 12):
                    config_temp1.append("usb_name");
                elif(l1 == 13):
                    config_temp1.append("usb_hidraw_name");
                elif(l1 == 14):
                    config_temp1.append("docker_build");
                elif(l1 == 15):
                    config_temp1.append("docker_input");
                elif(l1 == 16):
                    config_temp1.append("maxmemory");
                elif(l1 == 17):
                    config_temp1.append("maxcpus");
                elif(l1 == 18):
                    config_temp1.append("network_host");
                elif(l1 == 19):
                    config_temp1.append("portforwding");
                elif(l1 == 20):
                    config_temp1.append("dbus_rw");
                elif(l1 == 21):
                    config_temp1.append("pacman_cache");
                elif(l1 == 22):
                    config_temp1.append("dns");
                elif(l1 == 23):
                    config_temp1.append("ipv4");
                elif(l1 == 24):
                    config_temp1.append("wireguard_fix");
                elif(l1 == 25):
                    config_temp1.append("nosudo");
                elif(l1 == 26):
                    config_temp1.append("run_in_background");
                elif(l1 == 27):
                    config_temp1.append("ttyon");
                elif(l1 == 28):
                    config_temp1.append("pacman_pakgage_install");
                else:
                    print("ERROR l1 nciht gefunden!");
                    exit(-1);
                config_temp1.append(config_temp);
                config.append(config_temp1);
                config_temp1 = [];
                config_temp = "";
                l1 = -1;
                l2 = -1;

        i = i +1;
    print(config);
    return config;
