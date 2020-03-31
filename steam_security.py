#!/usr/bin/env python3.8
#Copyright (C) 2020  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#Warnung der Programmierer hafte nicht auf Schäden oder auf unsachgemäßen Umgang der APP
version = "0.1b"
print(version);

from PyQt5 import QtWidgets
from PyQt5 import QtGui
import sys
import os
import os.path
import platform

script_path = "/usr/bin/wine_security_gui";

steammode = 0;
steamauto = 0;
steamall = 0;
debug_fodler = "";
if(len(sys.argv) == 2):
    if(sys.argv[1] == "-version"):
        exit();
    elif(sys.argv[1] == "--help" or sys.argv[1] == "-h"):
        print("");
        exit();

def system(cmd):
    os.system(cmd);
    return 0;

home = "";
def read_WINEPREFIX():
    WINEPREFIX = "";
    if(debug_fodler != ""):
        WINEPREFIX = debug_fodler;
        os.system("mkdir -p \"" + debug_fodler + "/dosdevices" + "\"");
        return debug_fodler;
    try:
        WINEPREFIX = os.environ['WINEPREFIX'];
    except KeyError:
        home = os.environ['HOME'];
        WINEPREFIX = home + "/.wine";
    return WINEPREFIX;

class Wine_hardened_script_gui(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.title = "steam_security - " + version;
        self.setWindowTitle(self.title);
        self.WINEPREFIX = read_WINEPREFIX();
        self.block_device = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z";
        self.DEVICES = self.block_device.split(",");
        self.block_output_folder = "/tmp";
        self.device_overide = "";
        self.winefodler = self.WINEPREFIX + "/dosdevices"
        self.config = self.winefodler + "/.hardened.config";
        self.device_overide = "";
        self.mode = 0;

        self.layoutv1 = QtWidgets.QVBoxLayout(self)
        self.layouth1 = QtWidgets.QHBoxLayout()
        self.qlabel_wineprefix = QtWidgets.QLabel("Steam games:");
        self.combobox = QtWidgets.QComboBox();
        self.combobox.currentIndexChanged.connect(self.change_combobox);
        self.layouth1.addWidget(self.qlabel_wineprefix);
        self.layouth1.addWidget(self.combobox);
        self.layoutv1.addLayout(self.layouth1);
        self.bcolse = False;
	
        self.layouth30 = QtWidgets.QHBoxLayout();
        self.button_hardened = QtWidgets.QPushButton("start protection ");
        self.button_hardened.clicked.connect(self.hardened_start);
        self.button_remove_hardened = QtWidgets.QPushButton("remove protection start");
        self.button_remove_hardened.clicked.connect(self.remove_hardened);
        self.layouth30.addWidget(self.button_hardened);
        self.layouth30.addWidget(self.button_remove_hardened);
        self.layoutv1.addLayout(self.layouth30);

        self.list_all_Proton_games();
    def change_combobox(self):
        return 0;
    def hardened_start(self):
        index = self.combobox.currentIndex();
        print(self.array_name[index]);
        print(self.array_id[index]);
        os.system("protontricks -c \"python3.8 '" + script_path + "' -Steam_auto_protect\" " + self.array_id[index]);
        return 0;
    def remove_hardened(self):
        index = self.combobox.currentIndex();
        print(self.array_name[index]);
        print(self.array_id[index]);
        os.system("protontricks -c \"python3.8 '" + script_path + "' -Steam_auto_remove_protect\" " + self.array_id[index]);
        return 0;
    def closeEvent(self, event):
        self.bcolse = True;
        event.accept();
    def list_all_Proton_games(self):
        os.system("protontricks -s \"*\" | grep \"(\" >/tmp/tmp_wine_hardend_script.tmp");
        file1 = open("/tmp/tmp_wine_hardend_script.tmp", "r");
        file1.seek(0, 2);
        size = file1.tell();
        file1.seek(0, 0);
        s1 = file1.read(size);
        file1.close();
        s2 = s1.split('\n');
        i = 0;
        s4 = [];
        s4_name = [];
        while True:
            if(i >= len(s2)):
                break;
            s3 = s2[i];
            print(s3);
            j = 0;
            bmode = 0;
            s5 = "";
            s5_name = "";
            while True:
                if(j >=len(s3)):
                    break;
                if(s3[j] == '('):
                    bmode = 1;
                elif(bmode == 0):
                    s5_name = s5_name + s3[j];
                elif(bmode == 1 and s3[j] != ')'):
                    s5 = s5 + s3[j];
                elif(bmode == 1 and s3[j] == ')'):
                    s4.append(s5);
                    s4_name.append(s5_name);
                    break;
                j = j + 1;
            i = i +1;

        self.array_name = s4_name;
        self.array_id = s4;
        self.combobox.clear();
        self.combobox.addItems(self.array_name);
        self.combobox.update();
        self.combobox.setEnabled(True);
        os.system("rm -f /tmp/tmp_wine_hardend_script.tmp")
        return 0;

app = QtWidgets.QApplication(sys.argv);
mainwindow = Wine_hardened_script_gui();
mainwindow.show();
app.exec_();

