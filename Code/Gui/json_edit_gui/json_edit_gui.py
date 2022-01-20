#!/usr/bin/env python
#Copyright (C) 2022  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#this is a fork from https://github.com/kritzsie/steam-on-docker

version = "0.3f_3"
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
appname = "Seb Docker build json edit config"


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


def read_glxinfo(dri_prime):
    if(list_all_gpus() <= dri_prime):
        return "";
    cmd = cmd_start("DRI_PRIME=" + str(dri_prime) + " glxinfo | grep \"OpenGL renderer\"");
    if(len(cmd) == 0):
        return "ERROR mesa-utils not installed!";
    s1 = cmd[0].split("OpenGL renderer string: ");
    return s1[1]

def list_all_gpus():
    i1 = -1;
    cmd = cmd_start("lspci -v | grep \"Kernel driver in use: amdgpu\"");
    i1 = i1 + len(cmd);
    cmd = cmd_start("lspci -v | grep \"Kernel driver in use: radeon\"");
    i1 = i1 + len(cmd);
    return i1;

def read_all_dri_prime_device():
    out = [];
    for i in range(40):
        s1 = read_glxinfo(i);
        if(s1 != ""):
            out.append(s1);
    return out;

def start_json_edit_gui(dirname, docker_user, gpu_render, disk_device_name, zugriff_auf_media, sav_home_docker_folder, share_folder_daten,
                    share_folder1_aktiv, share_folder1, network_disable, steam_controller_bool, usb_sharing, usb_name, usb_hidraw_name,
                    docker_build, docker_input, maxmemory, maxcpus, network_host, portforwding, dbus_rw, pacman_cache, dns, ipv4,
                    wireguard_fix, nosudo, run_in_background, ttyon, pacman_pakgage_install, bluethoot_passthrough, hidraw_acs_overrides_patch,
                    ipv6_privacy, faketime, wine_32bit_speed_hak, read_only, read_only_password):
    from PyQt5 import QtWidgets
    from PyQt5 import QtGui
    from PyQt5 import QtCore
    import time
    import datetime
    app = QtWidgets.QApplication(sys.argv);
    class seb_sync_clinet_gui(QtWidgets.QWidget):
        def __init__(self):
            QtWidgets.QWidget.__init__(self)

            self.statusbar = QtWidgets.QStatusBar()
            self.statusbar.showMessage("test")
            self.title = appname + " - " + version
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

            if(read_only_password != ""):
                text, ok =  QtWidgets.QInputDialog.getText(self, 'config file passwort Farge!', 'Zum bearbeiten Bitte das Password:', QtWidgets.QLineEdit.NoEcho);
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

            self.layouth1 = QtWidgets.QHBoxLayout()
            self.docker_user_label = QtWidgets.QLabel("docker_user:");
            self.docker_user = QtWidgets.QLineEdit(docker_user);
            self.layouth1.addWidget(self.docker_user_label);
            self.layouth1.addWidget(self.docker_user);
            self.layoutv1.addLayout(self.layouth1);

            self.layouth2 = QtWidgets.QHBoxLayout()
            self.gpu_render_label =  QtWidgets.QLabel("gpu_render: (nur für muti gpu user um bei opengl eine gpu zu wählen! bei 1ner gpu Bitte 0 lassen )");
            self.gpu_render = QtWidgets.QSpinBox();
            self.gpu_render.setMinimum(0);
            self.gpu_render.setValue(int(gpu_render));
            self.gpu_render_combobox = QtWidgets.QComboBox();
            self.gpu_render_combobox_set = QtWidgets.QPushButton("set")
            self.gpu_render_combobox_set .clicked.connect(self.set_combox_gpu_render)
            self.layouth2.addWidget(self.gpu_render_label);
            self.layouth2.addWidget(self.gpu_render);
            self.layouth2.addWidget(self.gpu_render_combobox);
            self.layouth2.addWidget(self.gpu_render_combobox_set);
            self.layoutv1.addLayout(self.layouth2);

            self.layouth3 = QtWidgets.QHBoxLayout();
            self.disk_device_name_label = QtWidgets.QLabel("Standard Eisntellugn \"cd/dvd\" alle cd rom laufwerke werden in den docker container übernomen")
            self.disk_device_name = QtWidgets.QLineEdit(disk_device_name);
            self.layouth3.addWidget(self.disk_device_name_label);
            self.layouth3.addWidget(self.disk_device_name);
            self.layoutv1.addLayout(self.layouth3);

            self.layouth4 = QtWidgets.QHBoxLayout();
            self.zugriff_auf_media_label = QtWidgets.QLabel("docker Verzeichnis frei gabe von /run/media 1=on, 0=off")
            self.zugriff_auf_media = QtWidgets.QSpinBox();
            self.zugriff_auf_media.setMinimum(0);
            self.zugriff_auf_media.setMaximum(1);
            self.zugriff_auf_media.setValue(zugriff_auf_media);
            self.layouth4.addWidget(self.zugriff_auf_media_label);
            self.layouth4.addWidget(self.zugriff_auf_media);
            self.layoutv1.addLayout(self.layouth4);

            self.layouth5 = QtWidgets.QHBoxLayout();
            self.sav_home_docker_folder_label = QtWidgets.QLabel("docker Verzeichnis frei gabe von home Ordner 1=on, 0=off")
            self.sav_home_docker_folder = QtWidgets.QSpinBox();
            self.sav_home_docker_folder.setMinimum(0);
            self.sav_home_docker_folder.setMaximum(1);
            self.sav_home_docker_folder.setValue(sav_home_docker_folder);
            self.layouth5.addWidget(self.sav_home_docker_folder_label);
            self.layouth5.addWidget(self.sav_home_docker_folder);
            self.layoutv1.addLayout(self.layouth5);

            self.layouth6 = QtWidgets.QHBoxLayout();
            self.share_folder_daten_label = QtWidgets.QLabel("docker Verzeichnis frei gabe von sahre fodler daten im home folder Ordner 1=on, 0=off")
            self.share_folder_daten = QtWidgets.QSpinBox();
            self.share_folder_daten.setMinimum(0);
            self.share_folder_daten.setMaximum(1);
            self.share_folder_daten.setValue(share_folder_daten);
            self.layouth6.addWidget(self.share_folder_daten_label);
            self.layouth6.addWidget(self.share_folder_daten);
            self.layoutv1.addLayout(self.layouth6);

            self.layouth7 = QtWidgets.QHBoxLayout();
            self.share_folder1_aktiv_label = QtWidgets.QLabel("docker Verzeichnis frei gabe von eigner share fodler akriviren 1=on, 0=off")
            self.share_folder1_aktiv = QtWidgets.QSpinBox();
            self.share_folder1_aktiv.setMinimum(0);
            self.share_folder1_aktiv.setMaximum(1);
            self.share_folder1_aktiv.setValue(share_folder1_aktiv);
            self.layouth7.addWidget(self.share_folder1_aktiv_label);
            self.layouth7.addWidget(self.share_folder1_aktiv);
            self.layoutv1.addLayout(self.layouth7);

            self.layouth8 = QtWidgets.QHBoxLayout();
            self.share_folder1_label = QtWidgets.QLabel("eingner share fodler /run/media:/run/media:ro mounted /run/media als readonly mehre ordner mit ^ trenen:")
            self.share_folder1 = QtWidgets.QLineEdit(share_folder1);
            self.share_folder1 .textChanged.connect(self.share_folder1_textChanged)
            self.share_folder1_browse = QtWidgets.QPushButton("browse..")
            self.share_folder1_browse .clicked.connect(self.set_share_folder1)
            self.layouth8.addWidget(self.share_folder1_label);
            self.layouth8.addWidget(self.share_folder1);
            self.layouth8.addWidget(self.share_folder1_browse);
            self.layoutv1.addLayout(self.layouth8);

            self.layouth9 = QtWidgets.QHBoxLayout();
            self.network_disable_label = QtWidgets.QLabel("Netzwerk interface deaktiviren #0=Netzwerk aktive #1=Netzwerk deaktivirt");
            self.network_disable = QtWidgets.QSpinBox();
            self.network_disable.setValue(network_disable);
            self.network_disable.setMinimum(0);
            self.network_disable.setMaximum(1);
            self.layouth9.addWidget(self.network_disable_label);
            self.layouth9.addWidget(self.network_disable);
            self.layoutv1.addLayout(self.layouth9);

            self.layouth10 = QtWidgets.QHBoxLayout();
            self.steam_controller_bool_label = QtWidgets.QLabel("Steam controller in docker container nutzen #1= akriv");
            self.steam_controller_bool = QtWidgets.QSpinBox();
            self.steam_controller_bool.setValue(steam_controller_bool);
            self.steam_controller_bool.setMinimum(0);
            self.steam_controller_bool.setMaximum(1);
            self.layouth10.addWidget(self.steam_controller_bool_label);
            self.layouth10.addWidget(self.steam_controller_bool);
            self.layoutv1.addLayout(self.layouth10);

            self.layouth11 = QtWidgets.QHBoxLayout();
            self.usb_sharing_label = QtWidgets.QLabel("usb shring an aus schalten!: ");
            self.usb_sharing = QtWidgets.QSpinBox();
            self.usb_sharing.setValue(usb_sharing);
            self.usb_sharing.setMinimum(0);
            self.usb_sharing.setMaximum(1);
            self.layouth11.addWidget(self.usb_sharing_label);
            self.layouth11.addWidget(self.usb_sharing);
            self.layoutv1.addLayout(self.layouth11);

            self.layouth12 = QtWidgets.QHBoxLayout();
            self.usb_name_label = QtWidgets.QLabel("usb gerät per usb name in docker hinzufügen (mehere device getrennt mit ^): ");
            self.usb_name = QtWidgets.QLineEdit(usb_name);
            self.usb_name_combobox = QtWidgets.QComboBox();
            self.usb_name_combobox_add = QtWidgets.QPushButton("add")
            self.usb_name_combobox_add .clicked.connect(self.add_combox_usb_share)
            self.usb_name_combobox_update = QtWidgets.QPushButton("update")
            self.usb_name_combobox_update .clicked.connect(self.update_usb_share_combox)
            self.layouth12.addWidget(self.usb_name_label);
            self.layouth12.addWidget(self.usb_name);
            self.layouth12.addWidget(self.usb_name_combobox);
            self.layouth12.addWidget(self.usb_name_combobox_add);
            self.layouth12.addWidget(self.usb_name_combobox_update);
            self.layoutv1.addLayout(self.layouth12);



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

            self.layouth14 = QtWidgets.QHBoxLayout();
            self.docker_build_label = QtWidgets.QLabel("docker contaienr name: ");
            self.docker_build = QtWidgets.QLineEdit(docker_build);
            self.layouth14.addWidget(self.docker_build_label);
            self.layouth14.addWidget(self.docker_build);
            self.layoutv1.addLayout(self.layouth14);

            self.layouth15 = QtWidgets.QHBoxLayout();
            self.maxmemory_label = QtWidgets.QLabel("Mazialer zugelassener RAN verbauch (-1 == keine Beschrnäkung): ");
            self.maxmemory = QtWidgets.QSpinBox();
            self.maxmemory.setMinimum(-1);
            self.maxmemory.setMaximum(2147483647);
            self.maxmemory.setValue(maxmemory);
            self.layouth15.addWidget(self.maxmemory_label);
            self.layouth15.addWidget(self.maxmemory);
            self.layoutv1.addLayout(self.layouth15);

            self.layouth16 = QtWidgets.QHBoxLayout();
            self.maxcpus_label = QtWidgets.QLabel("Wie viele CPUS darf der docker container nutzen (-1 == keine Beschrnäkung): ");
            self.maxcpus = QtWidgets.QSpinBox();
            self.maxcpus.setMinimum(-1);
            self.maxcpus.setMaximum(2147483647);
            self.maxcpus.setValue(maxcpus);
            self.layouth16.addWidget(self.maxcpus_label);
            self.layouth16.addWidget(self.maxcpus);
            self.layoutv1.addLayout(self.layouth16);

            self.layouth17 = QtWidgets.QHBoxLayout();
            self.network_host_label = QtWidgets.QLabel("network_host gib eine netwerk geräte per name an oder lass lerr für default network bridge: ");
            self.network_host = QtWidgets.QLineEdit(network_host);
            self.layouth17.addWidget(self.network_host_label);
            self.layouth17.addWidget(self.network_host);
            self.layoutv1.addLayout(self.layouth17);

            self.layouth18 = QtWidgets.QHBoxLayout();
            self.portforwding_label = QtWidgets.QLabel("portforwding  zum beispiel \"1000:1000\" für prot 1000 weiterleitung:  ");
            self.portforwding = QtWidgets.QLineEdit(portforwding);
            self.layouth18.addWidget(self.portforwding_label);
            self.layouth18.addWidget(self.portforwding);
            self.layoutv1.addLayout(self.layouth18);

            self.layouth19 = QtWidgets.QHBoxLayout();
            self.dbus_rw_label = QtWidgets.QLabel("dbus_rw 0 = disabel , 1= enable: ");
            self.dbus_rw = QtWidgets.QSpinBox();
            self.dbus_rw.setValue(dbus_rw);
            self.dbus_rw.setMinimum(0);
            self.dbus_rw.setMaximum(1);
            self.layouth19.addWidget(self.dbus_rw_label);
            self.layouth19.addWidget(self.dbus_rw);
            self.layoutv1.addLayout(self.layouth19);

            self.layouth20 = QtWidgets.QHBoxLayout();
            self.pacman_cache_label = QtWidgets.QLabel("pacman_cache setze hier ein path zu einem Ordner an wo der packet cache von pacman gesichert wird: ");
            self.pacman_cache = QtWidgets.QLineEdit(pacman_cache);
            self.pacman_cache_browse = QtWidgets.QPushButton("browse..")
            self.pacman_cache_browse .clicked.connect(self.set_pacman_cache_folder)
            self.layouth20.addWidget(self.pacman_cache_label);
            self.layouth20.addWidget(self.pacman_cache);
            self.layouth20.addWidget(self.pacman_cache_browse);
            self.layoutv1.addLayout(self.layouth20);

            self.layouth21 = QtWidgets.QHBoxLayout();
            self.dns_label = QtWidgets.QLabel("ip addres eines custom DNS server: ");
            self.dns = QtWidgets.QLineEdit(dns);
            self.layouth21.addWidget(self.dns_label);
            self.layouth21.addWidget(self.dns);
            self.layoutv1.addLayout(self.layouth21);

            self.layouth22 = QtWidgets.QHBoxLayout();
            self.ipv4_label = QtWidgets.QLabel("Static ipv4 : ");
            self.ipv4 = QtWidgets.QLineEdit(ipv4);
            self.layouth22.addWidget(self.ipv4_label);
            self.layouth22.addWidget(self.ipv4);
            self.layoutv1.addLayout(self.layouth22);

            self.layouth23 = QtWidgets.QHBoxLayout();
            self.wireguard_fix_label = QtWidgets.QLabel("wiregaurd fix 0 = disabel , 1= enable: ");
            self.wireguard_fix = QtWidgets.QSpinBox();
            self.wireguard_fix.setValue(wireguard_fix);
            self.wireguard_fix.setMinimum(0);
            self.wireguard_fix.setMaximum(1);
            self.layouth23.addWidget(self.wireguard_fix_label);
            self.layouth23.addWidget(self.wireguard_fix);
            self.layoutv1.addLayout(self.layouth23);

            self.layouth24 = QtWidgets.QHBoxLayout();
            self.nosudo_label = QtWidgets.QLabel("nosudo 0 = disabel , 1= enable: ");
            self.nosudo = QtWidgets.QSpinBox();
            self.nosudo.setValue(nosudo);
            self.nosudo.setMinimum(0);
            self.nosudo.setMaximum(1);
            self.layouth24.addWidget(self.nosudo_label);
            self.layouth24.addWidget(self.nosudo);
            self.layoutv1.addLayout(self.layouth24);

            self.layouth25 = QtWidgets.QHBoxLayout();
            self.run_in_background_label = QtWidgets.QLabel("run_in_background 0 = disabel , 1= enable: ");
            self.run_in_background = QtWidgets.QSpinBox();
            self.run_in_background.setValue(run_in_background);
            self.run_in_background.setMinimum(0);
            self.run_in_background.setMaximum(1);
            self.layouth25.addWidget(self.run_in_background_label);
            self.layouth25.addWidget(self.run_in_background);
            self.layoutv1.addLayout(self.layouth25);

            self.layouth26 = QtWidgets.QHBoxLayout();
            self.ttyon_label = QtWidgets.QLabel("ttyon 0 = disabel , 1= enable, 2=docker checkpoint mdoe on: ");
            self.ttyon = QtWidgets.QSpinBox();
            self.ttyon.setValue(ttyon);
            self.ttyon.setMinimum(0);
            self.ttyon.setMaximum(2);
            self.layouth26.addWidget(self.ttyon_label);
            self.layouth26.addWidget(self.ttyon);
            self.layoutv1.addLayout(self.layouth26);

            self.layouth27 = QtWidgets.QHBoxLayout();
            self.pacman_pakgage_install_label = QtWidgets.QLabel("pacman install pakage: ");
            self.pacman_pakgage_install = QtWidgets.QLineEdit(pacman_pakgage_install);
            self.layouth27.addWidget(self.pacman_pakgage_install_label);
            self.layouth27.addWidget(self.pacman_pakgage_install);
            self.layoutv1.addLayout(self.layouth27);

            self.layouth28 = QtWidgets.QHBoxLayout();
            self.docker_input_label = QtWidgets.QLabel("docker input: ");
            self.docker_input = QtWidgets.QLineEdit(docker_input);
            self.layouth28.addWidget(self.docker_input_label);
            self.layouth28.addWidget(self.docker_input);
            self.layoutv1.addLayout(self.layouth28);

            self.layouth27 = QtWidgets.QHBoxLayout();
            self.bluethoot_passthrough_label = QtWidgets.QLabel("Bluethoot_passthrough  0 = disabel , 1= enable ");
            self.bluethoot_passthrough = QtWidgets.QSpinBox();
            self.bluethoot_passthrough.setValue(bluethoot_passthrough);
            self.bluethoot_passthrough.setMinimum(0);
            self.bluethoot_passthrough.setMaximum(1);
            self.layouth27.addWidget(self.bluethoot_passthrough_label);
            self.layouth27.addWidget(self.bluethoot_passthrough);
            self.layoutv1.addLayout(self.layouth27);

            self.layouth28 = QtWidgets.QHBoxLayout();
            self.hidraw_acs_overrides_patch_label = QtWidgets.QLabel("USB Hidraw acs overrides patch (alow docker user readwrite Hidraw devices) 0 = disabel , 1= enable ");
            self.hidraw_acs_overrides_patch = QtWidgets.QSpinBox();
            self.hidraw_acs_overrides_patch.setValue(hidraw_acs_overrides_patch);
            self.hidraw_acs_overrides_patch.setMinimum(0);
            self.hidraw_acs_overrides_patch.setMaximum(1);
            self.layouth28.addWidget(self.hidraw_acs_overrides_patch_label);
            self.layouth28.addWidget(self.hidraw_acs_overrides_patch);
            self.layoutv1.addLayout(self.layouth28);


            self.layouth29 = QtWidgets.QHBoxLayout();
            self.ipv6_privacy_label = QtWidgets.QLabel("ipv6_privacy mode (ramdon mac addr in ipv6 adress) 0 = disabel , 1= enable 2=all devies patch on Server: ");
            self.ipv6_privacy1 = QtWidgets.QSpinBox();
            self.ipv6_privacy1.setValue(ipv6_privacy);
            self.ipv6_privacy1.setMinimum(0);
            self.ipv6_privacy1.setMaximum(2);
            self.layouth29.addWidget(self.ipv6_privacy_label);
            self.layouth29.addWidget(self.ipv6_privacy1);
            self.layoutv1.addLayout(self.layouth29);

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

            self.layouth31 = QtWidgets.QHBoxLayout();
            self.wine_32bit_speed_hak_label = QtWidgets.QLabel("wine_32bit_speed_hak, lol speed hak (sysctl -w abi.vsyscall32=0) 0 = disabel , 1= enable: ");
            self.wine_32bit_speed_hak = QtWidgets.QSpinBox();
            self.wine_32bit_speed_hak.setValue(wine_32bit_speed_hak);
            self.wine_32bit_speed_hak.setMinimum(0);
            self.wine_32bit_speed_hak.setMaximum(1);
            self.layouth31.addWidget(self.wine_32bit_speed_hak_label);
            self.layouth31.addWidget(self.wine_32bit_speed_hak);
            self.layoutv1.addLayout(self.layouth31);

            self.layouth32 = QtWidgets.QHBoxLayout();
            self.read_only_label = QtWidgets.QLabel("Beabeitungschutz 0 = disabel , 1= enable: ");
            self.read_only = QtWidgets.QSpinBox();
            if(read_only != ""):
                self.read_only.setValue(1);
            else:
                self.read_only.setValue(0);
            self.read_only.setMinimum(0);
            self.read_only.setMaximum(1);
            self.layouth32.addWidget(self.read_only_label);
            self.layouth32.addWidget(self.read_only);
            self.layoutv1.addLayout(self.layouth32);

            self.layouth33 = QtWidgets.QHBoxLayout();
            self.read_only_password_label = QtWidgets.QLabel("Beabeitungschutz muss auf 1 stehe und hiere das Beabeitungschutz password");
            self.read_only_password = QtWidgets.QLineEdit(read_only_password);
            self.read_only_password_clear_ = QtWidgets.QPushButton("clear and disable")
            self.read_only_password_clear_ .clicked.connect(self.read_only_password_clear)
            self.layouth33.addWidget(self.read_only_password_label);
            self.layouth33.addWidget(self.read_only_password);
            self.layouth33.addWidget(self.read_only_password_clear_);
            self.layoutv1.addLayout(self.layouth33);


            self.layouth99999999999 = QtWidgets.QHBoxLayout();
            self.button_save = QtWidgets.QPushButton("Save json")
            self.button_save .clicked.connect(self.save)
            self.layouth99999999999.addWidget(self.button_save);
            self.layoutv1.addLayout(self.layouth99999999999);

            self.update_usb_share_combox();
            self.update_hidware_share_combox();
            self.update_gpu_render_combox();
            #self.showFullScreen();
            self.showMaximized();
            self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, self.w, self.h))
        def save(self):
            docker_user = self.docker_user.text();
            gpu_render = str(self.gpu_render.value());
            disk_device_name = self.disk_device_name.text();
            zugriff_auf_media = str(self.zugriff_auf_media.value());
            sav_home_docker_folder = str(self.sav_home_docker_folder.value());
            share_folder_daten = str(self.share_folder_daten.value());
            share_folder1_aktiv = str(self.share_folder1_aktiv.value());
            share_folder1 = self.share_folder1.text();
            network_disable = str(self.network_disable.value());
            steam_controller_bool = str(self.steam_controller_bool.value());
            usb_sharing = str(self.usb_sharing.value());
            usb_name = self.usb_name.text();
            usb_hidraw_name = self.usb_hidraw_name.text();
            docker_build = self.docker_build.text();
            maxmemory = str(self.maxmemory.value())
            maxcpus = str(self.maxcpus.value())
            network_host = self.network_host.text();
            portforwding =  self.portforwding.text();
            dbus_rw =  str(self.dbus_rw.value());
            pacman_cache = self.pacman_cache.text();
            dns = self.dns.text();
            ipv4 = self.ipv4.text();
            wireguard_fix = str(self.wireguard_fix.value());
            nosudo = str(self.nosudo.value());
            run_in_background = str(self.run_in_background.value());
            ttyon = str(self.ttyon.value());
            pacman_pakgage_install = self.pacman_pakgage_install.text();
            docker_input = self.docker_input.text();
            bluethoot_passthrough = str(self.bluethoot_passthrough.value());
            hidraw_acs_overrides_patch = str(self.hidraw_acs_overrides_patch.value());
            ipv6_privacy = str(self.ipv6_privacy1.value());
            faketime = self.faketime.text();
            wine_32bit_speed_hak = str(self.wine_32bit_speed_hak.value());
            read_only = str(self.read_only.value());
            read_only_password = self.read_only_password.text();
            #file_write_json(dirname + "/config_file_json", docker_user, gpu_render, disk_device_name, zugriff_auf_media, sav_home_docker_folder, share_folder_daten,
            #                share_folder1_aktiv, share_folder1, network_disable, steam_controller_bool, usb_sharing, usb_name, usb_hidraw_name,
            #                docker_build, maxmemory, maxcpus, network_host, portforwding, dbus_rw, pacman_cache, dns, ipv4, wireguard_fix,
            #                 nosudo, run_in_background, ttyon, pacman_pakgage_install, docker_input);
            file_write_json(dirname + "/config_file_json", docker_user, gpu_render, disk_device_name, zugriff_auf_media, sav_home_docker_folder, share_folder_daten, share_folder1_aktiv, share_folder1, network_disable, steam_controller_bool, usb_sharing, usb_name, usb_hidraw_name, docker_build, maxmemory, maxcpus, network_host, portforwding, dbus_rw, pacman_cache, dns, ipv4, wireguard_fix, nosudo, run_in_background, ttyon, pacman_pakgage_install, docker_input, bluethoot_passthrough, hidraw_acs_overrides_patch, ipv6_privacy, faketime, wine_32bit_speed_hak, read_only, read_only_password);
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
            self.gpu_render_array = read_all_dri_prime_device();
            self.gpu_render_combobox.clear()
            self.gpu_render_combobox.addItems(self.gpu_render_array)
            self.gpu_render_combobox.update()
            self.gpu_render_combobox.setEnabled(True)
            return 0;

        def set_combox_gpu_render(self):
            index = self.gpu_render_combobox.currentIndex()
            self.gpu_render.setValue(index);
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
                self.share_folder1_aktiv.setValue(0);
            else:
                self.share_folder1_aktiv.setValue(1);
            return 0;







    mainwindow = seb_sync_clinet_gui()
    mainwindow.show()
    app.exec_()
    exit();
