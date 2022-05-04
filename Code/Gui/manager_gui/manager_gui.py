#!/usr/bin/env python
#Copyright (C) 2022  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#this is a fork from https://github.com/kritzsie/steam-on-docker
#start file 26.03.2022
#last edit 09.04.2022

version_manager_gui = "0.1b"
#0.1b create a new vm
#0.1a gui work 0.1a

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
appname = "Docker build Manager gui"

abspath = os.path.abspath(sys.argv[0])
basename = os.path.basename(abspath)
dirname = os.path.dirname(abspath)
appname_build = "vfio_experte_docker_contianer_gaming_app"
home = "";
home = os.environ['HOME'];
home_fodler_daten = os.path.join(home, "." + appname_build);
dxvk_config_sam_on = os.path.join(home_fodler_daten, "dxvk_sam_on.conf");
dxvk_config_pulse = os.path.join(home_fodler_daten, "pulse-client.conf");
dxvk_config_chmod = os.path.join(home_fodler_daten, "chmod_check.py");
dxvk_config_hidraw = os.path.join(home_fodler_daten, "hidraw_acs_overrides_patch.py");
config_file = os.path.join(dirname, ".config");
config_file_json = os.path.join(dirname, "config_file_json");
build = os.path.join(dirname, "build");


def manager_gui_set_veriable(home_, home_fodler_daten_, dxvk_config_sam_on_, dxvk_config_pulse_, dxvk_config_chmod_, dxvk_config_hidraw_, config_file_, config_file_json_):
    home = home_;
    home_fodler_daten = home_fodler_daten_;
    dxvk_config_sam_on = dxvk_config_sam_on_;
    dxvk_config_pulse = dxvk_config_pulse_;
    dxvk_config_chmod = dxvk_config_chmod_;
    dxvk_config_hidraw = dxvk_config_hidraw_;
    config_file = config_file_;
    config_file_json = config_file_json_;
    return 0;


def cmd_start(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True).decode().split("\n")
        return out
    except subprocess.CalledProcessError:
        return []


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

def start_manager_gui(vms_folder):
    from PyQt5 import QtWidgets
    from PyQt5 import QtGui
    from PyQt5 import QtCore
    import time
    import datetime
    app = QtWidgets.QApplication(sys.argv);
    class manager_gui(QtWidgets.QWidget):
        def __init__(self):
            QtWidgets.QWidget.__init__(self)

            self.statusbar = QtWidgets.QStatusBar()
            self.statusbar.showMessage("test")
            self.title = appname + " - " + version_manager_gui
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

            self.layoutv1 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
            self.layoutv1.addLayout(self.layoutv1)

            self.layouth1 = QtWidgets.QHBoxLayout()

            self.layouth2 = QtWidgets.QHBoxLayout();
            self.vms_combobox = QtWidgets.QComboBox();
            self.vms_combobox. currentIndexChanged.connect(self.update_vm_comboox_commands_cahcnge);
            self.vms_combobox_command_label = QtWidgets.QLabel("run as")
            self.vms_combobox_command = QtWidgets.QComboBox();
            self.vms_combobox_command_Start = QtWidgets.QPushButton("start")
            self.vms_combobox_command_Start .clicked.connect(self.start_button_combobox)
            self.layouth2.addWidget(self.vms_combobox);
            self.layouth2.addWidget(self.vms_combobox_command_label);
            self.layouth2.addWidget(self.vms_combobox_command);
            self.layouth2.addWidget(self.vms_combobox_command_Start);
            self.layoutv1.addLayout(self.layouth2);

            self.layouth3 = QtWidgets.QHBoxLayout();
            self.create_a_new_vm_button = QtWidgets.QPushButton("create a new vm")
            self.create_a_new_vm_button .clicked.connect(self.create_a_new_vm)
            self.layouth3.addWidget(self.create_a_new_vm_button);
            self.layoutv1.addLayout(self.layouth3);

            self.vms_folder = vms_folder;
            if(self.vms_folder[len(self.vms_folder) -1] != "/"):
                self.vms_folder_with_slash = self.vms_folder + "/";
            self.vms_array_command = [];

            #os.access('my_file', os.X_OK)
            #self.showFullScreen();
            self.showMaximized();
            self.update_vms_combobox();
            self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, self.w, self.h))


        def update_vms_combobox(self):
            self.vms_array = read_all_vm_in_folder(self.vms_folder);
            self.vms_combobox.clear()
            self.vms_combobox.addItems(self.vms_array)
            self.vms_combobox.update()
            self.vms_combobox.setEnabled(True)
            self.vms_array_command = [];
            for tmp in self.vms_array:
                s2 = self.vms_folder_with_slash + tmp;
                self.vms_array_command.append(read_all_vm_in_command(s2))
            self.update_vms_combobox_commands(0);
            return 0;

        def update_vms_combobox_commands(self, arrrayid):
            if(len(self.vms_array_command) != 0):
                self.vms_array_command_id_array = self.vms_array_command[arrrayid];
                self.vms_combobox_command.clear()
                self.vms_combobox_command.addItems(self.vms_array_command_id_array)
                self.vms_combobox_command.update()
                self.vms_combobox_command.setEnabled(True)
            return 0;

        def update_vm_comboox_commands_cahcnge(self):
            index = self.vms_combobox.currentIndex()
            #s1 = self.vms_array[index];
            self.update_vms_combobox_commands(index);
            return 0;

        def login_combox_vms(self):
            index = self.vms_combobox.currentIndex()
            s1 = self.vms_array[index];
            s2 = self.vms_folder + s1;
            self.wirte_command_to_file("cd \"" + s2 + "\" && ./login");
            os.system("xfce4-terminal --execute '/tmp/docker_build_Manger_run_termianl_tmp.bash'")
            return 0;

        def login_root_combox_vms(self):
            index = self.vms_combobox.currentIndex()
            s1 = self.vms_array[index];
            s2 = self.vms_folder + s1;
            self.wirte_command_to_file("cd \"" + s2 + "\" && ./login_root");
            os.system("xfce4-terminal --execute '/tmp/docker_build_Manger_run_termianl_tmp.bash'")
            return 0;

        def edit_config_combox_vms(self):
            index = self.vms_combobox.currentIndex()
            s1 = self.vms_array[index];
            s2 = self.vms_folder + s1;
            self.wirte_command_to_file("cd \"" + s2 + "\" && ./edit_config");
            os.system("xfce4-terminal --execute '/tmp/docker_build_Manger_run_termianl_tmp.bash'")
            return 0;

        def start_button_combobox(self):
            index = self.vms_combobox.currentIndex()
            s1 = self.vms_array[index];
            s2 = self.vms_folder_with_slash + s1;
            index2 = self.vms_combobox_command.currentIndex()
            s3 = self.vms_array_command_id_array[index2];
            if(s3 == "edit_config"):
                os.system("cd \"" + s2 + "\" && ./" + s3);
            else:
                self.wirte_command_to_file("cd \"" + s2 + "\" && ./" + s3);
                os.system("xfce4-terminal --execute '/tmp/docker_build_Manger_run_termianl_tmp.bash'")
            return 0;

        def wirte_command_to_file(self, cmd):
            f1 = open("/tmp/docker_build_Manger_run_termianl_tmp.bash", "w");
            f1.write("!/bin/bash\n");
            f1.write(cmd);
            f1.close();
            os.system("chmod +x /tmp/docker_build_Manger_run_termianl_tmp.bash");
            return 0;

        def create_a_new_vm(self):
            while True:
                new_vm_name = self.question_vm_new_name();
                if(new_vm_name != ""):
                    s2 = self.vms_folder_with_slash + new_vm_name;
                    if(os.path.isdir(s2) == True):
                        self.messagebox_start("ERROR VM folder exist!");
                        continue;
                    self.create_a_new_vm_per_path(s2);
                    self.update_vms_combobox();
                    return 0;
                else:
                    return 0;

        def question_vm_new_name(self):
            text, okPressed = QtWidgets.QInputDialog.getText(self, "Get text", "new vm name please \"\" is exit: ", QtWidgets.QLineEdit.Normal, "");
            if(okPressed and text != ""):
                return text;
            else:
                return "";

        def messagebox_start(self, test):
            msgBox2 = QtWidgets.QMessageBox();
            msgBox2.setText(test);
            msgBox2.exec();
            return 0;

        def create_a_new_vm_per_path(self, path):
            s2 = path;
            os.system("mkdir -p \"" + s2 + "\"");
            os.system("cp \"" + dxvk_config_sam_on + "\" \"" + s2 + "/" + "dxvk_sam_on.conf\"")
            os.system("cp \"" + dxvk_config_chmod + "\" \"" + s2 + "/chmod_check.py\"")
            os.system("cp \"" + dxvk_config_pulse + "\" \"" + s2 + "/pulse-client.conf\"")
            os.system("cp \"" + dxvk_config_hidraw + "\" \"" + s2 + "/hidraw_acs_overrides_patch.py\"")
            os.system("cp \"" + config_file_json + "\" \"" + s2 + "/config_file_json\"")
            os.system("ln -sf \"" + build + "\" \"" + s2 + "/build\"");
            os.system("cd \"" + path + "\" && ln -sf build " + "edit_config");
            os.system("cd \"" + path + "\" && ./edit_config");
            return 0;











    mainwindow = manager_gui()
    mainwindow.show()
    app.exec_()
    exit();
