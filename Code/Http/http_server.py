#!/bin/python3
#Copyright (C) 2023  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#this is a fork from https://github.com/kritzsie/steam-on-docker

version_jsongui = "0.1beta5"

from http.server import *
import subprocess
import os
import json
from Code.Json.json_file import *
from Code.Path.path_lib import *
from Code.Patching.patching_lib import *
from Code.Usb.usb_lib import *
from Code.Cd_Rom.cdrom_lib import *
from Code.Gui.json_edit_gui.json_edit_gui import *
from Code.Xinput.xinput_lib import *
from Code.Bluethooth.bluethooth_lib import *
from Code.Crypt.rsa_lib import *
from Code.Gui.manager_gui.manager_gui import *
from Code.Lxc.lxc import *
from Code.Podman.podman import *
#import cgi

def read_docker_ps(docker_system, podman_runs_root):
    try:
        cmd = [];
        if(docker_system == 1):
            #docker
            cmd = subprocess.check_output("docker ps ", shell=True).decode().split("\n");
        elif(docker_system == 2):
            if(podman_runs_root == 1):
                cmd = subprocess.check_output("sudo podman ps ", shell=True).decode().split("\n");
            else:
                cmd = subprocess.check_output("podman ps ", shell=True).decode().split("\n");
        return cmd;

    except subprocess.CalledProcessError:
        return "";
    except FileNotFoundError:
        return "";
    except IndexError:
        return "";


def listpath_only_vm_dirs(path, rpath, array, idarray, patharray, ctime):
        #File list
        j = array[0];
        sdir = array[1];
        try:
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
                    s1 = os.path.join(tmp, "build")
                    s2 = os.path.join(tmp, ".config")
                    s3 = os.path.join(tmp, "config_file_json")
                    if(os.path.isfile(s1) == True):
                        if(os.path.isfile(s2) == True):
                            sdir = sdir + "ID: " + str(j) + " | " + rpath + "/" + list[i] + "\n";
                            idarray.append(j);
                            s1 = rpath + "/" + list[i];
                            patharray.append(spath);
                            ctime.append("");
                            i =  i+1;
                            if( i== size):
                                break;
                            continue;
                        elif(os.path.isfile(s3) == True):
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
                    array = listpath_only_vm_dirs(spath, rpath2, array, idarray, patharray, ctime);
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
        except PermissionError:
            return [j, sdir, idarray, patharray, ctime]


def aufbreitung_vmfolder_array(array, dirpath):
    out = [];
    for tmp in array[3]:
        if(tmp == ""):
            continue;
        out.append(tmp.split(dirpath)[1][1::]);
    return out;

def read_all_vm_in_folder(dirpath):
    out = [0, ""]
    out = listpath_only_vm_dirs(dirpath, "", out, [], [], []);
    out = aufbreitung_vmfolder_array(out, dirpath);
    return out;


def listpath_only_vm_commands(path, rpath, array, idarray, patharray, ctime):
        #File list
        j = array[0];
        sdir = array[1];
        try:
            list = os.listdir(path)
            size = len(list);
            sout = "";
            i = 0;
            if(size == 0):
                return [j, sdir, idarray, patharray, ctime];
            while True:
                spath = path + "/" + list[i];
                if(os.path.islink(spath) == True):
                    spath = path + "/" + list[i];
                    if(os.access(spath, os.X_OK) == True):
                        sdir = sdir + "ID: " + str(j) + " | " + rpath + "/" + list[i] + "\n";
                        idarray.append(j);
                        s1 = rpath + "/" + list[i];
                        patharray.append(spath);
                        ctime.append("");
                        i =  i+1;
                        if( i== size):
                            break;
                        continue;
                    #sdir = sdir + "ID: " + str(j) + " | " + rpath + "/" + list[i] + "\n";
                    #idarray.append(j);
                    #s1 = rpath + "/" + list[i];
                    #patharray.append(s1);
                    #ctime.append("");
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
                    i =  i+1;
                    array = [j, sdir];
                    #array = listpath_only_vm_dirs(spath, rpath2, array, idarray, patharray, ctime);
                    #idarray = array[2];
                    #patharray = array[3];
                    #ctime = array[4];
                    #j = array[0];
                    #sdir = array[1];
                    if( i== size):
                        break;
                else:
                    spath = path + "/" + list[i];
                    if(os.access(spath, os.X_OK) == True):
                        sdir = sdir + "ID: " + str(j) + " | " + rpath + "/" + list[i] + "\n";
                        idarray.append(j);
                        s1 = rpath + "/" + list[i];
                        patharray.append(spath);
                        ctime.append("");
                        i =  i+1;
                        if( i== size):
                            break;
                        continue;
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
        except PermissionError:
            return [j, sdir, idarray, patharray, ctime]

def aufbreitung_vm_commands_array(array, dirpath):
    out = [];
    #out.append("command");
    #out.append("command_root");
    out.append("edit_config");
    out.append("firefox");
    out.append("login");
    out.append("login_root");
    out.append("openra-ra");

    for tmp in array[3]:
        if(tmp == ""):
            continue;
        s1 = tmp.split(dirpath)[1][1::];
        if(s1 == ".config"):
            continue;
        if(s1 == "edit_config"):
            continue;
        elif(s1.find("config") != -1):
            continue;
        elif(s1 == "config_file_json"):
            continue;
        elif(s1 == "hidraw_acs_overrides_patch.py"):
            continue;
        elif(s1 == "chmod_check.py"):
            continue;
        elif(s1 == "tmp.bash"):
            continue;
        elif(s1 == "user_patched.bash"):
            continue;
        elif(s1 == "user_patched2.bash"):
            continue;
        elif(s1 == "install.bash"):
            continue;
        elif(s1 == "pipe.tmp"):
            continue;
        elif(s1 == "pulse-client.conf"):
            continue;
        elif(s1 == "Code"):
            continue;
        elif(s1 == "build"):
            continue;
        elif(s1 == "Manager"):
            continue;
        elif(s1 == "hostname"):
            continue;
        elif(s1 == "locale.gen"):
            continue;
        elif(s1 == "hostname"):
            continue;
        elif(s1 == "machine-id"):
            continue;
        elif(s1.find(".bash") != -1):
            out.append(s1);
        elif(s1.find(".sh") != -1):
            out.append(s1);
        elif(s1.find(".py") != -1):
            out.append(s1);
        else:
            continue;
    return out;

def read_all_vm_in_command(dirpath):
    out = [0, ""]
    out = listpath_only_vm_commands(dirpath, "", out, [], [], []);
    out = aufbreitung_vm_commands_array(out, dirpath);
    return out;


class docker_http_server():
    def start_server(self):
        class requestHeader(BaseHTTPRequestHandler):
            def brechne_neue_lxc_coantiner_name(self, last, out):
                if(last == ""):
                    return -1;
                for i in range(len(out)):
                    tmp = out[i];
                    if(tmp == last):
                        return i;
                for i in range(len(out)):
                    tmp = out[i];
                    if(tmp.find(last) != -1):
                        return i;
                return 0;

            def do_GET(self):
                self.vms_fodler = "/VM/docker"
                if(self.path.find("/list_docker") != -1):
                    self.send_response(200);
                    self.send_header("content-type", "text/html");
                    self.end_headers();
                    a_docker_ps = read_docker_ps(1, 1)
                    sout = "";
                    sout = sout + "<!DOCTYPE html>\n";
                    sout = sout + "<html>\n";
                    sout = sout + "<head>\n";
                    sout = sout + "<title>Runging docker conatiners</title>\n";
                    sout = sout + "</head>\n";
                    sout = sout + "<body>\n";
                    sout = sout + "<table border='8'>\n";
                    #sout = sout + "<tr>\n";
                    b1 = 0;
                    #sout = sout + "<th>Container Id</th>\n"
                    #sout = sout + "<th>Ports</th>\n"
                    #sout = sout + "</tr>\n";
                    for tmp in a_docker_ps[::1]:
                        tmp2 = tmp.split();
                        print(len(tmp2))
                        if(b1 == 0):
                            sout = sout + "<tr>\n";
                            for tmp3 in tmp2:
                                sout = sout + "<th>" + tmp3 + "</th>\n";
                            sout = sout + "</tr>\n";
                            b1 = 1;
                        else:
                            if(len(tmp2) >= 7):
                                sout = sout + "<tr>\n";
                                for tmp3 in tmp2:
                                    sout = sout + "<td>" + tmp3 + "</td>\n";
                                sout = sout + "</tr>\n";
                    sout = sout + "</table>\n";
                    sout = sout + "</body>\n";
                    sout = sout + "</html>\n";
                    #sout = sout + "hello " + self.path.split("?=")[1]
                    self.wfile.write(sout.encode());

                elif(self.path.find("/list_podman_root") != -1):
                    self.send_response(200);
                    self.send_header("content-type", "text/html");
                    self.end_headers();
                    a_docker_ps = read_docker_ps(2, 1)
                    sout = "";
                    sout = sout + "<!DOCTYPE html>\n";
                    sout = sout + "<html>\n";
                    sout = sout + "<head>\n";
                    sout = sout + "<title>Runging docker conatiners</title>\n";
                    sout = sout + "</head>\n";
                    sout = sout + "<body>\n";
                    sout = sout + "<table border='8'>\n";
                    #sout = sout + "<tr>\n";
                    b1 = 0;
                    #sout = sout + "<th>Container Id</th>\n"
                    #sout = sout + "<th>Ports</th>\n"
                    #sout = sout + "</tr>\n";
                    for tmp in a_docker_ps[::1]:
                        tmp2 = tmp.split();
                        print(len(tmp2))
                        if(b1 == 0):
                            sout = sout + "<tr>\n";
                            for tmp3 in tmp2:
                                sout = sout + "<th>" + tmp3 + "</th>\n";
                            sout = sout + "</tr>\n";
                            b1 = 1;
                        else:
                            if(len(tmp2) >= 7):
                                sout = sout + "<tr>\n";
                                for tmp3 in tmp2:
                                    sout = sout + "<td>" + tmp3 + "</td>\n";
                                sout = sout + "</tr>\n";
                    sout = sout + "</table>\n";
                    sout = sout + "</body>\n";
                    sout = sout + "</html>\n";
                    #sout = sout + "hello " + self.path.split("?=")[1]
                    self.wfile.write(sout.encode());

                elif(self.path.find("/list_podman_user") != -1):
                    self.send_response(200);
                    self.send_header("content-type", "text/html");
                    self.end_headers();
                    a_docker_ps = read_docker_ps(2, 0)
                    sout = "";
                    sout = sout + "<!DOCTYPE html>\n";
                    sout = sout + "<html>\n";
                    sout = sout + "<head>\n";
                    sout = sout + "<title>Runging docker conatiners</title>\n";
                    sout = sout + "</head>\n";
                    sout = sout + "<body>\n";
                    sout = sout + "<table border='8'>\n";
                    #sout = sout + "<tr>\n";
                    b1 = 0;
                    #sout = sout + "<th>Container Id</th>\n"
                    #sout = sout + "<th>Ports</th>\n"
                    #sout = sout + "</tr>\n";
                    for tmp in a_docker_ps[::1]:
                        tmp2 = tmp.split();
                        print(len(tmp2))
                        if(b1 == 0):
                            sout = sout + "<tr>\n";
                            for tmp3 in tmp2:
                                sout = sout + "<th>" + tmp3 + "</th>\n";
                            sout = sout + "</tr>\n";
                            b1 = 1;
                        else:
                            if(len(tmp2) >= 7):
                                sout = sout + "<tr>\n";
                                for tmp3 in tmp2:
                                    sout = sout + "<td>" + tmp3 + "</td>\n";
                                sout = sout + "</tr>\n";
                    sout = sout + "</table>\n";
                    sout = sout + "</body>\n";
                    sout = sout + "</html>\n";
                    #sout = sout + "hello " + self.path.split("?=")[1]
                    self.wfile.write(sout.encode());

                elif(self.path.find("/list_all_contaienr_vms") != -1):
                    self.send_response(200);
                    self.send_header("content-type", "text/html");
                    self.end_headers();
                    a_vms = read_all_vm_in_folder(self.vms_fodler)
                    sout = "";
                    sout = sout + "<!DOCTYPE html>\n";
                    sout = sout + "<html>\n";
                    sout = sout + "<head>\n";
                    sout = sout + "<title>List of Contaienr VMs</title>\n";
                    sout = sout + "</head>\n";
                    sout = sout + "<body>\n";
                    sout = sout + "<table border='8'>\n";
                    #sout = sout + "<tr>\n";
                    b1 = 0;
                    #sout = sout + "<th>Container Id</th>\n"
                    #sout = sout + "<th>Ports</th>\n"
                    #sout = sout + "</tr>\n";
                    headers = ["VMs", "start"];
                    sout = sout + "<tr>\n";

                    for tmp in headers:
                        sout = sout + "<th>" + tmp + "</th>\n";

                    sout = sout + "</tr>\n";
                    for tmp in a_vms:
                        sout = sout + "<tr>\n";
                        sout = sout + "<td>" + tmp + "</td>\n";
                        sout = sout + "<td>" + '<button onclick="window.location.href=\'/start_vm?=' + tmp + '\';">Start VM</button>' + "</td>\n";
                        sout = sout + "</tr>\n";
                    sout = sout + "</table>\n";
                    sout = sout + "</body>\n";
                    sout = sout + "</html>\n";
                    #sout = sout + "hello " + self.path.split("?=")[1]
                    self.wfile.write(sout.encode());

                elif(self.path.find("/start_vm") != -1):
                    self.send_response(200);
                    self.send_header("content-type", "text/html");
                    self.end_headers();

                    if(self.path.find("?=") != -1):
                        if(len(self.path.split("?=")) >= 3):
                            svm_name = self.path.split("?=")[1].split("?")[0];
                            svm_command = self.path.split("?=")[2];
                            scmd = "cd \"" + self.vms_fodler + "/" +  svm_name + "\"\n"
                            scmd = scmd + svm_command + "\n";
                            b1 = 0;
                            if(svm_command.find("|") != -1):
                                b1 = 1;
                            if(svm_command.find("&&") != -1):
                                b1 = 1;
                            if(svm_command.find("bash ") != -1):
                                tmp1 = svm_command.split("bash ")[1];
                                if(os.path.isfile(self.vms_fodler + "/" +  svm_name + "/" + tmp1) == False):
                                    b1 = 1;
                                print(tmp1);
                            if(svm_command.find("./") != -1):
                                tmp1 = svm_command.split("./")[1];
                                if(os.path.isfile(self.vms_fodler + "/" +  svm_name + "/" + tmp1) == False):
                                    b1 = 1;
                            if(b1 == 1):
                                sout = sout + "error..\n";
                                self.wfile.write(sout.encode());
                            else:
                                os.system(scmd)
                                print(scmd);
                                sout = '<META http-equiv="refresh" content="7;URL=/start_vm?=' + svm_name +'">\n'
                                sout = sout + "starting..\n";
                                self.wfile.write(sout.encode());
                        else:
                            svm_name = self.path.split("?=")[1];
                            a_vms_command = read_all_vm_in_command(self.vms_fodler + "/" + svm_name)
                            sout = "";
                            sout = sout + "<!DOCTYPE html>\n";
                            sout = sout + "<html>\n";
                            sout = sout + "<head>\n";
                            sout = sout + "<title>" + svm_name + " Commands</title>\n";
                            sout = sout + "</head>\n";
                            sout = sout + "<body>\n";
                            sout = sout + "<table border='8'>\n";
                            #sout = sout + "<tr>\n";
                            b1 = 0;
                            #sout = sout + "<th>Container Id</th>\n"
                            #sout = sout + "<th>Ports</th>\n"
                            #sout = sout + "</tr>\n";
                            headers = ["Commands", "start"];
                            sout = sout + "<tr>\n";

                            for tmp in headers:
                                sout = sout + "<th>" + tmp + "</th>\n";

                            sout = sout + "</tr>\n";
                            for tmp in a_vms_command:
                                sout = sout + "<tr>\n";
                                sout = sout + "<td>" + tmp + "</td>\n";
                                sout = sout + "<td>" + '<button onclick="window.location.href=\'/start_vm?=' + svm_name + "?=./" + tmp + '\';">Start VM</button>' + "</td>\n";
                                sout = sout + "</tr>\n";
                            sout = sout + "</table>\n";
                            sout = sout + "</body>\n";
                            sout = sout + "</html>\n";
                            #sout = sout + "hello " + self.path.split("?=")[1]
                            #print(sout)
                            self.wfile.write(sout.encode());

                elif(self.path.find("/edit_config_from_vm") != -1):
                    if(self.path.find("?=") == -1):
                        self.send_response(200);
                        self.send_header("content-type", "text/html");
                        self.end_headers();

                        sout = "";
                        sout = sout + "Eroor"
                        self.wfile.write(sout.encode());
                        return;

                    svm_name = self.path.split("?=")[1];
                    svm_name = self.vms_fodler + "/" + svm_name;
                    if(os.path.isdir(svm_name) == False):
                        self.send_response(200);
                        self.send_header("content-type", "text/html");
                        self.end_headers();

                        sout = "";
                        sout = sout + "Eroor"
                        self.wfile.write(sout.encode());
                        return;
                    os.chdir(svm_name);
                    config = loading_json_file("config_file_json");

                    pacman_pkgage_install = "";
                    DEBUG_MODE = "";

                    docker_input = "";
                    maxmemory = -1;
                    maxcpus = -1;
                    network_host = "0";
                    portforwding = "";
                    dbus_rw = 0;
                    pacman_cache = "";
                    dns = "";
                    ipv4 = "";
                    wireguard_fix = 0;
                    run_in_background = 0;
                    ttyon = 0;
                    pacman_pakgage_install = pacman_pkgage_install;
                    bluethoot_passthrough = 0;
                    hidraw_acs_overrides_patch = 0;
                    ipv6_privacy = 0;
                    faketime = "";
                    wine_32bit_speed_hak = 0;
                    read_only = "";
                    read_only_password = "";
                    json_config_Verison = "";
                    amd_gpu_raytrasing_allgpus = 0;
                    amd_gpu_raytrasing_rdan2_only = 0;
                    string_bash_add = "";
                    string_bash_add_root = "";
                    wine_fsr = -1;
                    manager_vm_fodler = "";
                    debug = DEBUG_MODE;
                    optional_array = "";
                    smart_acces_meomory = 0;
                    vulkan_index = "";
                    vulkan_device_name = "";
                    steam_proton_run_without_steam = 0;
                    mango_hud = 0;
                    vkbasalt = 0;
                    freesync = 0;
                    vsync = 1;
                    docker_in_docker = 1;

                    #new
                    docker_system = 1;#1 docker 0 lxc
                    lxc_readonly = 1;#1 root readonly
                    lxc_network_mac = "0";
                    lxc_tmp_auto_create_id = -1;
                    lxc_network_bridge_link = "";
                    lxc_start_vm_lxc_device_coammds = "";
                    lxc_string_add_config = "";
                    lxc_mount_switch = 0;
                    docker_system_bak = docker_system;
                    lxc_readonly_bak = lxc_readonly;
                    docker_disable_ipv6 = 0;
                    #lxc staticip wird benotigt und cd dns server angaber

                    nvidia_dlss = 0;
                    nvidia_dlss_non_nvida_gpu = 0;
                    wineesync_and_winefsync = 0;
                    pulseaudio_stotterfix = 0;
                    amdgpu_nohyperz = 0;
                    string_radv_pertest = [];
                    amdgpu_pswave32 = 0;
                    amdgpu_nv_ms = 0;
                    amdgpu_vrs = "";
                    pluseaudio_sdl_fix = 0;
                    docker_auto_sav_folder = "";#/NAS/Daten/Backup/Docker/Backup/auto_sav
                    dhcpv6 = 0;
                    docker_hardining = 1;
                    amdgpu_mesh_shader_support = 0;
                    podman_runs_root = 1;
                    podman_set_route_gateway_ip = "";
                    podman_security_appamore_disable = 1;
                    ipv6 = ""
                    amdgpu_gpl_pipline = 0;
                    reset_config = 1;
                    ubisoft_connect_mut_fix = 0;
                    vk_khr_present_wait=0;
                    docker_user_password = ""
                    gamescope_bypass = 0;
                    block_framepuffer = 1;
                    ryujinx_emu_crash_fix = 0;

                    i = 0;
                    while True:
                        if(i >= len(config)):
                            break;
                        tmp = config[i];
                        if(tmp[0] == "docker_user"):
                            docker_user = tmp[1];
                        elif(tmp[0] == "gpu_render"):
                            gpu_render = tmp[1];
                        elif(tmp[0] == "disk_device_name"):
                            disk_device_name = tmp[1];
                        elif(tmp[0] == "zugriff_auf_media"):
                            zugriff_auf_media = int(tmp[1]);
                        elif(tmp[0] == "sav_home_docker_folder"):
                            sav_home_docker_folder = int(tmp[1]);
                        elif(tmp[0] == "share_folder_daten"):
                            share_folder_daten = int(tmp[1]);
                        elif(tmp[0] == "share_folder1_aktiv"):
                            share_folder1_aktiv = int(tmp[1]);
                        elif(tmp[0] == "share_folder1"):
                            share_folder1 = tmp[1];
                        elif(tmp[0] == "network_disable"):
                            network_disable = int(tmp[1]);
                        elif(tmp[0] == "steam_controller_bool"):
                            steam_controller_bool = int(tmp[1]);
                        elif(tmp[0] == "usb_sharing"):
                            usb_sharing = int(tmp[1]);
                        elif(tmp[0] == "usb_name"):
                            usb_name = tmp[1];
                        elif(tmp[0] == "usb_hidraw_name"):
                            usb_hidraw_name = tmp[1];
                        elif(tmp[0] == "docker_build"):
                            docker_build = tmp[1];
                        elif(tmp[0] == "docker_input"):
                            docker_input = tmp[1];
                        elif(tmp[0] == "maxmemory"):
                            maxmemory = int(tmp[1]);
                        elif(tmp[0] == "maxcpus"):
                            maxcpus = int(tmp[1]);
                        elif(tmp[0] == "network_host"):
                            network_host = tmp[1];
                        elif(tmp[0] == "portforwding"):
                            portforwding = tmp[1];
                        elif(tmp[0] == "dbus_rw"):
                            dbus_rw = int(tmp[1]);
                        elif(tmp[0] == "pacman_cache"):
                            pacman_cache = tmp[1];
                        elif(tmp[0] == "dns"):
                            dns = tmp[1];
                        elif(tmp[0] == "ipv4"):
                            ipv4 = tmp[1];
                        elif(tmp[0] == "wireguard_fix"):
                            wireguard_fix = int(tmp[1]);
                        elif(tmp[0] == "nosudo"):
                            nosudo = int(tmp[1]);
                        elif(tmp[0] == "run_in_background"):
                            run_in_background = int(tmp[1]);
                        elif(tmp[0] == "ttyon"):
                            ttyon = int(tmp[1]);
                        elif(tmp[0] == "pacman_pakgage_install"):
                            pacman_pakgage_install = tmp[1];
                        elif(tmp[0] == "bluethoot_passthrough"):
                            bluethoot_passthrough = int(tmp[1]);
                        elif(tmp[0] == "hidraw_acs_overrides_patch"):
                            hidraw_acs_overrides_patch = int(tmp[1]);
                        elif(tmp[0] == "ipv6_privacy"):
                            ipv6_privacy = int(tmp[1]);
                        elif(tmp[0] == "faketime"):
                            faketime = tmp[1];
                            if(faketime != "" and debug == 1):
                                print("faketime aktiv!");
                                print("faketime: " + faketime)
                        elif(tmp[0] == "wine_32bit_speed_hak"):
                            wine_32bit_speed_hak = int(tmp[1]);
                            if(debug == 1):
                                print("wine_32bit_speed_hak aktiv!");
                        elif(tmp[0] == "read_only"):
                            read_only = tmp[1];
                            if(debug == 1):
                                print("bearbeitung_Schutz aktiv!")
                        elif(tmp[0] == "read_only_password"):
                            read_only_password = tmp[1];
                            if(debug == 1):
                                print("bearbeitung_Schutz mit Pasword aktiv!")
                        elif(tmp[0] == "amd_gpu_raytrasing_allgpus"):
                            amd_gpu_raytrasing_allgpus = int(tmp[1]);
                        elif(tmp[0] == "amd_gpu_raytrasing_rdan2_only"):
                            amd_gpu_raytrasing_rdan2_only = int(tmp[1]);
                        elif(tmp[0] == "wine_fsr"):
                            wine_fsr = int(tmp[1]);
                        elif(tmp[0] == "manager_vm_fodler"):
                            manager_vm_fodler = tmp[1];
                        elif(tmp[0] == "optional_array"):
                            optional_array = tmp[1];
                            if(debug == 1):
                                print("optional_array: ", optional_array);
                        elif(tmp[0] == "smart_acces_meomory"):
                            smart_acces_meomory = int(tmp[1]);
                        elif(tmp[0] == "vulkan_device_name"):
                            vulkan_device_name = tmp[1];
                        elif(tmp[0] == "steam_proton_run_without_steam"):
                            steam_proton_run_without_steam = int(tmp[1]);
                        elif(tmp[0] == "mango_hud"):
                            mango_hud = int(tmp[1]);
                        elif(tmp[0] == "vkbasalt"):
                            vkbasalt = int(tmp[1]);
                        elif(tmp[0] == "freesync"):
                            freesync = int(tmp[1]);
                        elif(tmp[0] == "vsync"):
                            vsync = int(tmp[1]);
                        elif(tmp[0] == "docker_system"):
                            docker_system = int(tmp[1]);
                        elif(tmp[0] == "lxc_readonly"):
                            lxc_readonly = int(tmp[1]);
                        elif(tmp[0] == "lxc_network_mac"):
                            lxc_network_mac = tmp[1];
                        elif(tmp[0] == "lxc_network_bridge_link"):
                            lxc_network_bridge_link = tmp[1];
                        elif(tmp[0] == "docker_disable_ipv6"):
                            docker_disable_ipv6 = int(tmp[1]);
                        elif(tmp[0] == "nvidia_dlss"):
                            nvidia_dlss = int(tmp[1]);
                        elif(tmp[0] == "wineesync_and_winefsync"):
                            wineesync_and_winefsync = int(tmp[1]);
                        elif(tmp[0] == "nvidia_dlss_non_nvida_gpu"):
                            nvidia_dlss_non_nvida_gpu = int(tmp[1]);
                        elif(tmp[0] == "pulseaudio_stotterfix"):
                            pulseaudio_stotterfix = int(tmp[1]);
                        elif(tmp[0] == "amdgpu_nohyperz"):
                            amdgpu_nohyperz = int(tmp[1]);
                        elif(tmp[0] == "amdgpu_pswave32"):
                            amdgpu_pswave32 = int(tmp[1]);
                        elif(tmp[0] == "amdgpu_nv_ms"):
                            amdgpu_nv_ms = int(tmp[1]);
                        elif(tmp[0] == "amdgpu_vrs"):
                            amdgpu_vrs = tmp[1];
                        elif(tmp[0] == "pluseaudio_sdl_fix"):
                            pluseaudio_sdl_fix = int(tmp[1]);
                        elif(tmp[0] == "docker_auto_sav_fodler"):
                            docker_auto_sav_folder = tmp[1];
                        elif(tmp[0] == "docker_auto_sav_folder"):
                            docker_auto_sav_folder = tmp[1];
                        elif(tmp[0] == "dhcpv6"):
                            dhcpv6 = int(tmp[1]);
                        elif(tmp[0] == "amdgpu_mesh_shader_support"):
                            amdgpu_mesh_shader_support = int(tmp[1]);
                        elif(tmp[0] == "podman_runs_root"):
                            podman_runs_root = int(tmp[1])
                        elif(tmp[0] == "podman_set_route_gateway_ip"):
                            podman_set_route_gateway_ip = tmp[1];
                        elif(tmp[0] == "ipv6"):
                            ipv6 = tmp[1];
                        elif(tmp[0] == "amdgpu_gpl_pipline"):
                            amdgpu_gpl_pipline = int(tmp[1]);
                        elif(tmp[0] == "rest_config"):
                            reset_config = int(tmp[1]);
                        elif(tmp[0] == "ubisoft_connect_mut_fix"):
                            ubisoft_connect_mut_fix = int(tmp[1]);
                        elif(tmp[0] == "vk_khr_present_wait"):
                            vk_khr_present_wait = int(tmp[1]);
                        elif(tmp[0] == "docker_user_password"):
                            docker_user_password = tmp[1];
                        elif(tmp[0] == "gamescope_bypass"):
                            gamescope_bypass = int(tmp[1]);
                        elif(tmp[0] == "ryujinx_emu_crash_fix"):
                            ryujinx_emu_crash_fix = int(tmp[1]);
                        elif(tmp[0] == "sav_Version"):
                            json_config_Verison = tmp[1];
                        else:
                            print("ERROR config file corrupt");
                            print(tmp);
                            exit(1);
                        i = i +1;


                    self.send_response(200);
                    self.send_header("content-type", "text/html");
                    self.end_headers();
                    sout = "<!DOCTYPE html>\n";

                    sout = sout + "<html>\n";
                    sout = sout + "<body>\n";
                    sout = sout + "<title>HTML Tutorial</title>\n";
                    sout = sout + "<h1>edit config</h1>\n";
                    #sout = sout + '<p id="myP">Click "sav" to change my font size.</p>\n';
                    sout = sout + '<button onclick="sav_config()">Save</button>\n';
                    sout = sout + '<label for="docker system:</label>\n';
                    sout = sout + '<form action="/action_page.php">\n';
                    #sout = sout + "<form>\n"

                    #docker_system
                    sout = sout + '<h1>--------------------------------------------------------Virtualsirer--------------------------------------------------------</h1>\n';
                    sout = sout + '<select id="docker_system_box" name="docker system">\n'
                    if(docker_system == 0):
                        sout = sout + '<option value="0" selected>Lxc</option>\n'
                        sout = sout + '<option value="1">Docker</option>\n'
                        sout = sout + '<option value="2">Podman (experimental)</option>\n'
                        sout = sout + '<option value="3">Vfiodock</option>\n'
                    elif(docker_system == 1):
                        sout = sout + '<option value="0">Lxc</option>\n'
                        sout = sout + '<option value="1" selected>Docker</option>\n'
                        sout = sout + '<option value="2">Podman (experimental)</option>\n'
                        sout = sout + '<option value="3">Vfiodock</option>\n'
                    elif(docker_system == 2):
                        sout = sout + '<option value="0">Lxc</option>\n'
                        sout = sout + '<option value="1">Docker</option>\n'
                        sout = sout + '<option value="2" selected>Podman (experimental)</option>\n'
                        sout = sout + '<option value="3">Vfiodock</option>\n'
                    elif(docker_system == 3):
                        sout = sout + '<option value="0">Lxc</option>\n'
                        sout = sout + '<option value="1">Docker</option>\n'
                        sout = sout + '<option value="2">Podman (experimental)</option>\n'
                        sout = sout + '<option value="3" selected>Vfiodock</option>\n'
                    else:
                        sout = sout + '<option value="0">Lxc</option>\n'
                        sout = sout + '<option value="1">Docker</option>\n'
                        sout = sout + '<option value="2">Podman (experimental)</option>\n'
                        sout = sout + '<option value="3">Vfiodock</option>\n'

                    sout = sout + '</select>\n'
                    #lxc_readonly
                    sout = sout + '<input type="checkbox" id="lxc_read_only_mode_checkbox" name="lxc_read_only_mode_checkbox" value="" checked=True>\n'
                    sout = sout + '<label for="lxc_read_only_mode_checkbox"> lxc readonly mode für / nur für lxc</label><br>\n'
                    sout = sout + "</form>\n"
                    #podman_runs_root
                    sout = sout + '<input type="checkbox" id="podman_runs_root_checkbox" name="podman_runs_root_checkbox" value="" checked=True>\n'
                    sout = sout + '<label for="podman_runs_root_checkbox"> podman als root ausführen: off als user on als root per sudo (cdrom fix)</label><br>\n'
                    sout = sout + "</form>\n"
                    #docker_build
                    sout = sout + '<select id="docker_build_combobox" name=""docker oder lxc oder podman oder vfiodock contaienr name das docker image wo gestatet wird: ">\n'
                    docker_build_combobox_array = [];

                    tmp1 = 0;
                    if(docker_system == 2):
                        tmp1 = podman_runs_root;
                    vm_imgaes = read_docker_imags(docker_system, tmp1);
                    vm_images_index = self.brechne_neue_lxc_coantiner_name(docker_build, vm_imgaes);
                    i = 0;
                    for tmp in vm_imgaes:
                        if (i == vm_images_index):
                            sout = sout + '<option value="' + tmp + '"selected>' + tmp + '</option>\n'
                        else:
                            sout = sout + '<option value="' + tmp + '">' + tmp + '</option>\n'
                        i = i +1;
                    sout = sout + '</select>\n'

                    sout = sout + "<h1>--------------------------------------------------------CPU & RAM--------------------------------------------------------</h1>\n";
                    #maxmemory
                    sout = sout + '<label for="maxmemory_spinbox_label"> Mazialer zugelassener RAN verbauch in Megabyte (-1 == keine Beschrnäkung: </label>\n'
                    sout = sout + '<input type=number min="-1" max="2147483647" value="' + str(maxmemory) + '" id="maxmemory_spinbox"><br>\n'
                    #maxcpus
                    sout = sout + '<label for="maxcpus_spinbox_label"> Wie viele CPUS darf der docker container nutzen in threads (-1 == keine Beschrnäkung): </label>>\n'
                    sout = sout + '<input type=number min="-1" max="2147483647" value="' + str(maxcpus) + '" id="maxcpus_spinbox"><br>\n'
                    #gpu_render
                    #vulkan_device
                    sout = sout + "<h1>--------------------------------------------------------GPUS--------------------------------------------------------</h1>\n";
                    sout = sout + '<label for="gpu_render_spinbox_label"> gpu_render: (nur für muti gpu user um bei opengl eine gpu zu wählen! bei 1ner gpu Bitte 0 lassen )</label>\n'
                    sout = sout + '<input type="text" id="gpu_rende_text" name="gpu_render" value="' + gpu_render + '">\n'
                    sout = sout + '<select id="gpu_render_box" name="docker system">\n'
                    gpu_render_array = read_all_dri_prime_device("");
                    #import pdb; pdb.set_trace()
                    b1 = 0;
                    for tmp in gpu_render_array:
                        if(b1 == 0):
                            b1 = 1;
                            sout = sout + '<option value="' +  tmp + '" selected>' + tmp + '</option>\n'
                        else:
                            sout = sout + '<option value="' +  tmp + '" >' + tmp + '</option>\n'
                    sout = sout + '</select>\n'
                    sout = sout + '<button onclick="set_combox_gpu_render()">set</button><br>\n';
                    sout = sout + '<label for="vulkan_device_name_spinbox_label"> vulkan device name bitte automatisch setzen lassen oder leer: </label>\n'
                    sout = sout + '<input type="text" id="vulkan_device_name_box" name="vulkan_device_name" value="' + vulkan_device_name + '"></input>\n'
                    sout = sout + '<button onclick="set_combox_gpu_render_name_vulkan_only()">set</button><br>\n';
                    #disk_device_name
                    #sout = sout + "<h1></h1>\n";
                    sout = sout + "<h1>--------------------------------------------------------CD/DVD & USB--------------------------------------------------------</h1>\n";
                    sout = sout + '<label for="disk_device_name_spinbox_label"> Standard Eisntellugn \"cd/dvd\" alle cd rom laufwerke werden in den docker container übernomen: > </label>\n'
                    sout = sout + '<input type="text" id="disk_device_name" name="disk_device_name" value="' + disk_device_name + '"></input><br>\n'
                    #usb_sharing
                    sout = sout + '<label for="usb_sharing_label">usb_sharing: </label>\n'
                    sout = sout + '<input type="checkbox" id="usb_sharing" name="usb_sharing" value="' + str(usb_sharing) + '"> </input>\n'
                    #steam_controller_bool
                    sout = sout + '<label for="steam_controller_bool_label"> steam_controller_bool:  </label>\n'
                    sout = sout + '<input type="checkbox" id="steam_controller_bool" name="steam_controller_bool" value="' + str(steam_controller_bool) + '"> </input>\n'
                    #usb_name
                    sout = sout + '<label for=usb gerät per usb name> in docker hinzufügen (mehere device getrennt mit ^): > </label>\n'
                    sout = sout + '<input type="text" id="usb_name" name="usb_name" value="' + usb_name + '"> </input>\n'
                    sout = sout + '<select id="usb_name_box" name="usb_name_box">\n'
                    usb_names = read_lsusb();
                    i = 0;
                    for tmp in usb_names:
                        if (i == 0):
                            sout = sout + '<option value="' + tmp + '"selected>' + tmp + '</option>\n'
                        else:
                            sout = sout + '<option value="' + tmp + '">' + tmp + '</option>\n'
                        i = i +1;
                    sout = sout + '</select>\n'
                    sout = sout + '<button onclick="add_combox_usb_share()">add</button><br>\n';


                    sout = sout + "<script>\n";

                    sout = sout + "function bool_to_int(a) {\n";
                    sout = sout + "if( a == true){\n";
                    sout = sout + 'return "1";\n';
                    sout = sout + "}\n"
                    sout = sout + "else{\n";
                    sout = sout + 'return "0";\n';
                    sout = sout + "}\n"
                    sout = sout + "}\n"

                    sout = sout + "function sav_config() {\n";
                    sout = sout + 'const docker_system = document.getElementById("docker_system_box");\n';
                    sout = sout + 'const lxc_readonly = document.getElementById("lxc_read_only_mode_checkbox");\n';
                    sout = sout + 'const podman_runs_root = document.getElementById("podman_runs_root_checkbox");\n';
                    sout = sout + 'const docker_build = document.getElementById("docker_system_box");\n';
                    sout = sout + 'const maxmemory = document.getElementById("maxmemory_spinbox");\n';
                    sout = sout + 'const maxcpus = document.getElementById("maxcpus_spinbox");\n';
                    sout = sout + 'const gpu_render = document.getElementById("gpu_rende_text");\n';
                    sout = sout + 'const vulkan_device_name = document.getElementById("vulkan_device_name_box");\n';
                    sout = sout + 'const disk_device_name = document.getElementById("disk_device_name");\n';
                    sout = sout + 'const usb_sharing = document.getElementById("usb_sharing");\n';
                    sout = sout + 'const steam_controller_bool = document.getElementById("steam_controller_bool");\n';
                    sout = sout + 'const usb_name = document.getElementById("usb_name");\n';
                    #sout = sout + 'url = "/sav_config?docker_system=" + docker_system.value + "?lxc_readonly=" + bool_to_int(lxc_readonly.checked) + "?podman_runs_root=" + bool_to_int(podman_runs_root.checked);\n';
                    #sout = sout + 'window.location.href=url;\n';
                    sout = sout + 'url = "/sav_config";\n';
                    sout = sout + 'json_data = {\n'
                    sout = sout + '"docker_system" : docker_system.value,\n'
                    sout = sout + '"lxc_readonly" : bool_to_int(lxc_readonly.checked),\n'
                    sout = sout + '"podman_runs_root" : bool_to_int(podman_runs_root.checked),\n'
                    sout = sout + '"docker_build" : docker_build.value,\n'
                    sout = sout + '"maxmemory" : maxmemory.value,\n'
                    sout = sout + '"maxcpus" : maxcpus.value,\n'
                    sout = sout + '"gpu_render" : gpu_render.value,\n'
                    sout = sout + '"vulkan_device_name" : vulkan_device_name.value,\n'
                    sout = sout + '"disk_device_name" : disk_device_name.value,\n'
                    sout = sout + '"usb_sharing" : usb_sharing.value,\n'
                    sout = sout + '"steam_controller_bool" : steam_controller_bool.value,\n'
                    sout = sout + '"usb_name" : usb_name.value,\n'
                    sout = sout + "}\n"
                    sout = sout + "json_data_out = JSON.stringify(json_data);\n";
                    sout = sout + "fetch(url, {\n"
                    sout = sout + 'method: "POST",\n'
                    sout = sout + 'body: json_data_out,\n'
                    sout = sout + 'headers: {\n'
                    sout = sout + '"Content-type": "application/json, charset=UTF-8"\n'
                    sout = sout + "}\n"
                    sout = sout + "})\n"
                    #sout = sout + "}\n"

                    #sout = sout + 'docker_system.value = "podman"\n';
                    #sout = sout + '<META http-equiv="refresh" content="7;URL=/sav_config?docker_system=' + docker_system.value +'">\n'
                    #dann url /sav_config$docker_system=podman per button
                    sout = sout + "}\n"
                    sout = sout + "function set_combox_gpu_render() {\n";
                    sout = sout + 'const gpu_render_box = document.getElementById("gpu_render_box");\n';
                    sout = sout + 'const gpu_render = document.getElementById("gpu_rende_text");\n';
                    sout = sout + 'const docker_system = document.getElementById("docker_system_box");\n';
                    sout = sout + 'if( docker_system.value == "0"){\n'
                    sout = sout + 'set_combox_gpu_render_name_vulkan_only();\n'

                    sout = sout + "}\n"
                    sout = sout + 'gpu_render.value = gpu_render_box.value.split(" (")[0];\n'
                    sout = sout + "}\n"
                    sout = sout + "function set_combox_gpu_render_name_vulkan_only() {\n";
                    sout = sout + 'const gpu_render_box = document.getElementById("gpu_render_box");\n';
                    sout = sout + 'const gpu_render = document.getElementById("gpu_rende_text");\n';
                    sout = sout + 'const docker_system = document.getElementById("docker_system_box");\n';
                    sout = sout + 'const vulkan_device_name = document.getElementById("vulkan_device_name_box");\n';
                    sout = sout + 'if( docker_system.value == "0"){\n'
                    #lxc #work
                    sout = sout + 'gpu_render.value = gpu_render_box.value.split(" (")[0];\n'
                    sout = sout + 's1 = gpu_render_box.value.split(" (")[0].split(" Series")[0].toLowerCase();\n'
                    sout = sout + 's1 = s1.split(" ");\n'
                    sout = sout + 's1 = s1[s1.length - 1];\n';
                    sout = sout + 'vulkan_device_name.value = s1;\n'
                    sout = sout + 'gpu_render.value = "";\n'
                    sout = sout + "}\n"
                    sout = sout + 'if( docker_system.value == "1"){\n'
                    #docker
                    sout = sout + 'gpu_render.value = gpu_render_box.value.split(" (")[0];\n'
                    sout = sout + 's1 = gpu_render_box.value.split("(")[0].split();\n'
                    sout = sout + 's1 = s1[s1.length - 1];\n';
                    sout = sout + 'vulkan_device_name.value = s1;\n'
                    sout = sout + 'gpu_render.value = gpu_render_box.value.split("(")[1].split()[0].split(",")[0];\n'
                    sout = sout + "}\n"
                    sout = sout + 'if( docker_system.value == "2"){\n'
                    #podman
                    sout = sout + 'gpu_render.value = gpu_render_box.value.split(" (")[0];\n'
                    sout = sout + 's1 = gpu_render_box.value.split("(")[0].split();\n'
                    sout = sout + 's1 = s1[s1.length - 1];\n'
                    sout = sout + 'vulkan_device_name.value = s1;\n'
                    sout = sout + 'gpu_render.value = gpu_render_box.value.split("(")[1].split()[0].split(",")[0];\n'
                    sout = sout + "}\n"
                    sout = sout + 'if( docker_system.value == "3"){\n'
                    #vfiodock
                    sout = sout + 'gpu_render.value = gpu_render_box.value.split(" (")[0];\n'
                    sout = sout + 'vulkan_device_name.value = "opengl render use";\n'
                    sout = sout + 'gpu_render.value = gpu_render_box.value.split("(")[1].split()[0].split(",")[0];\n'
                    sout = sout + "}\n"
                    #end if
                    sout = sout + "}\n"

                    #add_combox_usb_share func
                    sout = sout + "function add_combox_usb_share() {\n";
                    sout = sout + 'const usb_name_box = document.getElementById("usb_name_box");\n';
                    sout = sout + 'const usb_name = document.getElementById("usb_name");\n';
                    sout = sout + 'if( usb_name.value.search("^") == 0){\n'
                    #1

                    sout = sout + 'if( usb_name_box.value == usb_name.value){\n'
                    sout = sout + 'usb_name.value = usb_name_box.value;\n'
                    sout = sout + "}\n"

                    sout = sout + 'if( usb_name.value == ""){\n'
                    sout = sout + 'usb_name.value = usb_name_box.value;\n'
                    sout = sout + "}\n"

                    sout = sout + 'else{\n'

                    #2
                    sout = sout + 'if( usb_name.value != usb_name_box.value){\n'
                    sout = sout + 'usb_name.value = usb_name.value + "^" + usb_name_box.value;\n'
                    sout = sout + "}\n"
                    #2

                    sout = sout + "}\n"

                    #1
                    sout = sout + "}\n"

                    sout = sout + 'else{\n'

                    sout = sout + 'a = usb_name.value.split("^");\n'

                    #2
                    sout = sout + 'b1 = 0\n'
                    sout = sout + 'for (let i = 0; i < length(a); i++) {\n'

                    sout = sout + 'tmp = a[i];\n'
                    #3
                    sout = sout + 'if( usb_name_box.value == tmp){\n'
                    sout = sout + 'b1 = 1;\n'
                    sout = sout + 'break;\n'
                    sout = sout + "}\n"
                    #3

                    #2
                    sout = sout + 'if( b1 == 0){\n'
                    sout = sout + 'usb_name.value = usb_name.value + "^" + usb_name_box.value;\n'
                    sout = sout + "}\n"
                    #2

                    sout = sout + "}\n"
                    #1

                    #sout = sout + 'usb_name.value = usb_name.value + "^" + usb_name_box.value;\n'
                    sout = sout + "}\n"

                    sout = sout + "}\n"
                    #

                    sout = sout + "</script>\n"
                    sout = sout + "</body>\n";
                    sout = sout + "</html>\n";
                    #https://www.w3schools.com/css/default.asp
                    #http://192.168.111.30:8080/edit_config_from_vm
                    #http://192.168.111.30:8080/edit_config_from_vm?=alcohol_120
                    #https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/send
                    self.wfile.write(sout.encode());
                    #import pdb; pdb.set_trace()

                else:
                    self.send_response(200);
                    self.send_header("content-type", "text/html");
                    self.end_headers();

                    sout = "";
                    sout = sout + "Error"
                    self.wfile.write(sout.encode());
            def do_POST(self):
                if(self.path.find("/sav_config") != -1):
                        ctype, pdict = cgi.parse_header(self.headers.get("Content-type"));
                        if(ctype == "application/json, charset=UTF-8"):
                            json_data_upload = self.rfile.read1(99999999999999999)
                            json_data = json.loads(json_data_upload)
                            docker_system = json_data["docker_system"];
                            lxc_readonly = json_data["lxc_readonly"];
                            podman_runs_root = json_data["podman_runs_root"];
                            docker_build = json_data["docker_build"];
                            maxmemory = json_data["maxmemory"];
                            maxcpus = json_data["maxcpus"];
                            gpu_render = json_data["gpu_render"];
                            vulkan_device_name = json_data["vulkan_device_name"];
                            disk_device_name = json_data["disk_device_name"];
                            print(disk_device_name)
                else:
                    return;
                return;



        port = 8080;
        server_address = ("0.0.0.0", port);
        self.httpd = HTTPServer(server_address, requestHeader)
        print("Server gestarted!")
        self.httpd.serve_forever();

def start_http_server():
    server = docker_http_server();
    server.start_server();
    return 0;
