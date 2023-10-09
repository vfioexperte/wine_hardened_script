#!/usr/bin/env python
#Copyright (C) 2022  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#this is a fork from https://github.com/kritzsie/steam-on-docker

version_jsongui = "0.8a"
#0.8a add neu option gamescope_render_auflosung
#0.7m4 degrade fuktion vulkan_device fix 0.2a
#0.7j ryujinx_emu_crash_fix 0.1a
#0.7i new pacman_pakgage_install check 0.1a
#0.7f gamescope_bypass add new option
#0.7d add new options docker_user_password
#0.7c add new options vk_khr_present_wait
#0.6i python qt6
#0.6h add new amdgpu_gpl_pipline
#v0.6d podman_set_route_gateway_ip
#0.6a podman support
#0.5d amdgpu_mesh_shader_support variable
#0.4f docker input label fix 0.1a
#0.4e docker system combobox fix 0.1a
#0.4d new desinge 0.2a
#0.4c lxc support 0.1a
#0.4b 2 network intefaces
#0.4a_hotfix_7 ICE default IO error handler doing an exit(), pid = 82334, errno = 32 fix 0.1a
#0.4a_hotfix_5 glxinfo run in archlinux docker coantiner
#0.4a_hotfix_4 add freesync, vsync
#0.4a_hotfix_2 dxvk samrt smart_acces_meomory 0.1a
#0.4a new look with qchckboxes 0.1a
#0.3j_hotfix_4 opengl or vulkan device select fix 0.1a
#0.3j optional_array and smart_acces_meomory add
# 0.3h wine_fsr
#0.3g hotfix 5 docker image auswahl 0.1a
#0.3g raytrasing option add
#0.3f_6 virgl hot fix 0.1a
#0.3f_5 DRI PRIME in docker coantiner fix 0.2a
#0.3f_3 json_edit_gui add a scrollbar

import platform
import os
import sys
import string
import subprocess
import time
import math
import json
jason_data = {};
from Code.Json.json_file import *
from Code.Lxc.lxc import *
from Code.Podman.podman import *
appname = "Seb Docker build json edit config"

DEBUG_MODE_jsongui = 0;
def set_DEBUG_MODE_jsongui(bool1):
    DEBUG_MODE_jsongui = bool1;

def cmd_start(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True).decode().split("\n")
        return out
    except subprocess.CalledProcessError:
        return []

def split_to_usbnames(array):
    sout1 = "";
    i = 0;
    for tmp in array:
        if(i >= len(array)-1):
            sout1 = sout1 + tmp;
        else:
            sout1 = sout1 + tmp + " ";
        i = i +1;
    return sout1;


def read_lsusb():
    out = cmd_start("lsusb");
    usb_names = []
    for tmp in out:
        s1 = tmp.split(" ");
        if(len(s1) >= 5):
            usb_names.append((split_to_usbnames(s1[6::])));
    return usb_names;

def check_device_isopen_hidraw(filepath):
    try:
        tmp = os.open(filepath, os.O_RDONLY);
        os.close(tmp);
        return 1;
    except PermissionError:
        return 1;
    except TypeError:
        return 1;
    except FileNotFoundError:
        return 0;
    return 1;


def read_hidraw():
    usb_hidraw_names = [];
    i = 0;
    dev = [];
    while True:
        if(i >= 100):
            break;
        if(check_device_isopen_hidraw("/dev/hidraw" + str(i)) == 0):
            i = i +1;
            continue;
        try:
            output = subprocess.check_output("/usr/bin/cat < /sys/class/hidraw/hidraw" + str(i) +  "/device/uevent | /usr/bin/grep \"HID_NAME=\"", shell=True).decode();
            s1 = output.split("\n");
            s2 = s1[0].split("HID_NAME=");
            usb_hidraw_names.append(s2[1]);
        except subprocess.CalledProcessError:
            pass;
        i = i +1;
    print(usb_hidraw_names)
    return usb_hidraw_names;


def read_glxinfo(dri_prime, basename):
    if(list_all_gpus() <= dri_prime):
        return "";
    if(basename == "system_only2"):
        return "";
    #cmd = cmd_start("DRI_PRIME=" + str(dri_prime) + " glxinfo | grep \"OpenGL renderer\"");
    #if(len(cmd) == 0):
    #    return "ERROR mesa-utils not installed!";
    #s1 = cmd[0].split("OpenGL renderer string: ");
    #return s1[1]
    #cmd_start("./command 'DRI_PRIME=" + str(dri_prime) + " glxinfo | grep \"OpenGL renderer\" > /tmp/pipe.tmp'");
    #cmd_start("./system_only DRI_PRIME=" + str(dri_prime) + " glxinfo | grep \"OpenGL renderer\" 2>/tmp/pipe.tmp");
    #cmd_start
    os.system("./system_only2 'DRI_PRIME=" + str(dri_prime) + " glxinfo | grep \"OpenGL renderer\" >/etc/tmp/pipe.tmp'");

    f1 = open("pipe.tmp", "r");
    f1.seek(0, 2);
    size = f1.tell();
    f1.seek(0, 0);
    s1 = f1.read(size);
    f1.close();
    #print(s1);
    cmd = s1.split("\n");
    #f1 = open("pipe.tmp", "r");
    #f1.seek(0, 2);
    #size = f1.tell();
    #f1.seek(0, 0);
    #cmd = f1.read(size).split("\n");
    #f1.close();
    if(len(cmd) == 0):
        return "ERROR mesa-utils not installed!";
    s1 = cmd[0].split("OpenGL renderer string: ");
    if(len(s1) >= 2):
        return s1[1];
    return "";

def list_all_gpus():
    i1 = -1;
    cmd = cmd_start("lspci -v | grep \"Kernel driver in use: amdgpu\"");
    i1 = i1 + len(cmd);
    cmd = cmd_start("lspci -v | grep \"Kernel driver in use: radeon\"");
    i1 = i1 + len(cmd);
    cmd = cmd_start("lspci -v | grep \"VGA compatible controller: Red Hat, Inc. Virtio GPU\"");
    i1 = i1 + len(cmd);
    return i1;

def read_all_dri_prime_device(basename):
    out = [];
    for i in range(16):
        s1 = read_glxinfo(i, basename);
        if(s1 != ""):
            out.append(s1);
        else:
            break;
    return out;

def read_docker_imags(docker_system, podman_runs_root = 0):
    if(docker_system == 0):
        #lxc
        out = [];
        s1 = cmd_start("sudo lxc-ls");
        return s1[0].split();
    if(docker_system == 1):
        #docker
        out = [];
        s1 = cmd_start("docker image ls");
        s1 = s1[1::];
        for tmp in s1:
            tmp2 = tmp.split();
            if(len(tmp2) > 6):
                out.append(tmp2[0]);
        return out;
    else:
        #podman
        out = [];
        s1  = []
        if(podman_runs_root == 1):
            s1 = cmd_start("sudo podman image ls");
        else:
            s1 = cmd_start("podman image ls");
        s1 = s1[1::];
        for tmp in s1:
            tmp2 = tmp.split();
            if(len(tmp2) > 6):
                out.append(tmp2[0]);
        return out;



def list_mesa_vulkan_device():
    devices = [];
    #MESA_VK_DEVICE_SELECT_FORCE_DEFAULT_DEVICE
    cmd_start("./system_only2 'MESA_VK_DEVICE_SELECT=\"list\" vkcube 2>/etc/tmp/pipe.tmp'");
    f1 = open("pipe.tmp", "r");
    f1.seek(0, 2);
    size = f1.tell();
    f1.seek(0, 0);
    s1 = f1.read(size);
    f1.close();
    s1 = s1.split("\n")
    #print(s1);
    b1 = 0;
    if(len(s1) < 1):
        return -1;
    for tmp in s1:
        print(tmp)
        s3 = tmp.split();
        if(tmp == ""):
            break;
        if(b1 == 0):
            if(len(s3) >= 2):
                if(s3[0] == "selectable"):
                    if(s3[1] == "devices:"):
                        b1 = 1;
                        #print("b1 = 1")
        elif(b1 == 1):
            device_name = tmp.split("\"")[1];
            device_name2 = tmp.split("\"")[1].split("(")[0];
            device_name3 = tmp.split("\"")[1].split("(")[1].split(")")[0];
            device_id = s3[2];
            devices.append([device_name.upper(), device_name2.upper(), device_name3.upper(), device_id]);
    #print(devices)
    if(len(devices) == 0):
        return 0;
    return devices;

def start_json_edit_gui(dirname, docker_user, gpu_render, disk_device_name, zugriff_auf_media, sav_home_docker_folder, share_folder_daten,
                    share_folder1_aktiv, share_folder1, network_disable, steam_controller_bool, usb_sharing, usb_name, usb_hidraw_name,
                    docker_build, docker_input, maxmemory, maxcpus, network_host, portforwding, dbus_rw, pacman_cache, dns, ipv4,
                    wireguard_fix, nosudo, run_in_background, ttyon, pacman_pakgage_install, bluethoot_passthrough, hidraw_acs_overrides_patch,
                    ipv6_privacy, faketime, wine_32bit_speed_hak, read_only, read_only_password, amd_gpu_raytrasing_allgpus, amd_gpu_raytrasing_rdan2_only
                    , wine_fsr, manager_vm_fodler, optional_array, smart_acces_meomory, vulkan_device_name, steam_proton_run_without_steam, mango_hud, vkbasalt,
                    freesync, vsync, docker_system, lxc_readonly, lxc_network_mac, lxc_network_bridge_link, sav_and_exit, docker_disable_ipv6,
                    nvidia_dlss, nvidia_dlss_non_nvida_gpu, wineesync_and_winefsync, pulseaudio_stotterfix, amdgpu_nohyperz, amdgpu_pswave32, amdgpu_nv_ms,
                    amdgpu_vrs, pluseaudio_sdl_fix, docker_auto_sav_fodler, dhcpv6, amdgpu_mesh_shader_support, podman_runs_root,
                    podman_set_route_gateway_ip, ipv6, amdgpu_gpl_pipline, rest_config, ubisoft_connect_mut_fix, vk_khr_present_wait,
                    docker_user_password, gamescope_bypass, ryujinx_emu_crash_fix, gamescope_render_auflosung):
    from PyQt6 import QtWidgets
    from PyQt6 import QtGui
    from PyQt6 import QtCore
    import time
    import datetime
    app = QtWidgets.QApplication(sys.argv);
    class seb_sync_clinet_gui(QtWidgets.QWidget):
        def __init__(self):
            QtWidgets.QWidget.__init__(self)

            self.statusbar = QtWidgets.QStatusBar()
            self.statusbar.showMessage("test")
            self.title = appname + " - " + version_jsongui
            self.setWindowTitle(self.title)
            self.h = 1080;
            self.w = 1920;
            #self.resize(self.w, self.h)
            self.layoutv0 = QtWidgets.QVBoxLayout(self)
            self.scrollArea = QtWidgets.QScrollArea()
            self.scrollArea.setWidgetResizable(True)
            self.scrollAreaWidgetContents = QtWidgets.QWidget(self.scrollArea)
            #self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, self.w, self.h))
            self.scrollArea.setWidget(self.scrollAreaWidgetContents)
            self.layoutv0.addWidget(self.scrollArea)

            #print(read_only_password)
            if(read_only_password != ""):
                text, ok =  QtWidgets.QInputDialog.getText(self, 'config file passwort Frage!', 'Zum bearbeiten Bitte das Password:');
                if ok and read_only_password == text:
                    pass;
                else:
                    msgBox = QtWidgets.QMessageBox();
                    msgBox.setIcon(QtWidgets.QMessageBox.Information);
                    msgBox.setText("Password Falsch");
                    msgBox.exec();
                    exit();

            self.layoutv1 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
            self.layoutv1.addLayout(self.layoutv1)

            self.layouth_tmp2 =  QtWidgets.QHBoxLayout();
            self.layouth_tmp2_label = QtWidgets.QLabel("--------------------------------------------------------Virtualsirer--------------------------------------------------------")
            self.layouth_tmp2.addWidget(self.layouth_tmp2_label);
            self.layoutv1.addLayout(self.layouth_tmp2);

            self.layouth_tmp1 = QtWidgets.QHBoxLayout();
            self.docker_system_label = QtWidgets.QLabel("docker_system for steam lxc wählen (lxc == 0, docker == 1, podman (experimental) == 2, vfiodock (experimental) == 3)")
            self.docker_system = QtWidgets.QSpinBox()
            self.docker_system.setValue(docker_system);
            self.docker_system.setMinimum(0);
            self.docker_system.setMaximum(3)
            self.docker_system.valueChanged.connect(self.docker_system_changed)
            self.lxc_readonly = QtWidgets.QCheckBox("lxc readonly mode für / nur für lxc");
            self.lxc_readonly.setChecked(self.int_to_bool(sav_home_docker_folder));
            self.layouth_tmp1.addWidget(self.docker_system_label);
            self.layouth_tmp1.addWidget(self.docker_system);
            self.layouth_tmp1.addWidget(self.lxc_readonly);
            self.layoutv1.addLayout(self.layouth_tmp1);

            self.podman_runs_root_label = QtWidgets.QLabel("podman als root ausführen: off als user on als root per sudo (cdrom fix)")
            self.podman_runs_root = QtWidgets.QCheckBox();
            self.podman_runs_root.setChecked(self.int_to_bool(podman_runs_root));
            self.podman_runs_root.stateChanged.connect(self.docker_system_changed)
            self.layouth_tmp3 = QtWidgets.QHBoxLayout();
            self.layouth_tmp3.addWidget(self.podman_runs_root_label);
            self.layouth_tmp3.addWidget(self.podman_runs_root);
            self.layoutv1.addLayout(self.layouth_tmp3);

            self.layouth14 = QtWidgets.QHBoxLayout();
            self.docker_build_label = QtWidgets.QLabel("docker oder lxc oder podman oder vfiodock contaienr name das docker image wo gestatet wird: ");
            self.docker_build = QtWidgets.QLineEdit(docker_build);
            self.docker_build_combobox = QtWidgets.QComboBox();
            self.docker_build_combobox_add = QtWidgets.QPushButton("add")
            self.docker_build_combobox_add .clicked.connect(self.add_docker_build_combobox)
            self.docker_build_combobox_add_update = QtWidgets.QPushButton("update")
            self.docker_build_combobox_add_update .clicked.connect(self.update_docker_build_combobox)
            self.layouth14.addWidget(self.docker_build_label);
            self.layouth14.addWidget(self.docker_build);
            self.layouth14.addWidget(self.docker_build_combobox);
            self.layouth14.addWidget(self.docker_build_combobox_add)
            self.layouth14.addWidget(self.docker_build_combobox_add_update)
            self.layoutv1.addLayout(self.layouth14);

            self.layouth_tmp3 =  QtWidgets.QHBoxLayout();
            self.layouth_tmp3_label = QtWidgets.QLabel("--------------------------------------------------------CPU & RAM--------------------------------------------------------")
            self.layouth_tmp3.addWidget(self.layouth_tmp3_label);
            self.layoutv1.addLayout(self.layouth_tmp3);

            self.layouth15 = QtWidgets.QHBoxLayout();
            self.maxmemory_label = QtWidgets.QLabel("Mazialer zugelassener RAN verbauch in Megabyte (-1 == keine Beschrnäkung): ");
            self.maxmemory = QtWidgets.QSpinBox();
            self.maxmemory.setMinimum(-1);
            self.maxmemory.setMaximum(2147483647);
            self.maxmemory.setValue(maxmemory);
            self.layouth15.addWidget(self.maxmemory_label);
            self.layouth15.addWidget(self.maxmemory);
            self.layoutv1.addLayout(self.layouth15);

            self.layouth16 = QtWidgets.QHBoxLayout();
            self.maxcpus_label = QtWidgets.QLabel("Wie viele CPUS darf der docker container nutzen in threads (-1 == keine Beschrnäkung): ");
            self.maxcpus = QtWidgets.QSpinBox();
            self.maxcpus.setMinimum(-1);
            self.maxcpus.setMaximum(2147483647);
            self.maxcpus.setValue(maxcpus);
            self.layouth16.addWidget(self.maxcpus_label);
            self.layouth16.addWidget(self.maxcpus);
            self.layoutv1.addLayout(self.layouth16);

            self.layouth_tmp4 =  QtWidgets.QHBoxLayout();
            self.layouth_tmp4_label = QtWidgets.QLabel("--------------------------------------------------------GPUS--------------------------------------------------------")
            self.layouth_tmp4.addWidget(self.layouth_tmp4_label);
            self.layoutv1.addLayout(self.layouth_tmp4);


            self.layouth2 = QtWidgets.QHBoxLayout()
            self.gpu_render_label =  QtWidgets.QLabel("gpu_render: (nur für muti gpu user um bei opengl eine gpu zu wählen! bei 1ner gpu Bitte 0 lassen )");
            self.gpu_render = QtWidgets.QLineEdit();
            #self.gpu_render.setMinimum(0);
            self.gpu_render.setText(str(gpu_render));
            self.gpu_render_combobox = QtWidgets.QComboBox();
            self.gpu_render_combobox_set = QtWidgets.QPushButton("set as int")
            self.gpu_render_combobox_set .clicked.connect(self.set_combox_gpu_render)
            self.gpu_render_combobox_set_name_opengl_only = QtWidgets.QPushButton("set as gpu name for opengl only")
            self.gpu_render_combobox_set_name_opengl_only .clicked.connect(self.set_combox_gpu_render_name_opengl_only)
            self.gpu_render_combobox_set_name_vulkan_only = QtWidgets.QPushButton("set as gpu name for vulkan only")
            self.gpu_render_combobox_set_name_vulkan_only .clicked.connect(self.set_combox_gpu_render_name_vulkan_only)
            self.layouth2.addWidget(self.gpu_render_label);
            self.layouth2.addWidget(self.gpu_render);
            self.layouth2.addWidget(self.gpu_render_combobox);
            self.layouth2.addWidget(self.gpu_render_combobox_set);
            self.layouth2.addWidget(self.gpu_render_combobox_set_name_opengl_only);
            self.layouth2.addWidget(self.gpu_render_combobox_set_name_vulkan_only);
            self.layoutv1.addLayout(self.layouth2);

            self.layouth2_2 = QtWidgets.QHBoxLayout()
            self.vulkan_device_name =  QtWidgets.QLabel("vulkan device name bitte automatisch setzen lassen oder leer ab mesa 23.1 fehlerhaft: ");
            self.vulkan_device = QtWidgets.QLineEdit();
            self.vulkan_device.setText(vulkan_device_name);
            self.layouth2_2.addWidget(self.vulkan_device_name);
            self.layouth2_2.addWidget(self.vulkan_device);
            self.layoutv1.addLayout(self.layouth2_2);



            self.layouth_tmp4 =  QtWidgets.QHBoxLayout();
            self.layouth_tmp4_label = QtWidgets.QLabel("--------------------------------------------------------CD/DVD & USB--------------------------------------------------------")
            self.layouth_tmp4.addWidget(self.layouth_tmp4_label);
            self.layoutv1.addLayout(self.layouth_tmp4);

            self.layouth3 = QtWidgets.QHBoxLayout();
            self.disk_device_name_label = QtWidgets.QLabel("Standard Eisntellugn \"cd/dvd\" alle cd rom laufwerke werden in den docker container übernomen")
            self.disk_device_name = QtWidgets.QLineEdit(disk_device_name);
            self.layouth3.addWidget(self.disk_device_name_label);
            self.layouth3.addWidget(self.disk_device_name);
            self.layoutv1.addLayout(self.layouth3);

            self.layouth11 = QtWidgets.QHBoxLayout();
            self.usb_sharing = QtWidgets.QCheckBox("usb shring");
            self.usb_sharing.setChecked(self.int_to_bool(usb_sharing));
            self.steam_controller_bool = QtWidgets.QCheckBox("Steam controller in docker container nutzen");
            self.steam_controller_bool.setChecked(self.int_to_bool(steam_controller_bool));
            self.usb_name_label = QtWidgets.QLabel("usb gerät per usb name in docker hinzufügen (mehere device getrennt mit ^): ");
            self.usb_name = QtWidgets.QLineEdit(usb_name);
            self.usb_name_combobox = QtWidgets.QComboBox();
            self.usb_name_combobox_add = QtWidgets.QPushButton("add")
            self.usb_name_combobox_add .clicked.connect(self.add_combox_usb_share)
            self.usb_name_combobox_update = QtWidgets.QPushButton("update")
            self.usb_name_combobox_update .clicked.connect(self.update_usb_share_combox)
            self.layouth11.addWidget(self.usb_sharing);
            self.layouth11.addWidget(self.steam_controller_bool);
            self.layouth11.addWidget(self.usb_name_label);
            self.layouth11.addWidget(self.usb_name);
            self.layouth11.addWidget(self.usb_name_combobox);
            self.layouth11.addWidget(self.usb_name_combobox_add);
            self.layouth11.addWidget(self.usb_name_combobox_update);
            self.layoutv1.addLayout(self.layouth11);

            self.layouth13 = QtWidgets.QHBoxLayout();
            self.usb_hidraw_name_label = QtWidgets.QLabel("usb gerät per usb hdiraw name in docker hinzufügen (mehere device getrennt mit ^): ");
            self.usb_hidraw_name = QtWidgets.QLineEdit(usb_hidraw_name);
            self.usb_hidraw_combobox = QtWidgets.QComboBox();
            self.usb_hidraw_combobox_add = QtWidgets.QPushButton("add")
            self.usb_hidraw_combobox_add .clicked.connect(self.add_combox_hidraw_share)
            self.usb_hidraw_combobox_update = QtWidgets.QPushButton("update")
            self.usb_hidraw_combobox_update .clicked.connect(self.update_hidware_share_combox)
            self.layouth13.addWidget(self.usb_hidraw_name_label);
            self.layouth13.addWidget(self.usb_hidraw_name);
            self.layouth13.addWidget(self.usb_hidraw_combobox);
            self.layouth13.addWidget(self.usb_hidraw_combobox_add);
            self.layouth13.addWidget(self.usb_hidraw_combobox_update);
            self.layoutv1.addLayout(self.layouth13);

            self.layouth_tmp4 =  QtWidgets.QHBoxLayout();
            self.layouth_tmp4_label = QtWidgets.QLabel("--------------------------------------------------------NETWORK & Share Folder & Pacman cache & docker backup fodler--------------------------------------------------------")
            self.layouth_tmp4.addWidget(self.layouth_tmp4_label);
            self.layoutv1.addLayout(self.layouth_tmp4);

            self.layouth9 = QtWidgets.QHBoxLayout();
            self.network_disable = QtWidgets.QCheckBox("Netzwerk interface deaktiviren");
            self.network_disable.setChecked(self.int_to_bool(network_disable));
            self.layouth9.addWidget(self.network_disable);
            self.layoutv1.addLayout(self.layouth9);

            self.layouth17 = QtWidgets.QHBoxLayout();
            self.network_host_label = QtWidgets.QLabel("network_host gib eine netwerk geräte per name an oder lass es lerr für default network bridge more with network names ^ getrennt (\"0\" disable): ");
            tmp = network_host;
            if(type(tmp) == type([])):
                if(len(tmp) >= 1):
                    tmp = tmp[0];
                else:
                    tmp = "";
            self.network_host = QtWidgets.QLineEdit(tmp);
            #lxc_network_bridge_link
            self.lxc_network_bridge_link_link_eth0_lbael = QtWidgets.QLabel("Network link eth0 for internet: ");
            self.lxc_network_bridge_link = QtWidgets.QLineEdit(lxc_network_bridge_link);
            self.lxc_network_mac_label = QtWidgets.QLabel("macaddr from network \"\" is random mac addr lxc \"0\" for disable: ");
            self.lxc_network_mac = QtWidgets.QLineEdit(lxc_network_mac);
            self.lxc_network_mac_button = QtWidgets.QPushButton("create a radom mac addr");
            self.lxc_network_mac_button .clicked.connect(self.lxc_network_mac_set)
            self.layouth17.addWidget(self.network_host_label);
            self.layouth17.addWidget(self.network_host);
            self.layouth17.addWidget(self.lxc_network_bridge_link_link_eth0_lbael);
            self.layouth17.addWidget(self.lxc_network_bridge_link);
            self.layouth17.addWidget(self.lxc_network_mac_label);
            self.layouth17.addWidget(self.lxc_network_mac);
            self.layouth17.addWidget(self.lxc_network_mac_button);
            self.layoutv1.addLayout(self.layouth17);

            self.layouth29 = QtWidgets.QHBoxLayout();
            self.docker_disable_ipv6 = QtWidgets.QCheckBox("ipv6 addr dsiable");
            self.docker_disable_ipv6.setChecked(self.int_to_bool(docker_disable_ipv6));
            self.ipv6_privacy_label = QtWidgets.QLabel("ipv6_privacy mode (ramdon mac addr in ipv6 adress) 0 = disabel , 1= enable 2=all devies patch on Server: ");
            self.ipv6_privacy1 = QtWidgets.QSpinBox();
            self.ipv6_privacy1.setValue(ipv6_privacy);
            self.ipv6_privacy1.setMinimum(0);
            self.ipv6_privacy1.setMaximum(2);
            self.dhcpv6 = QtWidgets.QCheckBox("Netzwerk dhcpv6 aktiviren lxc only: ");
            self.dhcpv6.setChecked(self.int_to_bool(dhcpv6));
            self.layouth29.addWidget(self.docker_disable_ipv6);
            self.layouth29.addWidget(self.dhcpv6);
            self.layouth29.addWidget(self.ipv6_privacy_label);
            self.layouth29.addWidget(self.ipv6_privacy1);
            self.layoutv1.addLayout(self.layouth29);

            self.layouth21 = QtWidgets.QHBoxLayout();
            self.dns_label = QtWidgets.QLabel("ip addres eines custom DNS server: ");
            self.dns = QtWidgets.QLineEdit(dns);
            self.layouth21.addWidget(self.dns_label);
            self.layouth21.addWidget(self.dns);
            self.layoutv1.addLayout(self.layouth21);

            self.layouth22 = QtWidgets.QHBoxLayout();
            self.ipv4_label = QtWidgets.QLabel("Static ipv4 : ");
            self.ipv4 = QtWidgets.QLineEdit(ipv4);
            self.ipv6_label = QtWidgets.QLabel("Static ipv6 : ");
            self.ipv6 = QtWidgets.QLineEdit(ipv6);
            self.podman_set_route_gateway_ip_label = QtWidgets.QLabel("set ipv4 gateway (use for poadman network fix): ");
            self.podman_set_route_gateway_ip = QtWidgets.QLineEdit(podman_set_route_gateway_ip);
            self.layouth22.addWidget(self.ipv4_label);
            self.layouth22.addWidget(self.ipv4);
            self.layouth22.addWidget(self.ipv6_label);
            self.layouth22.addWidget(self.ipv6);
            self.layouth22.addWidget(self.podman_set_route_gateway_ip_label);
            self.layouth22.addWidget(self.podman_set_route_gateway_ip);
            self.layoutv1.addLayout(self.layouth22);

            self.layouth18 = QtWidgets.QHBoxLayout();
            self.portforwding_label = QtWidgets.QLabel("portforwding  zum beispiel \"1000:1000\" \"1000:1000/tcp\" \"1000:1000/udp\" für prot 1000 weiterleitung:  ");
            self.portforwding = QtWidgets.QLineEdit(portforwding);
            self.layouth18.addWidget(self.portforwding_label);
            self.layouth18.addWidget(self.portforwding);
            self.layoutv1.addLayout(self.layouth18);

            self.layouth20 = QtWidgets.QHBoxLayout();
            self.layouth20_1 = QtWidgets.QHBoxLayout();
            self.pacman_cache_label = QtWidgets.QLabel("pacman_cache setze hier ein path zu einem Ordner an wo der packet cache von pacman gesichert wird: ");
            self.pacman_cache = QtWidgets.QLineEdit(pacman_cache);
            self.pacman_cache_browse = QtWidgets.QPushButton("browse..")
            self.pacman_cache_browse .clicked.connect(self.set_pacman_cache_folder)
            self.docker_auto_sav_fodler_label = QtWidgets.QLabel("docker and lxc contaienr sav fodler for run ./auto_update and ./auto_backup: ");
            self.docker_auto_sav_fodler = QtWidgets.QLineEdit(docker_auto_sav_fodler);
            self.docker_auto_sav_fodler_broswe = QtWidgets.QPushButton("browse..")
            self.docker_auto_sav_fodler_broswe .clicked.connect(self.set_docker_auto_sav_fodler)
            self.layouth20.addWidget(self.pacman_cache_label);
            self.layouth20.addWidget(self.pacman_cache);
            self.layouth20.addWidget(self.pacman_cache_browse);
            self.layoutv1.addLayout(self.layouth20);
            self.layouth20_1.addWidget(self.docker_auto_sav_fodler_label);
            self.layouth20_1.addWidget(self.docker_auto_sav_fodler);
            self.layouth20_1.addWidget(self.docker_auto_sav_fodler_broswe);
            self.layoutv1.addLayout(self.layouth20_1);

            self.layouth27 = QtWidgets.QHBoxLayout();
            self.pacman_pakgage_install_label = QtWidgets.QLabel("pacman install pakage von pacman zu installirende packet beim build des continer: ");
            self.pacman_pakgage_install = QtWidgets.QLineEdit(pacman_pakgage_install);
            self.layouth27.addWidget(self.pacman_pakgage_install_label);
            self.layouth27.addWidget(self.pacman_pakgage_install);
            self.layoutv1.addLayout(self.layouth27);











            self.layouth4 = QtWidgets.QHBoxLayout();
            self.zugriff_auf_media = QtWidgets.QCheckBox("docker Verzeichnis frei gabe von /run/media");
            self.zugriff_auf_media.setChecked(self.int_to_bool(zugriff_auf_media));
            self.sav_home_docker_folder = QtWidgets.QCheckBox("docker Verzeichnis frei gabe von home Ordner im aktuellen ordner");
            self.sav_home_docker_folder.setChecked(self.int_to_bool(sav_home_docker_folder));
            self.share_folder_daten = QtWidgets.QCheckBox("docker Verzeichnis frei gabe von share fodler daten im /home/daten folder Ordner im aktuellen ordner");
            self.share_folder_daten.setChecked(self.int_to_bool(share_folder_daten));
            self.layouth4.addWidget(self.zugriff_auf_media);
            self.layouth4.addWidget(self.sav_home_docker_folder);
            self.layouth4.addWidget(self.share_folder_daten);
            self.layoutv1.addLayout(self.layouth4);

            self.layouth7 = QtWidgets.QHBoxLayout();
            self.share_folder1_aktiv = QtWidgets.QCheckBox("docker Verzeichnis frei gabe von eigner share fodler akriviren");
            self.share_folder1_aktiv.setChecked(self.int_to_bool(share_folder1_aktiv));
            self.share_folder1_label = QtWidgets.QLabel("eingner share fodler /run/media:/run/media:ro mounted /run/media als readonly mehre ordner mit ^ trenen:")
            self.share_folder1 = QtWidgets.QLineEdit(share_folder1);
            self.share_folder1 .textChanged.connect(self.share_folder1_textChanged)
            self.share_folder1_browse = QtWidgets.QPushButton("browse..")
            self.share_folder1_browse .clicked.connect(self.set_share_folder1)
            self.layouth7.addWidget(self.share_folder1_aktiv);
            self.layouth7.addWidget(self.share_folder1_label);
            self.layouth7.addWidget(self.share_folder1);
            self.layouth7.addWidget(self.share_folder1_browse);
            self.layoutv1.addLayout(self.layouth7);




            self.layouth_tmp4 =  QtWidgets.QHBoxLayout();
            self.layouth_tmp4_label = QtWidgets.QLabel("--------------------------------------------------------Docker User Name & Acess Allow--------------------------------------------------------")
            self.layouth_tmp4.addWidget(self.layouth_tmp4_label);
            self.layoutv1.addLayout(self.layouth_tmp4);

            self.layouth1 = QtWidgets.QHBoxLayout()
            self.docker_user_label = QtWidgets.QLabel("docker_user:");
            self.docker_user = QtWidgets.QLineEdit(docker_user);
            self.layouth1.addWidget(self.docker_user_label);
            self.layouth1.addWidget(self.docker_user);
            self.layoutv1.addLayout(self.layouth1);

            self.layouth1_4 =  QtWidgets.QHBoxLayout();
            self.docker_user_password_label =  QtWidgets.QLabel("docker user password setzen (ohne \ bitte):");
            self.docker_user_password = QtWidgets.QLineEdit(docker_user_password);
            self.layouth1_4.addWidget(self.docker_user_password_label);
            self.layouth1_4.addWidget(self.docker_user_password);
            self.layoutv1.addLayout(self.layouth1_4);



            self.layouth19 = QtWidgets.QHBoxLayout();
            self.dbus_rw = QtWidgets.QCheckBox("dbus_rw beschreibar für manch anwedeungen benötigt z.B. Gamescope ");
            self.dbus_rw.setChecked(self.int_to_bool(dbus_rw));
            self.gamescope_bypass = QtWidgets.QCheckBox("Gamescope bypas");
            self.gamescope_bypass.setChecked(self.int_to_bool(gamescope_bypass));
            self.gamescope_render_auflosung_label =  QtWidgets.QLabel("gamescope gamescope_render_auflosung set ("" is default 720p, \"1920x1080\" is FULL HD  ):");
            self.gamescope_render_auflosung = QtWidgets.QLineEdit(gamescope_render_auflosung);
            self.layouth19.addWidget(self.dbus_rw);
            self.layouth19.addWidget(self.gamescope_bypass);
            self.layouth19.addWidget(self.gamescope_render_auflosung_label);
            self.layouth19.addWidget(self.gamescope_render_auflosung);
            self.layoutv1.addLayout(self.layouth19);

            self.layouth23 = QtWidgets.QHBoxLayout();
            self.wireguard_fix = QtWidgets.QCheckBox("wiregaurd fix und openvpn fix");
            self.wireguard_fix.setChecked(self.int_to_bool(wireguard_fix));
            self.nosudo = QtWidgets.QCheckBox("nosudo keine sudo rechte nicht zum bauen des container gegeignet");
            self.nosudo.setChecked(self.int_to_bool(nosudo));
            self.run_in_background = QtWidgets.QCheckBox("run_in_background");
            self.run_in_background.setChecked(self.int_to_bool(run_in_background));
            self.ttyon_label = QtWidgets.QLabel("ttyon ttyterminal in docker coantiner 0 = disabel , 1= enable, 2=docker checkpoint mdoe on: ");
            self.ttyon = QtWidgets.QSpinBox();
            self.ttyon.setValue(ttyon);
            self.ttyon.setMinimum(0);
            self.ttyon.setMaximum(2);
            self.layouth23.addWidget(self.wireguard_fix);
            self.layouth23.addWidget(self.nosudo);
            self.layouth23.addWidget(self.run_in_background);
            self.layouth23.addWidget(self.ttyon_label);
            self.layouth23.addWidget(self.ttyon);
            self.layoutv1.addLayout(self.layouth23);

            self.layouth28 = QtWidgets.QHBoxLayout();
            self.docker_input_label = QtWidgets.QLabel("docker input: block \"*\" /dev/input ");
            self.docker_input = QtWidgets.QLineEdit(docker_input);
            self.layouth28.addWidget(self.docker_input_label);
            self.layouth28.addWidget(self.docker_input);
            self.layoutv1.addLayout(self.layouth28);

            self.layouth27 = QtWidgets.QHBoxLayout();
            self.bluethoot_passthrough = QtWidgets.QCheckBox("Bluethoot_passthrough");
            self.bluethoot_passthrough.setChecked(self.int_to_bool(bluethoot_passthrough));
            self.hidraw_acs_overrides_patch = QtWidgets.QCheckBox("USB Hidraw acs overrides patch (alow docker user readwrite Hidraw devices");
            self.hidraw_acs_overrides_patch.setChecked(self.int_to_bool(hidraw_acs_overrides_patch));
            self.layouth27.addWidget(self.bluethoot_passthrough);
            self.layouth27.addWidget(self.hidraw_acs_overrides_patch);
            self.layoutv1.addLayout(self.layouth27);

            self.layouth31 = QtWidgets.QHBoxLayout();
            self.wine_32bit_speed_hak = QtWidgets.QCheckBox("wine_32bit_speed_hak, lol speed hak (sysctl -w abi.vsyscall32=0)");
            self.wine_32bit_speed_hak.setChecked(self.int_to_bool(wine_32bit_speed_hak));
            self.amd_gpu_raytrasing_allgpus = QtWidgets.QCheckBox("amd gpu for all raytrasing support");
            self.amd_gpu_raytrasing_allgpus.setChecked(self.int_to_bool(amd_gpu_raytrasing_allgpus));
            self.amd_gpu_raytrasing_allgpus.toggled.connect(self.amdgpu_spinbox_value_change)
            self.amd_gpu_raytrasing_rdan2_only = QtWidgets.QCheckBox("amd gpu for all raytrasing wav64 sped hak support rdna 2(amd rx 6000) only up mesa 22.0");
            self.amd_gpu_raytrasing_rdan2_only.setChecked(self.int_to_bool(amd_gpu_raytrasing_rdan2_only));
            self.amd_gpu_raytrasing_rdan2_only.toggled.connect(self.amdgpu_spinbox_value_change)
            self.amdgpu_gpl_pipline = QtWidgets.QCheckBox("amd gpu experimentel gpl pipline mesa 22.3");
            self.amdgpu_gpl_pipline.setChecked(self.int_to_bool(amdgpu_gpl_pipline));
            self.wineesync_and_winefsync = QtWidgets.QCheckBox("wine and Proton speed patch FSYNC ab linux kernel 5.19");
            self.wineesync_and_winefsync.setChecked(self.int_to_bool(wineesync_and_winefsync));
            self.layouth31.addWidget(self.wine_32bit_speed_hak);
            self.layouth31.addWidget(self.amd_gpu_raytrasing_allgpus);
            self.layouth31.addWidget(self.amd_gpu_raytrasing_rdan2_only);
            self.layouth31.addWidget(self.amdgpu_gpl_pipline);
            self.layouth31.addWidget(self.wineesync_and_winefsync);
            self.layoutv1.addLayout(self.layouth31);
            self.amd_gpu_raytrasing_bak = 0;

            self.nvidia_dlss = QtWidgets.QCheckBox("aktiviren NVIDIA DLSS (dxvk nvapi hak)");
            self.nvidia_dlss.setChecked(self.int_to_bool(nvidia_dlss));
            self.nvidia_dlss.toggled.connect(self.nvidia_dlss_change)
            self.nvidia_dlss_non_nvida_gpu = QtWidgets.QCheckBox("aktiviren NVIDAI DLSS non NVIDIA GPU");
            self.nvidia_dlss_non_nvida_gpu.setChecked(self.int_to_bool(nvidia_dlss_non_nvida_gpu));
            self.nvidia_dlss_non_nvida_gpu.toggled.connect(self.nvidia_dlss_non_nvida_gpu_change)
            self.layouth31_2 = QtWidgets.QHBoxLayout();
            self.layouth31_2.addWidget(self.nvidia_dlss);
            self.layouth31_2.addWidget(self.nvidia_dlss_non_nvida_gpu);
            self.layoutv1.addLayout(self.layouth31_2);

            self.pulseaudio_stotterfix = QtWidgets.QCheckBox("pulseaudio stotter fix");
            self.pulseaudio_stotterfix.setChecked(self.int_to_bool(pulseaudio_stotterfix));

            self.pluseaudio_sdl_fix_label = QtWidgets.QLabel("pulseaudio sdl use fix for steam and other apps: 0 = disable, 1=pluseaudio, 2=alsa")
            self.pluseaudio_sdl_fix = QtWidgets.QSpinBox();
            self.pluseaudio_sdl_fix.setValue(pluseaudio_sdl_fix);
            self.pluseaudio_sdl_fix.setMaximum(2);
            self.pluseaudio_sdl_fix.setMinimum(0);


            self.amdgpu_nohyperz = QtWidgets.QCheckBox("yuzu emu amd gpu grafik fix");
            self.amdgpu_nohyperz.setChecked(self.int_to_bool(amdgpu_nohyperz));
            self.ryujinx_emu_crash_fix =  QtWidgets.QCheckBox("ryujinx emu amd gpu grafik fix");
            self.ryujinx_emu_crash_fix.setChecked(self.int_to_bool(ryujinx_emu_crash_fix));
            self.amdgpu_pswave32 = QtWidgets.QCheckBox("amdgpu enable wave32 for pixel shaders (GFX10+)");
            self.amdgpu_pswave32.setChecked(self.int_to_bool(amdgpu_pswave32));
            self.amdgpu_nv_ms = QtWidgets.QCheckBox("amdgpu enable unofficial experimental support for NV_mesh_shader");
            self.amdgpu_nv_ms.setChecked(self.int_to_bool(amdgpu_nv_ms));
            self.amdgpu_mesh_shader_support = QtWidgets.QCheckBox("amdgpu rdna 2 oder hoeher enable unofficial experimental support for NV_mesh_shader");
            self.amdgpu_mesh_shader_support.setChecked(self.int_to_bool(amdgpu_mesh_shader_support));
            self.amdgpu_vrs = QtWidgets.QComboBox();
            if(amdgpu_vrs == ""):
                self.amdgpu_vrs_array = ["disable", "1x1", "1x2", "2x1", "2x2"]
            else:
                self.amdgpu_vrs_array = [amdgpu_vrs, "disable", "1x1", "1x2", "2x1", "2x2"]
            self.amdgpu_vrs.addItems(self.amdgpu_vrs_array)
            self.amdgpu_vrs.update();
            self.layouth31_3 = QtWidgets.QHBoxLayout();
            self.layouth31_3.addWidget(self.pulseaudio_stotterfix);
            self.layouth31_3.addWidget(self.pluseaudio_sdl_fix_label);
            self.layouth31_3.addWidget(self.pluseaudio_sdl_fix);
            self.layouth31_3.addWidget(self.amdgpu_nohyperz);
            self.layouth31_3.addWidget(self.ryujinx_emu_crash_fix);
            self.layouth31_3.addWidget(self.amdgpu_mesh_shader_support);
            self.layouth31_3.addWidget(self.amdgpu_nv_ms);
            self.layouth31_3.addWidget(self.amdgpu_nv_ms);
            self.layouth31_3.addWidget(self.amdgpu_vrs);
            self.layoutv1.addLayout(self.layouth31_3);


            self.layouth_tmp6 =  QtWidgets.QHBoxLayout();
            self.layouth_tmp6_label = QtWidgets.QLabel("--------------------------------------------------------Time & Advacne--------------------------------------------------------")
            self.layouth_tmp6.addWidget(self.layouth_tmp6_label);
            self.layoutv1.addLayout(self.layouth_tmp6);

            self.layouth30 = QtWidgets.QHBoxLayout();
            self.faketime_label = QtWidgets.QLabel("faketime: (2008-12-24 08:15:42) (-1day)");
            self.faketime = QtWidgets.QLineEdit(faketime);
            self.faketime_clear_ = QtWidgets.QPushButton("clear and disable")
            self.faketime_clear_ .clicked.connect(self.faketime_clear)
            self.faketime_set_to_real_time = QtWidgets.QPushButton("set to real time")
            self.faketime_set_to_real_time .clicked.connect(self.faketime_set_to_realtime)
            self.layouth30.addWidget(self.faketime_label);
            self.layouth30.addWidget(self.faketime);
            self.layouth30.addWidget(self.faketime_clear_);
            self.layouth30.addWidget(self.faketime_set_to_real_time);
            self.layoutv1.addLayout(self.layouth30);


            self.layouth34 = QtWidgets.QHBoxLayout();
            self.wine_fsr_label = QtWidgets.QLabel("wine Fidelity Super Rescoution (0 max - 5 lowest, -1 off): ");
            self.wine_fsr = QtWidgets.QSpinBox();
            self.wine_fsr.setMinimum(-1);
            self.wine_fsr.setMaximum(5);
            self.wine_fsr.setValue(wine_fsr);
            self.smart_acces_meomory = QtWidgets.QCheckBox("Smart Acess Memonry (kann leitsung beeifussen wenn nicht supportet mit der cpu)");
            self.smart_acces_meomory.setChecked(self.int_to_bool(smart_acces_meomory));
            self.layouth34.addWidget(self.wine_fsr_label);
            self.layouth34.addWidget(self.wine_fsr);
            self.layouth34.addWidget(self.smart_acces_meomory);
            self.layoutv1.addLayout(self.layouth34);

            self.layouth37 = QtWidgets.QHBoxLayout();
            self.steam_proton_run_without_steam = QtWidgets.QCheckBox("steam_proton_run_without_steam");
            self.steam_proton_run_without_steam.setChecked(self.int_to_bool(steam_proton_run_without_steam));
            self.mango_hud = QtWidgets.QCheckBox("mango_hud not used run Gamescope");
            self.mango_hud.setChecked(self.int_to_bool(mango_hud));
            self.vkbasalt = QtWidgets.QCheckBox("vkbasalt");
            self.vkbasalt.setChecked(self.int_to_bool(vkbasalt));
            self.layouth37.addWidget(self.steam_proton_run_without_steam);
            self.layouth37.addWidget(self.mango_hud);
            self.layouth37.addWidget(self.vkbasalt);
            self.layoutv1.addLayout(self.layouth37);

            self.layouth38 = QtWidgets.QHBoxLayout();
            self.freesync = QtWidgets.QCheckBox("freesync");
            self.freesync.setChecked(self.int_to_bool(freesync));
            self.freesync.toggled.connect(self.update_freesync_and_vsync_change)
            self.freesync_bak = 0;
            self.vsync = QtWidgets.QCheckBox("vsync");
            self.vsync.setChecked(self.int_to_bool(vsync));
            self.vsync.toggled.connect(self.update_freesync_and_vsync_change)
            self.ubisoft_connect_mut_fix = QtWidgets.QCheckBox("Ubisoft connect fix")
            self.ubisoft_connect_mut_fix.setChecked(self.int_to_bool(ubisoft_connect_mut_fix));
            self.vk_khr_present_wait = QtWidgets.QCheckBox("vk_khr_present_wait=true Vulkan swapchain wait patch for steam Play")
            self.vk_khr_present_wait.setChecked(self.int_to_bool(vk_khr_present_wait));
            self.layouth38.addWidget(self.freesync);
            self.layouth38.addWidget(self.vsync);
            self.layouth38.addWidget(self.ubisoft_connect_mut_fix);
            self.layouth38.addWidget(self.vk_khr_present_wait);
            self.layoutv1.addLayout(self.layouth38);



            self.layouth_tmp6 =  QtWidgets.QHBoxLayout();
            self.layouth_tmp6_label = QtWidgets.QLabel("--------------------------------------------------------VM Mager & Password--------------------------------------------------------")
            self.layouth_tmp6.addWidget(self.layouth_tmp6_label);
            self.layoutv1.addLayout(self.layouth_tmp6);

            self.layouth35 = QtWidgets.QHBoxLayout();
            self.mmanager_vm_fodler_label = QtWidgets.QLabel("VM Folder for VM Manger: ");
            self.manager_vm_fodler = QtWidgets.QLineEdit(manager_vm_fodler);
            self.manager_vm_fodler_browse_ = QtWidgets.QPushButton("browse..")
            self.manager_vm_fodler_browse_ .clicked.connect(self.manager_vm_fodler_browse)
            self.layouth35.addWidget(self.mmanager_vm_fodler_label);
            self.layouth35.addWidget(self.manager_vm_fodler);
            self.layouth35.addWidget(self.manager_vm_fodler_browse_);
            self.layoutv1.addLayout(self.layouth35);

            self.layouth32 = QtWidgets.QHBoxLayout();
            self.read_only = QtWidgets.QCheckBox("Beabeitungschutz");
            self.read_only.setChecked(self.int_to_bool(read_only));
            if(read_only != ""):
                self.read_only.setChecked(True);
            else:
                self.read_only.setChecked(False);
            self.read_only_password_label = QtWidgets.QLabel("Beabeitungschutz muss auf 1 stehe und hiere das Beabeitungschutz password");
            self.read_only_password = QtWidgets.QLineEdit(read_only_password);
            self.read_only_password_clear_ = QtWidgets.QPushButton("clear and disable")
            self.read_only_password_clear_ .clicked.connect(self.read_only_password_clear)
            #self.read_only_password.setEchoMode(QtWidgets.QLineEdit.Password)
            self.layouth32.addWidget(self.read_only);
            self.layouth32.addWidget(self.read_only_password_label);
            self.layouth32.addWidget(self.read_only_password);
            self.layouth32.addWidget(self.read_only_password_clear_);
            self.layoutv1.addLayout(self.layouth32);

            self.layouth99999999999 = QtWidgets.QHBoxLayout();
            self.button_save = QtWidgets.QPushButton("Save json")
            self.button_save .clicked.connect(self.save)
            self.layouth99999999999.addWidget(self.button_save);
            self.layoutv1.addLayout(self.layouth99999999999);

            self.docker_build_combobox_last = "";
            self.update_usb_share_combox();
            self.update_hidware_share_combox();
            self.update_gpu_render_combox();
            #self.showFullScreen();
            self.showMaximized();
            self.amdgpu_spinbox_value_change();
            self.update_docker_build_combobox();
            self.update_freesync_and_vsync_change();
            self.docker_system_changed();
            self.docker_system_changed();

            if(rest_config == 1):
                self.rest_config = 0;
                msgBox2 = QtWidgets.QMessageBox();
                msgBox2.setText("config was reset please set all settings new? ");
                out = msgBox2.exec();
            else:
                self.rest_config = 0;


            self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, self.w, self.h))
        def save(self):
            docker_user = self.docker_user.text();
            gpu_render = str(self.gpu_render.text());
            disk_device_name = self.disk_device_name.text();
            zugriff_auf_media = str(self.bool_to_int(self.zugriff_auf_media.isChecked()));
            sav_home_docker_folder = str(self.bool_to_int(self.sav_home_docker_folder.isChecked()));
            share_folder_daten = str(self.bool_to_int(self.share_folder_daten.isChecked()));
            share_folder1_aktiv = str(self.bool_to_int(self.share_folder1_aktiv.isChecked()));
            share_folder1 = self.share_folder1.text();
            network_disable = str(self.bool_to_int(self.network_disable.isChecked()));
            steam_controller_bool = str(self.bool_to_int(self.steam_controller_bool.isChecked()));
            usb_sharing = str(self.bool_to_int(self.usb_sharing.isChecked()));
            usb_name = self.usb_name.text();
            usb_hidraw_name = self.usb_hidraw_name.text();
            docker_build = self.docker_build.text();
            maxmemory = str(self.maxmemory.value())
            maxcpus = str(self.maxcpus.value())
            network_host = self.network_host.text();
            portforwding =  self.portforwding.text();
            dbus_rw =  str(self.bool_to_int(self.dbus_rw.isChecked()));
            pacman_cache = self.pacman_cache.text();
            dns = self.dns.text();
            ipv4 = self.ipv4.text();
            wireguard_fix = str(self.bool_to_int(self.wireguard_fix.isChecked()));
            nosudo = str(self.bool_to_int(self.nosudo.isChecked()));
            run_in_background = str(self.bool_to_int(self.run_in_background.isChecked()));
            ttyon = str(self.ttyon.value());
            pacman_pakgage_install = self.remove_string_tablaotor(self.pacman_pakgage_install.text());
            out = -1;
            if(pacman_pakgage_install != ""):
                if(pacman_pakgage_install != "bash "):
                    out = pacman_list_a_downlaod_pkg("");
                    out2 = check_array_pacman_pkg_exist(out, pacman_pakgage_install);
                    out = podman_pkg_doppelt_check(out2[0])
                    pacman_pakgage_install = out;
                    #out = [[], []];
                    if(len(out2[1]) >= 1):
                        msgBox2 = QtWidgets.QMessageBox();
                        tmp = "ERROR pacman_pakgage_install pkg names not found: ";
                        for tmp2 in out2[1]:
                            tmp = tmp + tmp2 + " ,";
                        msgBox2.setText(tmp);
                        msgBox2.exec();


            docker_input = self.docker_input.text();
            bluethoot_passthrough = str(self.bool_to_int(self.bluethoot_passthrough.isChecked()));
            hidraw_acs_overrides_patch = str(self.bool_to_int(self.hidraw_acs_overrides_patch.isChecked()));
            ipv6_privacy = str(self.ipv6_privacy1.value());
            faketime = self.faketime.text();

            wine_32bit_speed_hak = str(self.bool_to_int(self.wine_32bit_speed_hak.isChecked()));
            read_only = str(self.bool_to_int(self.read_only.isChecked()));
            read_only_password = self.read_only_password.text();
            amd_gpu_raytrasing_allgpus = str(self.bool_to_int(self.amd_gpu_raytrasing_allgpus.isChecked()));
            amd_gpu_raytrasing_rdan2_only = str(self.bool_to_int(self.amd_gpu_raytrasing_rdan2_only.isChecked()));
            wine_fsr = str(self.wine_fsr.value());
            manager_vm_fodler = self.manager_vm_fodler.text();
            smart_acces_meomory = str(self.bool_to_int(self.smart_acces_meomory.isChecked()));
            vulkan_device = self.vulkan_device.text();

            steam_proton_run_without_steam = str(self.bool_to_int(self.steam_proton_run_without_steam.isChecked()));
            mango_hud = str(self.bool_to_int(self.mango_hud.isChecked()));
            vkbasalt = str(self.bool_to_int(self.vkbasalt.isChecked()));
            freesync = str(self.bool_to_int(self.freesync.isChecked()));
            vsync = str(self.bool_to_int(self.vsync.isChecked()));
            docker_system = str(self.docker_system.value());
            lxc_readonly = str(self.bool_to_int(self.lxc_readonly.isChecked()));
            lxc_network_mac = self.lxc_network_mac.text();
            lxc_network_bridge_link = self.lxc_network_bridge_link.text();
            docker_disable_ipv6 = str(self.bool_to_int(self.docker_disable_ipv6.isChecked()));

            wineesync_and_winefsync = str(self.bool_to_int(self.wineesync_and_winefsync.isChecked()));
            nvidia_dlss = str(self.bool_to_int(self.nvidia_dlss.isChecked()));
            nvidia_dlss_non_nvida_gpu = str(self.bool_to_int(self.nvidia_dlss_non_nvida_gpu.isChecked()));
            pulseaudio_stotterfix = str(self.bool_to_int(self.pulseaudio_stotterfix.isChecked()));
            amdgpu_nohyperz = str(self.bool_to_int(self.amdgpu_nohyperz.isChecked()));
            amdgpu_pswave32 = str(self.bool_to_int(self.amdgpu_pswave32.isChecked()));
            amdgpu_nv_ms = str(self.bool_to_int(self.amdgpu_nv_ms.isChecked()));
            amdgpu_vrs = self.amdgpu_vrs_array[self.amdgpu_vrs.currentIndex()];
            pluseaudio_sdl_fix = str(self.pluseaudio_sdl_fix.value());
            if(amdgpu_vrs == "disable"):
                amdgpu_vrs = "";

            docker_auto_sav_fodler = self.docker_auto_sav_fodler.text();
            dhcpv6 = str(self.bool_to_int(self.dhcpv6.isChecked()));
            amdgpu_mesh_shader_support = str(self.bool_to_int(self.amdgpu_nv_ms.isChecked()));
            podman_runs_root = str(self.bool_to_int(self.podman_runs_root.isChecked()));
            podman_set_route_gateway_ip = self.podman_set_route_gateway_ip.text();
            ipv6 = self.ipv6.text();
            amdgpu_gpl_pipline =  str(self.bool_to_int(self.amdgpu_gpl_pipline.isChecked()));
            rest_config = self.rest_config;
            ubisoft_connect_mut_fix = str(self.bool_to_int(self.ubisoft_connect_mut_fix.isChecked()));
            vk_khr_present_wait = str(self.bool_to_int(self.vk_khr_present_wait.isChecked()));
            docker_user_password = self.docker_user_password.text();
            gamescope_bypass = str(self.bool_to_int(self.gamescope_bypass.isChecked()));
            ryujinx_emu_crash_fix =  str(self.bool_to_int(self.ryujinx_emu_crash_fix.isChecked()));
            gamescope_render_auflosung = self.gamescope_render_auflosung.text();

            gamescope_render_auflosung3 = 0;
            if(gamescope_render_auflosung != ""):
                if(gamescope_render_auflosung.find("x") != -1):
                    gamescope_render_auflosung2 = gamescope_render_auflosung.split("x");
                    if(int(gamescope_render_auflosung2[0]) >= 1240 ):
                        if(int(gamescope_render_auflosung2[1]) >= 720 ):
                            gamescope_render_auflosung3 = 1;
            else:
                gamescope_render_auflosung3 = 1;
            if(gamescope_render_auflosung3 == 0):
                msgBox2 = QtWidgets.QMessageBox();
                tmp = "ERROR gamescope_render_auflosung not correct!";
                msgBox2.setText(tmp);
                msgBox2.exec();
                return 0;
            if(amdgpu_nv_ms == "1"):
                amdgpu_mesh_shader_support = "1";
                amdgpu_nv_ms = "0";

            #, steam_proton_run_without_steam, mango_hud, vkbasalt
            optional_array = [smart_acces_meomory, vulkan_device, steam_proton_run_without_steam, mango_hud, vkbasalt, freesync, vsync, docker_system, lxc_readonly, lxc_network_mac, lxc_network_bridge_link, docker_disable_ipv6, nvidia_dlss, nvidia_dlss_non_nvida_gpu, wineesync_and_winefsync, pulseaudio_stotterfix, amdgpu_nohyperz, amdgpu_pswave32, amdgpu_nv_ms, amdgpu_vrs,
                                pluseaudio_sdl_fix, docker_auto_sav_fodler, dhcpv6, amdgpu_mesh_shader_support, podman_runs_root,
                                podman_set_route_gateway_ip, ipv6, amdgpu_gpl_pipline, rest_config, ubisoft_connect_mut_fix,
                                vk_khr_present_wait, docker_user_password, gamescope_bypass, ryujinx_emu_crash_fix, gamescope_render_auflosung];

            optional_array_str = self.optional_array_to_string(optional_array);

            #file_write_json(dirname + "/config_file_json", docker_user, gpu_render, disk_device_name, zugriff_auf_media, sav_home_docker_folder, share_folder_daten,
            #                share_folder1_aktiv, share_folder1, network_disable, steam_controller_bool, usb_sharing, usb_name, usb_hidraw_name,
            #                docker_build, maxmemory, maxcpus, network_host, portforwding, dbus_rw, pacman_cache, dns, ipv4, wireguard_fix,
            #                 nosudo, run_in_background, ttyon, pacman_pakgage_install, docker_input);
            file_write_json(dirname + "/config_file_json", docker_user, gpu_render, disk_device_name, zugriff_auf_media, sav_home_docker_folder, share_folder_daten, share_folder1_aktiv, share_folder1, network_disable, steam_controller_bool, usb_sharing, usb_name, usb_hidraw_name, docker_build, maxmemory, maxcpus, network_host, portforwding, dbus_rw, pacman_cache, dns, ipv4, wireguard_fix, nosudo, run_in_background, ttyon, pacman_pakgage_install, docker_input, bluethoot_passthrough, hidraw_acs_overrides_patch, ipv6_privacy, faketime, wine_32bit_speed_hak, read_only, read_only_password, amd_gpu_raytrasing_allgpus, amd_gpu_raytrasing_rdan2_only, wine_fsr, manager_vm_fodler, optional_array_str);
            msgBox2 = QtWidgets.QMessageBox();
            tmp = "Save!";
            if(out != -1):
                for tmp2 in out[1]:
                    tmp = tmp + tmp2 + ", ";
            msgBox2.setText(tmp);
            msgBox2.exec();
            return 0;

        def add_combox_usb_share(self):
            index = self.usb_name_combobox.currentIndex()
            s1 = self.usb_sahring_array[index];
            if(self.usb_name.text().find("^") == -1):
                if(self.usb_name.text() != s1):
                    if(self.usb_name.text() == ""):
                        self.usb_name.setText(s1);
                    else:
                        self.usb_name.setText(self.usb_name.text() + "^" + s1);
            else:
                s2 = self.usb_name.text().split("^");
                b1 = 0;
                for tmp in s2:
                    if(tmp == s1):
                        b1 = 1;
                        break;
                if(b1 == 0):
                    self.usb_name.setText(self.usb_name.text() + "^" + s1);
            return 0;

        def update_usb_share_combox(self):
            self.usb_sahring_array = read_lsusb();
            self.usb_name_combobox.clear()
            self.usb_name_combobox.addItems(self.usb_sahring_array)
            self.usb_name_combobox.update()
            self.usb_name_combobox.setEnabled(True)
            return 0;

        def update_hidware_share_combox(self):
            self.hidraw_sahring_array = read_hidraw();
            self.usb_hidraw_combobox.clear()
            self.usb_hidraw_combobox.addItems(self.hidraw_sahring_array)
            self.usb_hidraw_combobox.update()
            self.usb_hidraw_combobox.setEnabled(True)
            return 0;

        def add_combox_hidraw_share(self):
            index = self.usb_hidraw_combobox.currentIndex()
            s1 = self.hidraw_sahring_array[index];
            if(self.usb_hidraw_name.text().find("^") == -1):
                if(self.usb_hidraw_name.text() != s1):
                    if(self.usb_hidraw_name.text() == ""):
                        self.usb_hidraw_name.setText(s1);
                    else:
                        self.usb_hidraw_name.setText(self.usb_hidraw_name.text() + "^" + s1);
            else:
                s2 = self.usb_hidraw_name.text().split("^");
                b1 = 0;
                for tmp in s2:
                    if(tmp == s1):
                        b1 = 1;
                        break;
                if(b1 == 0):
                    self.usb_hidraw_name.setText(self.usb_hidraw_name.text() + "^" + s1);
            return 0;


        def update_gpu_render_combox(self):
            self.gpu_render_array = read_all_dri_prime_device("");
            self.gpu_render_combobox.clear()
            self.gpu_render_combobox.addItems(self.gpu_render_array)
            self.gpu_render_combobox.update()
            self.gpu_render_combobox.setEnabled(True)
            return 0;

        def set_combox_gpu_render(self):
            index = self.gpu_render_combobox.currentIndex()
            self.gpu_render.setText(str(index));
            #self.vulkan_device.setText("");
            return 0;

        def set_combox_gpu_render_name_vulkan_only(self):
            self.set_combox_gpu_render_name_opengl_only()
            #degrade fuktion vulkan_device fix 0.1a
            return 0;

            if(self.docker_system.value() == 0):
                #lxc
                index = self.gpu_render_combobox.currentIndex()
                self.gpu_render.setText(self.gpu_render_array[index].split(" (")[0]);
                #s1 = self.gpu_render_array[index].split("(")[1].split()[0].split(",")[0];
                s1 = self.gpu_render_array[index].split(" (")[0].split(" Series")[0].lower();
                s1 = s1.split();
                s1 = s1[len(s1) -1];
                if(DEBUG_MODE_jsongui == 1):
                    #print("opengl_device found set: ", self.gpu_render.text())
                    print("vulkan_device found set: ", s1)
                    print("vulkan only")
                self.gpu_render.setText("")
                self.vulkan_device.setText(s1);
            elif(self.docker_system.value() == 2):
                #pdoman
                self.vulkan_device.setText("opengl render use");
                index = self.gpu_render_combobox.currentIndex()
                self.gpu_render.setText("");
                s1 =  self.gpu_render_array[index].split("(")[0].split();
                self.vulkan_device.setText(s1[len(s1) - 1].lower());
                s1 = self.gpu_render_array[index].split("(")[1].split()[0].split(",")[0];
                #if(DEBUG_MODE_jsongui == 1):
                #    print("opengl_device found set: ", self.gpu_render.text())
                #    #print("vulkan_device found set: ", s1)
                #    print("opengl only")
            elif(self.docker_system.value() == 3):
                #vfiodock
                self.vulkan_device.setText("opengl render use");
                index = self.gpu_render_combobox.currentIndex()
                self.gpu_render.setText(self.gpu_render_array[index].split(" (")[0]);
                s1 = self.gpu_render_array[index].split("(")[1].split()[0].split(",")[0];
                if(DEBUG_MODE_jsongui == 1):
                    print("opengl_device found set: ", self.gpu_render.text())
                    #print("vulkan_device found set: ", s1)
                    print("opengl only")
            return 0;
        def set_combox_gpu_render_name_opengl_only(self):
            index = self.gpu_render_combobox.currentIndex()
            self.gpu_render.setText(self.gpu_render_array[index].split(" (")[0]);
            s1 = self.gpu_render_array[index].split("(")[1].split()[0].split(",")[0];
            if(DEBUG_MODE_jsongui == 1):
                print("opengl_device found set: ", self.gpu_render.text())
                #print("vulkan_device found set: ", s1)
                print("opengl only")
            #self.vulkan_device.setText("");
            name = self.gpu_render.text().split()[::-1][::2][::-1]
            name2 = "";
            for tmp in name:
                name2 = name2 + tmp + " "
            self.vulkan_device.setText(name2);
            self.gpu_render.setText(name2);
            return 0;

        def set_share_folder1(self):
            s1 = QtWidgets.QFileDialog.getExistingDirectory();
            if(self.share_folder1.text().find("^") == -1):
                if(self.share_folder1.text() != s1):
                    if(self.share_folder1.text() == ""):
                        self.share_folder1.setText(s1 + ":" + s1 + ":rw");
                    else:
                        self.share_folder1.setText(self.share_folder1.text() + "^" + s1 + ":" + s1 + ":rw");
            else:
                s2 = self.share_folder1.text().split("^");
                b1 = 0;
                for tmp in s2:
                    if(tmp == s1):
                        b1 = 1;
                        break;
                if(b1 == 0):
                    self.share_folder1.setText(self.share_folder1.text() + "^" + s1 + ":" + s1 + ":rw");
            return 0;

        def set_pacman_cache_folder(self):
            s1 = QtWidgets.QFileDialog.getExistingDirectory();
            self.pacman_cache.setText(s1);
            return 0;

        def faketime_clear(self):
            self.faketime_clear.setText("");
            return 0;

        def faketime_clear(self):
            self.faketime.setText("");
            return 0;

        def faketime_set_to_realtime(self):
            update = time.localtime(time.time());
            self.faketime.setText(str(update.tm_year) + "-" + str(update.tm_mon) + "-" + str(update.tm_mday) + " " + str(self.int_to_time(update.tm_hour)) + ":" + str(self.int_to_time(update.tm_min)) + ":" + str(self.int_to_time(update.tm_sec)));
            return 0;

        def int_to_time(self, i1):
            if(i1 < 10):
                return "0" + str(i1);
            return str(i1);

        def read_only_password_clear(self):
            self.read_only_password.setText("");
            return 0;

        def share_folder1_textChanged(self):
            if(self.share_folder1.text() == ""):
                self.share_folder1_aktiv.setChecked(False);
            else:
                self.share_folder1_aktiv.setChecked(True);
            return 0;

        def amdgpu_spinbox_value_change(self):
            if(self.amd_gpu_raytrasing_bak == 0 and self.amd_gpu_raytrasing_rdan2_only.isChecked() == True):
                self.amd_gpu_raytrasing_allgpus.setChecked(False);
                self.amd_gpu_raytrasing_bak = 1;
            elif(self.amd_gpu_raytrasing_bak == 1 and self.amd_gpu_raytrasing_allgpus.isChecked() == True):
                self.amd_gpu_raytrasing_rdan2_only.setChecked(False);
                self.amd_gpu_raytrasing_bak = 0;
            return 0;

        def update_docker_build_combobox(self):
            if(self.docker_system.value() == 0):
                #lxc
                self.docker_build_combobox_array = read_docker_imags(0);
                self.docker_build_combobox.clear()
                self.docker_build_combobox.addItems(self.docker_build_combobox_array)
                self.docker_build_combobox.update()
                self.docker_build_combobox.setEnabled(True)
            if(self.docker_system.value() == 1):
                #docker
                self.docker_build_combobox_array = read_docker_imags(1);
                self.docker_build_combobox.clear()
                self.docker_build_combobox.addItems(self.docker_build_combobox_array)
                self.docker_build_combobox.update()
                self.docker_build_combobox.setEnabled(True)
            if(self.docker_system.value() == 2):
                #podman
                self.docker_build_combobox_array = read_docker_imags(2, self.bool_to_int(self.podman_runs_root.isChecked()));
                self.docker_build_combobox.clear()
                self.docker_build_combobox.addItems(self.docker_build_combobox_array)
                self.docker_build_combobox.update()
                self.docker_build_combobox.setEnabled(True)
            if(self.docker_system.value() == 3):
                #vfiodock
                self.docker_build_combobox_array = read_docker_imags(3, 0);
                self.docker_build_combobox.clear()
                self.docker_build_combobox.addItems(self.docker_build_combobox_array)
                self.docker_build_combobox.update()
                self.docker_build_combobox.setEnabled(True)
            if(len(self.docker_build_combobox_array) >= 1):
                index = self.brechne_neue_lxc_coantiner_name(self.docker_build.text(), self.docker_build_combobox_array);
                self.docker_build_combobox_last = self.docker_build_combobox_array[index];
                #self.docker_build_combobox.setIndex(index);
            if(len(self.docker_build_combobox_array) != 0):
                self.docker_build.setText(self.docker_build_combobox_last);
            return 0;

        def update_freesync_and_vsync_change(self):
            if(self.freesync_bak == 0 and self.freesync.isChecked() == True):
                self.vsync.setChecked(True);
                self.freesync_bak = 1;
            elif(self.freesync_bak == 1 and self.vsync.isChecked() == False):
                self.freesync.setChecked(False);
                self.freesync_bak = 0;
            return 0;


        def add_docker_build_combobox(self):
            index = self.docker_build_combobox.currentIndex()
            s1 = self.docker_build_combobox_array[index];
            if(self.docker_build.text() != s1):
                self.docker_build.setText(s1);
            return 0;

        def manager_vm_fodler_browse(self):
            s1 = QtWidgets.QFileDialog.getExistingDirectory();
            self.manager_vm_fodler.setText(s1);
            return 0;

        def optional_array_to_string(self, array):
            s1 = "";
            for tmp in array:
                s1 = s1 + str(tmp) + "^";
            return s1;

        def bool_to_int(self, bool):
            if(bool == False):
                return 0;
            else:
                return 1;

        def int_to_bool(self, int):
            if(int == 0):
                return False;
            else:
                return True;

        def docker_system_changed(self):
            if(self.docker_system.value() == 0):
                #lxc
                #self.docker_build_combobox.setEnabled(False);
                #self.docker_build_combobox_add.setEnabled(False);
                self.maxmemory.setEnabled(False);
                self.maxcpus.setEnabled(False);
                #self.ipv4.setEnabled(False);
                self.portforwding.setEnabled(False);
                self.wireguard_fix.setEnabled(False);
                self.ttyon.setEnabled(False);
                #self.run_in_background.setEnabled(False);
                self.nosudo.setEnabled(False);
                #self.lxc_network_mac.setEnabled(True);
                self.lxc_readonly.setEnabled(True);
                self.gpu_render_combobox_set_name_opengl_only.setEnabled(False);
                self.gpu_render.setText("");
                self.gpu_render.setEnabled(False);
            elif(self.docker_system.value() == 1):
                #docker
                #self.docker_build_combobox.setEnabled(True);
                #self.docker_build_combobox_add.setEnabled(True);
                self.maxmemory.setEnabled(True);
                self.maxcpus.setEnabled(True);
                #self.ipv4.setEnabled(True);
                self.portforwding.setEnabled(True);
                self.wireguard_fix.setEnabled(True);
                self.ttyon.setEnabled(True);
                #self.run_in_background.setEnabled(True);
                self.nosudo.setEnabled(True);
                #self.lxc_network_mac.setEnabled(False);
                self.lxc_readonly.setEnabled(False);
                self.gpu_render_combobox_set_name_opengl_only.setEnabled(True);
                self.gpu_render.setEnabled(True);
                if(self.network_host.text() != "" and self.network_host.text() != "0"):
                    def question_networkbridge():
                        msgBox2 = QtWidgets.QMessageBox();
                        msgBox2.setText("delete the network bridge for docker conatiner? " + self.network_host.text() + ":");
                        yesbuttom = QtWidgets.QPushButton("Yes");
                        nobuttom = QtWidgets.QPushButton("No");
                        yesbuttom = msgBox2.addButton("Yes", QtWidgets.QMessageBox.ButtonRole.AcceptRole);
                        nobuttom = msgBox2.addButton("No", QtWidgets.QMessageBox.ButtonRole.NoRole);

                        out = msgBox2.exec();
                        if(msgBox2.clickedButton() == yesbuttom):
                            self.network_host.setText("");
                        elif(msgBox2.clickedButton() == nobuttom):
                            pass;
                        else:
                            pass;
                    question_networkbridge();
            elif(self.docker_system.value() == 2):
                #vfiodock
                #self.docker_build_combobox.setEnabled(True);
                #self.docker_build_combobox_add.setEnabled(True);
                self.maxmemory.setEnabled(True);
                self.maxcpus.setEnabled(True);
                #self.ipv4.setEnabled(True);
                self.portforwding.setEnabled(True);
                self.wireguard_fix.setEnabled(True);
                self.ttyon.setEnabled(True);
                #self.run_in_background.setEnabled(True);
                self.nosudo.setEnabled(True);
                #self.lxc_network_mac.setEnabled(False);
                self.lxc_readonly.setEnabled(False);
                self.gpu_render_combobox_set_name_opengl_only.setEnabled(True);
                self.gpu_render.setEnabled(True);
                if(self.network_host.text() != "" and self.network_host.text() != "0"):
                    def question_networkbridge():
                        msgBox2 = QtWidgets.QMessageBox();
                        msgBox2.setText("delete the network bridge for docker conatiner? " + self.network_host.text() + ":");
                        yesbuttom = QtWidgets.QPushButton("Yes");
                        nobuttom = QtWidgets.QPushButton("No");
                        yesbuttom = msgBox2.addButton("Yes", QtWidgets.QMessageBox.ButtonRole.AcceptRole);
                        nobuttom = msgBox2.addButton("No", QtWidgets.QMessageBox.ButtonRole.NoRole);

                        out = msgBox2.exec();
                        if(msgBox2.clickedButton() == yesbuttom):
                            self.network_host.setText("");
                        elif(msgBox2.clickedButton() == nobuttom):
                            pass;
                        else:
                            pass;
                    question_networkbridge();
            elif(self.docker_system.value() == 3):
                #pdoman
                #self.docker_build_combobox.setEnabled(True);
                #self.docker_build_combobox_add.setEnabled(True);
                self.maxmemory.setEnabled(True);
                self.maxcpus.setEnabled(True);
                #self.ipv4.setEnabled(True);
                self.portforwding.setEnabled(True);
                self.wireguard_fix.setEnabled(True);
                self.ttyon.setEnabled(True);
                #self.run_in_background.setEnabled(True);
                self.nosudo.setEnabled(True);
                #self.lxc_network_mac.setEnabled(False);
                self.lxc_readonly.setEnabled(False);
                self.gpu_render_combobox_set_name_opengl_only.setEnabled(True);
                self.gpu_render.setEnabled(True);
                if(self.network_host.text() != "" and self.network_host.text() != "0"):
                    def question_networkbridge():
                        msgBox2 = QtWidgets.QMessageBox();
                        msgBox2.setText("delete the network bridge for docker conatiner? " + self.network_host.text() + ":");
                        yesbuttom = QtWidgets.QPushButton("Yes");
                        nobuttom = QtWidgets.QPushButton("No");
                        yesbuttom = msgBox2.addButton("Yes", QtWidgets.QMessageBox.ButtonRole.AcceptRole);
                        nobuttom = msgBox2.addButton("No", QtWidgets.QMessageBox.ButtonRole.NoRole);

                        out = msgBox2.exec();
                        if(msgBox2.clickedButton() == yesbuttom):
                            self.network_host.setText("");
                        elif(msgBox2.clickedButton() == nobuttom):
                            pass;
                        else:
                            pass;
                    question_networkbridge();
            self.update_docker_build_combobox();
            return 0;

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

        def remove_string_tablaotor(self, s1):
            out = "";
            for tmp in s1:
                if (tmp == '\r'):
                    out = out +  " ";
                elif (tmp == '\t'):
                    out = out +  " ";
                elif (tmp == '\n'):
                    out = out +  " ";
                else:
                    out = out + tmp;
            return out;

        def remove_numbers_String(self, s1):
            out = "";
            for tmp in s1:
                if(tmp == "0"):
                    continue;
                elif(tmp == "1"):
                    continue;
                elif(tmp == "2"):
                    continue;
                elif(tmp == "3"):
                    continue;
                elif(tmp == "4"):
                    continue;
                elif(tmp == "5"):
                    continue;
                elif(tmp == "6"):
                    continue;
                elif(tmp == "7"):
                    continue;
                elif(tmp == "8"):
                    continue;
                elif(tmp == "9"):
                    continue;
                else:
                    out = out + tmp;
            return out;

        def nvidia_dlss_change(self):
            if(self.nvidia_dlss.isChecked() == True):
                self.smart_acces_meomory.setChecked(True);
            else:
                self.nvidia_dlss_non_nvida_gpu.setChecked(False);
        def nvidia_dlss_non_nvida_gpu_change(self):
            if(self.nvidia_dlss_non_nvida_gpu.isChecked() == True):
                self.smart_acces_meomory.setChecked(True);
                self.nvidia_dlss.setChecked(True);
        def lxc_network_mac_set(self):
            self.lxc_network_mac.setText(lxc_create_a_new_random_mac_addr());
            return 0;

        def set_docker_auto_sav_fodler(self):
            s1 = QtWidgets.QFileDialog.getExistingDirectory();
            self.docker_auto_sav_fodler.setText(s1);
            return 0;













    while True:
            mainwindow = seb_sync_clinet_gui()
            if(sav_and_exit == 1):
                mainwindow.save();
                exit();
                break;
            else:
                mainwindow.show()
                app.exec()
                exit();
                break;
            break;

def brechne_neue_lxc_coantiner_name_build(last, out):
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
