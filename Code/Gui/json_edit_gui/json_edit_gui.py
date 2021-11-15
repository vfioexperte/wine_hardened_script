#!/usr/bin/env python
#Copyright (C) 2021  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#this is a fork from https://github.com/kritzsie/steam-on-docker

version = "0.2b"

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

def start_json_edit_gui(dirname, docker_user, gpu_render, disk_device_name, zugriff_auf_media, sav_home_docker_folder, share_folder_daten,
                    share_folder1_aktiv, share_folder1, network_disable, steam_controller_bool, usb_sharing, usb_name, usb_hidraw_name,
                    docker_build, docker_input, maxmemory, maxcpus, network_host, portforwding, dbus_rw, pacman_cache, dns, ipv4,
                    wireguard_fix, nosudo, run_in_background, ttyon, pacman_pakgage_install):
    from PyQt5 import QtWidgets
    from PyQt5 import QtGui
    app = QtWidgets.QApplication(sys.argv);
    class seb_sync_clinet_gui(QtWidgets.QWidget):
        def __init__(self):
            QtWidgets.QWidget.__init__(self)

            self.statusbar = QtWidgets.QStatusBar()
            self.statusbar.showMessage("test")
            self.title = appname + " - " + version
            self.setWindowTitle(self.title)
            self.resize(1920, 1080)

            self.layoutv1 = QtWidgets.QVBoxLayout(self)

            self.layouth1 = QtWidgets.QHBoxLayout()
            self.docker_user_label = QtWidgets.QLabel("docker_user:");
            self.docker_user = QtWidgets.QLineEdit(docker_user);
            self.layouth1.addWidget(self.docker_user_label);
            self.layouth1.addWidget(self.docker_user);
            self.layoutv1.addLayout(self.layouth1);

            self.layouth2 = QtWidgets.QHBoxLayout()
            self.gpu_render_label =  QtWidgets.QLabel("gpu_render: (nur für muti gpu user um bei opengl eine gpu zu wählen! bei 1ner gpubiit 0 lassen )");
            self.gpu_render = QtWidgets.QSpinBox();
            self.gpu_render.setMinimum(0);
            self.gpu_render.setValue(int(gpu_render));
            self.layouth2.addWidget(self.gpu_render_label);
            self.layouth2.addWidget(self.gpu_render);
            self.layoutv1.addLayout(self.layouth2);

            self.layouth3 = QtWidgets.QHBoxLayout();
            self.disk_device_name_label = QtWidgets.QLabel("Standard Eisntellugn \"cd/dvd\" alle cd rom laufwerke werden in den docker container übernomen")
            self.disk_device_name = QtWidgets.QLineEdit(disk_device_name);
            self.layouth3.addWidget(self.disk_device_name_label);
            self.layouth3.addWidget(self.disk_device_name);
            self.layoutv1.addLayout(self.layouth3);

            self.layouth4 = QtWidgets.QHBoxLayout();
            self.zugriff_auf_media_label = QtWidgets.QLabel("docker verzeich frei gabe von /run/media 1=on, 0=off")
            self.zugriff_auf_media = QtWidgets.QSpinBox();
            self.zugriff_auf_media.setMinimum(0);
            self.zugriff_auf_media.setMaximum(1);
            self.zugriff_auf_media.setValue(zugriff_auf_media);
            self.layouth4.addWidget(self.zugriff_auf_media_label);
            self.layouth4.addWidget(self.zugriff_auf_media);
            self.layoutv1.addLayout(self.layouth4);

            self.layouth5 = QtWidgets.QHBoxLayout();
            self.sav_home_docker_folder_label = QtWidgets.QLabel("docker verzeich frei gabe von home Ordner 1=on, 0=off")
            self.sav_home_docker_folder = QtWidgets.QSpinBox();
            self.sav_home_docker_folder.setMinimum(0);
            self.sav_home_docker_folder.setMaximum(1);
            self.sav_home_docker_folder.setValue(sav_home_docker_folder);
            self.layouth5.addWidget(self.sav_home_docker_folder_label);
            self.layouth5.addWidget(self.sav_home_docker_folder);
            self.layoutv1.addLayout(self.layouth5);

            self.layouth6 = QtWidgets.QHBoxLayout();
            self.share_folder_daten_label = QtWidgets.QLabel("docker verzeich frei gabe von sahre fodler daten im home folder Ordner 1=on, 0=off")
            self.share_folder_daten = QtWidgets.QSpinBox();
            self.share_folder_daten.setMinimum(0);
            self.share_folder_daten.setMaximum(1);
            self.share_folder_daten.setValue(share_folder_daten);
            self.layouth6.addWidget(self.share_folder_daten_label);
            self.layouth6.addWidget(self.share_folder_daten);
            self.layoutv1.addLayout(self.layouth6);

            self.layouth7 = QtWidgets.QHBoxLayout();
            self.share_folder1_aktiv_label = QtWidgets.QLabel("docker verzeich frei gabe von eigner share fodler akriviren 1=on, 0=off")
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
            self.layouth8.addWidget(self.share_folder1_label);
            self.layouth8.addWidget(self.share_folder1);
            self.layoutv1.addLayout(self.layouth8);

            self.layouth9 = QtWidgets.QHBoxLayout();
            self.network_disable_label = QtWidgets.QLabel("Netzwerk interface deaktiren #0=netwtzwwerk aktive #1=netwerk desaktivirt");
            self.network_disable = QtWidgets.QSpinBox();
            self.network_disable.setValue(network_disable);
            self.network_disable.setMinimum(0);
            self.network_disable.setMaximum(1);
            self.layouth9.addWidget(self.network_disable_label);
            self.layouth9.addWidget(self.network_disable);
            self.layoutv1.addLayout(self.layouth9);

            self.layouth10 = QtWidgets.QHBoxLayout();
            self.steam_controller_bool_label = QtWidgets.QLabel("Steam controller in docker conitern nutzen #1= akriv");
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
            self.layouth12.addWidget(self.usb_name_label);
            self.layouth12.addWidget(self.usb_name);
            self.layoutv1.addLayout(self.layouth12);

            self.layouth13 = QtWidgets.QHBoxLayout();
            self.usb_hidraw_name_label = QtWidgets.QLabel("usb gerät per usb hdiraw name in docker hinzufügen (mehere device getrennt mit ^): ");
            self.usb_hidraw_name = QtWidgets.QLineEdit(usb_hidraw_name);
            self.layouth13.addWidget(self.usb_hidraw_name_label);
            self.layouth13.addWidget(self.usb_hidraw_name);
            self.layoutv1.addLayout(self.layouth13);

            self.layouth14 = QtWidgets.QHBoxLayout();
            self.docker_build_label = QtWidgets.QLabel("docker contaienr name: ");
            self.docker_build = QtWidgets.QLineEdit(docker_build);
            self.layouth14.addWidget(self.docker_build_label);
            self.layouth14.addWidget(self.docker_build);
            self.layoutv1.addLayout(self.layouth14);

            self.layouth15 = QtWidgets.QHBoxLayout();
            self.maxmemory_label = QtWidgets.QLabel("Mazialer zugelassener RAN verbauch (-1 == keine beschrnäkung): ");
            self.maxmemory = QtWidgets.QSpinBox();
            self.maxmemory.setMinimum(-1);
            self.maxmemory.setMaximum(2147483647);
            self.maxmemory.setValue(maxmemory);
            self.layouth15.addWidget(self.maxmemory_label);
            self.layouth15.addWidget(self.maxmemory);
            self.layoutv1.addLayout(self.layouth15);

            self.layouth16 = QtWidgets.QHBoxLayout();
            self.maxcpus_label = QtWidgets.QLabel("Wie ville CPUS darf der docker container nutzen (-1 == keine beschrnäkung): ");
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
            self.layouth20.addWidget(self.pacman_cache_label);
            self.layouth20.addWidget(self.pacman_cache);
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
            self.pacman_pakgage_install_label = QtWidgets.QLabel("pacman install pakage : ");
            self.pacman_pakgage_install = QtWidgets.QLineEdit(pacman_pakgage_install);
            self.layouth27.addWidget(self.pacman_pakgage_install_label);
            self.layouth27.addWidget(self.pacman_pakgage_install);
            self.layoutv1.addLayout(self.layouth27);

            self.layouth28 = QtWidgets.QHBoxLayout();
            self.docker_input_label = QtWidgets.QLabel("docker input : ");
            self.docker_input = QtWidgets.QLineEdit(docker_input);
            self.layouth28.addWidget(self.docker_input_label);
            self.layouth28.addWidget(self.docker_input);
            self.layoutv1.addLayout(self.layouth28);

            self.layouth99999999999 = QtWidgets.QHBoxLayout();
            self.button_save = QtWidgets.QPushButton("Save json")
            self.button_save .clicked.connect(self.save)
            self.layouth99999999999.addWidget(self.button_save);
            self.layoutv1.addLayout(self.layouth99999999999);

        def save(self):
            docker_user = self.docker_user.text();
            gpu_render = str(self.gpu_render.value());
            disk_device_name = self.disk_device_name.text();
            zugriff_auf_media = self.zugriff_auf_media.value();
            sav_home_docker_folder = self.sav_home_docker_folder.value();
            share_folder_daten = self.share_folder_daten.value();
            share_folder1_aktiv = self.share_folder1_aktiv.value();
            share_folder1 = self.share_folder1.text();
            network_disable = self.network_disable.value();
            steam_controller_bool = self.steam_controller_bool.value();
            usb_sharing = self.usb_sharing.value();
            usb_name = self.usb_name.text();
            usb_hidraw_name = self.usb_hidraw_name.text();
            docker_build = self.docker_build.text();
            maxmemory = self.maxmemory.value()
            maxcpus = self.maxcpus.value()
            network_host = self.network_host.text();
            portforwding =  self.portforwding.text();
            dbus_rw =  self.dbus_rw.value();
            pacman_cache = self.pacman_cache.text();
            dns = self.dns.text();
            ipv4 = self.ipv4.text();
            wireguard_fix = self.wireguard_fix.value();
            nosudo = self.nosudo.value();
            run_in_background = self.run_in_background.value();
            ttyon = self.ttyon.value();
            pacman_pakgage_install = self.pacman_pakgage_install.text();
            docker_input = self.docker_input.text();
            #file_write_json(dirname + "/config_file_json", docker_user, gpu_render, disk_device_name, zugriff_auf_media, sav_home_docker_folder, share_folder_daten,
            #                share_folder1_aktiv, share_folder1, network_disable, steam_controller_bool, usb_sharing, usb_name, usb_hidraw_name,
            #                docker_build, maxmemory, maxcpus, network_host, portforwding, dbus_rw, pacman_cache, dns, ipv4, wireguard_fix,
            #                 nosudo, run_in_background, ttyon, pacman_pakgage_install, docker_input);
            file_write_json(dirname + "/config_file_json", docker_user, gpu_render, disk_device_name, zugriff_auf_media, sav_home_docker_folder, share_folder_daten, share_folder1_aktiv, share_folder1, network_disable, steam_controller_bool, usb_sharing, usb_name, usb_hidraw_name, docker_build, maxmemory, maxcpus, network_host, portforwding, dbus_rw, pacman_cache, dns, ipv4, wireguard_fix, nosudo, run_in_background, ttyon, pacman_pakgage_install, docker_input);

    mainwindow = seb_sync_clinet_gui()
    mainwindow.show()
    app.exec_()
    exit();
