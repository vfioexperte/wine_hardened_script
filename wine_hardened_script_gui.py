#!/usr/bin/env python3.8
#Copyright (C) 2020  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#Warnung der Programmierer hafte nicht auf Schäden oder auf unsachgemäßen Umgang der APP
version = "0.8e"
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
noerror = 0;
debug_fodler = "";
if(len(sys.argv) == 2 or len(sys.argv) == 3):
    if(sys.argv[1] == "-version"):
        exit();
    if(sys.argv[1] == "-Steam"):
        print("enabled Steam mode");
        print("use this mode only with protontricks command")
        print("you are find the APPID with protontricks -s \"game name\"");
        print("protontricks  -c \"python3.8 '../wine_hardened_script_gui.py' -Steam\" APPID")
        steammode = 1;
    elif(sys.argv[1] == "-Steam_auto_protect"):
        print("enabled Steam auto protect mode");
        print("protontricks  -c \"python3.8 '../wine_hardened_script_gui.py' -Steam_auto_protect\" APPID");
        print("auto protect mode enabled");
        steamauto = 1;
        steammode = 1;
    elif(sys.argv[1] == "-Steam_auto_remove_protect"):
        print("enabled Steam auto remove protect mode");
        print("protontricks  -c \"python3.8 '/wine_hardened_script_gui.py' -Steam_auto_remove_protect\" APPID");
        print("auto remove protect mode enabled");
        steamauto = 2;
        steammode = 1;
    elif(sys.argv[1] == "-Steam_all_auto_protect"):
        steamall = 1;
        steamauto = 1;
        #steammode = 1;
    elif(sys.argv[1] == "-Steam_all_auto_remove_protect"):
        steamall = 1;
        steamauto = 2;
        #steammode = 1;
    if(len(sys.argv) == 3):
        if(sys.argv[2] == "-noerror"):
            print("enable noerror mode");
            noerror = 1;
    elif(sys.argv[1] == "--help" or sys.argv[1] == "-h"):
        print("options:");
        print("");
        print("-Steam");
        print("enabled Steam mode");
        print("use this mode only with protontricks command")
        print("you are find the APPID with protontricks -s \"game name\"");
        print("protontricks  -c \"python3.8 '../wine_hardened_script_gui.py' -Steam\" APPID")
        print("");
        print("-Steam_auto_protect");
        print("enabled Steam auto protect mode");
        print("protontricks  -c \"python3.8 '../wine_hardened_script_gui.py' -Steam_auto_protect\" APPID");
        print("auto protect mode enabled");
        print("");
        print("-Steam_auto_remove_protect");
        print("enabled Steam auto remove protect mode");
        print("protontricks  -c \"python3.8 '/wine_hardened_script_gui.py' -Steam_auto_remove_protect\" APPID");
        print("auto remove protect mode enabled");
        print("");
        print("-Steam_all_auto_protect");
        print("protect all steam games");
        print("");
        print("-Steam_auto_remove_protect");
        print("remove protection all steam games");
        print("-debug");
        print("test debug folder");
        print("-debug /tmp");
        exit();
else:
    if(len(sys.argv) == 3):
        if(sys.argv[1] == "-debug"):
            debug_fodler = sys.argv[2];
            print("enable debug mode");



def popen(cmd, sin):
    pipeout, pipein = pty.openpty();
    print(sin);
    process = subprocess.Popen(cmd,stdin=pipeout, stderr=subprocess.STDOUT);#stdout=pipein
    os.write(pipein, sin.encode());
    os.close(pipeout);
    process.wait();
    return 0;

def system(cmd):
    os.system(cmd);

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

def remnove_hardened(device, winefodler, block_output_folder):
    i = 0;
    while True:
        if(i >= len(device)):
            break;
        s2 = device[i];
        s1 = winefodler + "/" + s2 + ":";
        s3 = s1 + ":";
        system("rm -f \"" + s1 + "\"");
        system("rm -f \"" + s3 + "\"");
        i = i +1;

def add_hardened(device, winefodler, block_output_folder):
    remnove_hardened(device, winefodler, block_output_folder);
    i = 0;
    while True:
        if(i >= len(device)):
            break;
        if(device[i] != ","):
            s2 = device[i];
            s1 = winefodler + "/" + s2 + ":";
            system("ln -sf " + "\"" + block_output_folder + "\" " + "\""  + s1 + "\"");
        i = i +1;

def read_config_file(config):
    if(os.path.isfile(config) == False):
        return -1;
    file1 = open(config, "r");
    file1.seek(0, 2);
    size = file1.tell();
    file1.seek(0, 0);
    b1 = file1.read(size);
    file1.close();
    return b1;

def write_config_file(config, device_overide):
    file1 = open(config, "w");
    file1.write(device_overide)
    file1.close();
    return 0;

def restore_device_z(winefodler):
    s2 = winefodler + "/" + "z" + ":";
    os.system("ln -sf " + "/ " + "\"" + winefodler + "/z:" + "\"");
    return 0;

class Wine_hardened_script_gui(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.title = "Wine_hardened_script_gui - " + version;
        self.setWindowTitle(self.title);
        self.WINEPREFIX = read_WINEPREFIX();
        self.block_device = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z";
        self.DEVICES = self.block_device.split(",");
        self.block_output_folder = "/tmp/wine_security";
        self.device_overide = "";
        self.winefodler = self.WINEPREFIX + "/dosdevices"
        self.config = self.winefodler + "/.hardened.config";
        self.device_overide = "";
        self.mode = 0;

        self.layoutv1 = QtWidgets.QVBoxLayout(self)

        self.layouth1 = QtWidgets.QHBoxLayout()
        self.qlabel_wineprefix = QtWidgets.QLabel("WINEPREFIX:");
        self.textedit_wineprefix = QtWidgets.QTextEdit(self.WINEPREFIX);
        self.button_wineprefix = QtWidgets.QPushButton("browse..");
        self.button_wineprefix.clicked.connect(self.browse_WINEPREFIX);
        self.layouth1.addWidget(self.qlabel_wineprefix);
        self.layouth1.addWidget(self.textedit_wineprefix);
        self.layouth1.addWidget(self.button_wineprefix);
        self.layoutv1.addLayout(self.layouth1);
        self.bcolse = False;
	
        self.qlabel = [];
        self.qlabel_tenner = [];
        self.qlabel_path = [];
        self.qlabel_bool = [];
        self.layouth = [];
        i = 0;
        block_device = self.block_device.split(",");
        while True:
            if(i >= len(block_device)):
                break;
            self.qlabel.append(QtWidgets.QLabel(block_device[i] + ":"));
            self.qlabel_tenner.append(QtWidgets.QLabel("->"));
            self.qlabel_path.append(QtWidgets.QLabel(""));
            self.qlabel_bool.append(QtWidgets.QCheckBox(""));
            self.layouth.append(QtWidgets.QHBoxLayout());
            self.layouth[i].addWidget(self.qlabel[i]);
            self.layouth[i].addWidget(self.qlabel_tenner[i]);
            self.layouth[i].addWidget(self.qlabel_path[i]);
            self.layouth[i].addWidget(self.qlabel_bool[i]);
            if(block_device[i] == "c"):
                self.qlabel_bool[i].setChecked(False);
                self.qlabel_bool[i].setDisabled(True);
                self.qlabel_bool[i].setText("c: disbale");
            if(block_device[i] == "z"):
                self.qlabel_z_dir = QtWidgets.QTextEdit("");
                self.layouth[i].addWidget(self.qlabel_z_dir);
            self.layoutv1.addLayout(self.layouth[i]);
            i = i +1;

        if(steammode == 1):
            self.steammode = steammode;
            self.steamauto = steamauto;

        self.layouth30 = QtWidgets.QHBoxLayout();
        self.button_hardened = QtWidgets.QPushButton("start protection ");
        self.button_hardened.clicked.connect(self.hardened_start);
        self.button_remove_hardened = QtWidgets.QPushButton("remove protection start");
        self.button_remove_hardened.clicked.connect(self.remove_hardened);
        self.layouth30.addWidget(self.button_hardened);
        self.layouth30.addWidget(self.button_remove_hardened);
        self.layoutv1.addLayout(self.layouth30);

        self.textedit_wineprefix.setDisabled(True);
        self.change_WINEPREFIX(self.WINEPREFIX);

        if(steamall == 1):
            self.lsit_all_Proton_games();

    def change_WINEPREFIX(self, wineprefix):
        if(os.path.isdir(wineprefix) == False):
            if(noerror == 0):
                print("WINEPREFIX: " + "\"" + wineprefix + "\" not found!");
                msgBox = QtWidgets.QMessageBox();
                msgBox.setIcon(QtWidgets.QMessageBox.Warning);
                msgBox.setText("WINEPREFIX: " + "\"" + wineprefix + "\" not found!");
                msgBox.exec();
            exit();
        if(steammode != 0):
            if(wineprefix.find("compatdata") == -1 or wineprefix.find("pfx") == -1):
                if(noerror == 0):
                    print("WINEPREFIX: " + "\"" + wineprefix + "\" not a steam wine folder found!\nremove the -Steam options!");
                    msgBox = QtWidgets.QMessageBox();
                    msgBox.setIcon(QtWidgets.QMessageBox.Warning);
                    msgBox.setText("WINEPREFIX: " + "\"" + wineprefix + "\" not a steam wine folder found!\nremove the -Steam options!");
                    msgBox.exec();
                exit();
        self.WINEPREFIX = wineprefix;
        self.winefodler = self.WINEPREFIX + "/dosdevices"
        self.config = self.winefodler + "/.hardened.config";
        if(os.path.isfile(self.config) == True):
            self.mode = 1;
            self.button_hardened.setDisabled(True);
            self.button_remove_hardened.setDisabled(False);
        else:
            self.mode = 0;
            self.button_hardened.setDisabled(False);
            self.button_remove_hardened.setDisabled(True);
        self.change_gui(self.block_device, self.winefodler);
        return 0;

    def change_gui(self, block_device, winefodler):
        self.steamauto = steamauto;
        self.steammode = steammode;
        device = block_device.split(",");
        if(self.mode == 1):
                if(os.path.isfile(self.config) == True):
                    self.device_overide = read_config_file(self.config);
                    self.set_cheboxes(self.device_overide, self.block_device);
                    return 0;
        device_overide = "";
        i = 0;
        while True:
                if(i >= len(device)):
                        break;
                s2 = device[i];
                s1 = winefodler + "/" + s2 + ":";
                if(os.path.islink(s1) == True):
                    device_overide = device_overide + "0" + ",";
                elif(os.path.islink(s1+":") == True):
                    device_overide = device_overide + "0" + ",";
                else:
                    device_overide = device_overide + "1" + ",";

                i = i +1;
        self.set_cheboxes(device_overide, self.block_device);
        return 0;

    def set_cheboxes(self, device_overide, block_device2):
        block_device = block_device2.split(",");
        stext = "";
        self.device_overide = device_overide;
        device_overide = device_overide.split(",");
        if(self.mode == 0):
            stext = "create a protection device ";
        else:
            stext = "remove a protection device ";

        i = 0;
        while True:
            if(i >= len(block_device)):
                break;
            if(block_device[i] != "c" and block_device[i] != "z"):
                if(device_overide[i] == "0" and steammode == 0):
                    self.qlabel_bool[i].setDisabled(False);
                    self.qlabel_bool[i].setText(stext + block_device[i]);
                    self.qlabel_bool[i].setChecked(False);
                else:
                    self.qlabel_bool[i].setDisabled(True);
                    self.qlabel_bool[i].setText(stext + block_device[i]);
                    self.qlabel_bool[i].setChecked(True);
            elif(block_device[i] == "z"):
                if(device_overide[i] == "0" and self.mode == 0):
                    self.qlabel_bool[i].setDisabled(False);
                    self.qlabel_bool[i].setText(stext + block_device[i]);
                    self.qlabel_bool[i].setChecked(False);
                    if(self.steammode == 1):
                        s1  = self.textedit_wineprefix.toPlainText();
                        s1 = os.path.realpath(s1+"../../../../");
                        self.qlabel_z_dir.setText(s1);
                        self.qlabel_bool[i].setText("create a protection device path ->");
                        self.qlabel_z_dir.setHidden(False);
                        self.qlabel_z_dir.setDisabled(False);
                        if(self.steamauto == 1):
                            self.qlabel_bool[i].setChecked(True);
                    else:
                        self.qlabel_z_dir.setHidden(True);
                else:
                    self.qlabel_bool[i].setDisabled(False);
                    self.qlabel_bool[i].setText("resore a protection device " + block_device[i]);
                    self.qlabel_bool[i].setChecked(False);
                    self.qlabel_z_dir.setText("");
                    self.qlabel_z_dir.setDisabled(True);
                    self.qlabel_z_dir.setHidden(True);
                    if(self.steamauto == 2):
                        self.qlabel_bool[i].setChecked(True);
            elif(block_device[i] == "c"):
                self.qlabel_bool[i].setDisabled(True);
                self.qlabel_bool[i].setText(stext + "c");
                self.qlabel_bool[i].setChecked(False);
            i = i +1;
        app.processEvents();
        return 0;




    def calculate1(self):
        block_device = self.block_device.split(",");
        device = "";
        device_overide = "";
        i = 0;
        while True:
            if(i >= len(block_device)):
                break;
            if(self.qlabel_bool[i].isChecked() == True):
                device = device + block_device[i] + ",";
                device_overide = device_overide + "1" + ",";
            else:
                device_overide = device_overide + "0" + ",";

            i = i +1;

        self.device_overide = device_overide;
        return device;

    def hardened_start(self):
        if(os.path.isfile(self.config) == True):
            if(noerror == 0):
                print("ERROR is protect");
                msgBox = QtWidgets.QMessageBox();
                msgBox.setIcon(QtWidgets.QMessageBox.Warning);
                msgBox.setText("ERROR is protect");
                msgBox.exec();
            exit();
        self.DEVICES = self.calculate1();
        remnove_hardened(self.DEVICES, self.winefodler, self.block_output_folder);
        add_hardened(self.DEVICES, self.winefodler, self.block_output_folder);
        write_config_file(self.config, self.device_overide);
        if(self.steammode == 1):
            s1 = self.qlabel_z_dir.toPlainText();
            s2 = self.winefodler + "/" + "z" + ":";
            os.system("rm -f " + "\"" + s2  +  "\"");
            os.system("ln -sf " + s1 + " " + "\"" + s2  +  "\"" );

        self.change_WINEPREFIX(self.WINEPREFIX);
        self.change_gui(self.block_device, self.winefodler);
        return 0;
    def remove_hardened(self):
        if(os.path.isfile(self.config) == False):
            if(noerror == 0):
                print("ERROR is not protect please run protection first");
                msgBox = QtWidgets.QMessageBox();
                msgBox.setIcon(QtWidgets.QMessageBox.Warning);
                msgBox.setText("ERROR is not protect please run protection first");
                msgBox.exec();
            exit();
        self.DEVICES = self.calculate1();
        remnove_hardened(self.DEVICES, self.winefodler, self.block_output_folder);
        os.system("rm -f " + self.config);
        block_device = self.block_device.split(",");
        i = 0;
        while True:
            if(i >= len(block_device)):
                break;
            if(block_device[i] == "z"):
                if(self.qlabel_bool[i].isChecked() == True):
                    restore_device_z(self.winefodler);
            i = i +1;
        self.change_WINEPREFIX(self.WINEPREFIX);
        self.change_gui(self.block_device, self.winefodler);
        return 0;
    def browse_WINEPREFIX(self):            
        msgBox = QtWidgets.QMessageBox();
        msgBox.setIcon(QtWidgets.QMessageBox.Warning);
        if(self.steammode == 1):
            self.steammode = 0;
            msgBox.setText("You are in steamode and disabled steammode");
            msgBox.exec();
        while True:
            fieldialog = QtWidgets.QFileDialog;
            file = fieldialog.getExistingDirectory(self, "WINEPREFIX", home);
            if(file == ""):
                exit();
            if(os.path.exists(file + "/dosdevices")  == True):
                self.textedit_wineprefix.setText(file);
                self.change_WINEPREFIX(file);
                self.textedit_wineprefix.setText(file);
                self.change_gui(self.block_device, self.winefodler);
                break;
            else:
                msgBox.setText("The folder isn't a WINEPREFIX: \"" + file + "\"");
                msgBox.exec();
        return 0;

    def closeEvent(self, event):
        self.bcolse = True;
        event.accept();
    def calculate_path1(self, path):
        i = len(path);
        badd = 0;
        b1 = 0;
        while True:
            if(i == 0):
                break;
            if(path[i] == '/'):
                badd = badd + 1;
            if(badd >= 5):
                b1 = 1;
                break;
            i = i -1;
        j = 0;
        s1 = "";
        while True:
            if(j >= i):
                break;
            if(j >= len(path)):
                break;
            s1 = s1 + path[j];
            j = j +1;
        return s1;
    def lsit_all_Proton_games(self):
        if(steamall == 0):
            return 0;
        os.system("protontricks -s \"*\" | grep \"(\" | cat>/tmp/tmp_wine_hardend_script.tmp");
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
        #print(s4);
        #print(s4_name);
        i = 0;
        while True:
            if(i >= len(s4)):
                break;
            print(s4_name);
            if(steamauto == 1):
                os.system("protontricks -c \"python3.8 '" + script_path + "' -Steam_auto_protect -noerror\" " + s4[i]);
            elif(steamauto == 2):
                os.system("protontricks -c \"python3.8 '" + script_path + "' -Steam_auto_remove_protect -noerror\" " + s4[i]);
            i = i +1;


        os.system("rm -f /tmp/tmp_wine_hardend_script.tmp")
        return 0;





app = QtWidgets.QApplication(sys.argv);
mainwindow = Wine_hardened_script_gui();
if(steamauto == 1):
    mainwindow.hardened_start();
    #mainwindow.show();
    #app.exec_();
    mainwindow.close();
elif(steamauto == 2):
    mainwindow.remove_hardened();
    #mainwindow.show();
    #app.exec_();
    mainwindow.close();
else:
    mainwindow.show();
    app.exec_();

