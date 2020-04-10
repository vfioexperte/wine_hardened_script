#!/usr/bin/env python
#Copyright (C) 2020  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#Warnung der Programmierer hafte nicht auf Schäden oder auf unsachgemäßen Umgang der APP
version = "0.9c"
print(version);

from PyQt5 import QtWidgets
from PyQt5 import QtGui
import sys
import os
import os.path
import platform
import string

script_path = "/usr/bin/wine-security-gui";

steammode = 0;
steamauto = 0;
steamall = 0;
noerror = 0;
add_blacklist = 0;
remvoe_blacklist = 0,
appname = "wine-security-gui";
debug_fodler = "";
if(len(sys.argv) == 2 or len(sys.argv) == 3):
    if(sys.argv[1] == "-version"):
        exit();
    if(sys.argv[1] == "-Steam"):
        print("enabled Steam mode");
        print("use this mode only with protontricks command")
        print("you will find the APPID with protontricks -s \"game name\"");
        print("protontricks  -c \"/usr/bin/wine-security-gui -Steam\" APPID")
        steammode = 1;
    elif(sys.argv[1] == "-Steam_auto_protect"):
        print("enabled Steam auto protect mode");
        print("protontricks  -c \"/usr/bin/wine-security-gui -Steam_auto_protect\" APPID");
        print("auto protect mode enabled");
        steamauto = 1;
        steammode = 1;
    elif(sys.argv[1] == "-Steam_auto_remove_protect"):
        print("enabled Steam auto remove protect mode");
        print("protontricks  -c \"/usr/bin/wine-security-gui -Steam_auto_remove_protect\" APPID");
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
    elif(sys.argv[1] == "-add_to_balcklist"):
        add_blacklist = 1;
    elif(sys.argv[1] == "-remove_to_balcklist"):
        remvoe_blacklist = 1;
    if(len(sys.argv) == 3):
        if(sys.argv[2] == "-noerror"):
            print("enable noerror mode");
            noerror = 1;
    elif(sys.argv[1] == "--help" or sys.argv[1] == "-h"):
        print("options:");
        print("");
        print("-Steam");
        print("enabled Steam mode");
        print("only use this mode with protontricks command")
        print("you will find the APPID with protontricks -s \"game name\"");
        print("protontricks  -c \"/usr/bin/wine-security-gui -Steam\" APPID")
        print("");
        print("-Steam_auto_protect");
        print("enabled Steam auto protect mode");
        print("protontricks  -c \"/usr/bin/wine-security-gui -Steam_auto_protect\" APPID");
        print("auto protect mode enabled");
        print("");
        print("-Steam_auto_remove_protect");
        print("enabled Steam auto remove protect mode");
        print("protontricks  -c \"/usr/bin/wine-security-gui -Steam_auto_remove_protect\" APPID");
        print("auto remove protect mode enabled");
        print("");
        print("-Steam_all_auto_protect");
        print("protect all steam games");
        print("");
        print("-Steam_all_auto_remove_protect");
        print("remove protection all steam games");
        print("");
        print("-add_to_balcklist");
        print("add WINEPREFIX to blacklist");
        print("-remove_to_balcklist");
        print("remvoe blacklist from WINEPREFIX");
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
    if debug_fodler:
        WINEPREFIX = debug_fodler;
        os.makedirs(os.path.join(debug_folder, 'dosdevices'), exist_ok=True);
        return debug_fodler;
    try:
        WINEPREFIX = os.environ['WINEPREFIX'];
    except KeyError:
        home = os.environ['HOME'];
        WINEPREFIX = os.path.join(home, ".wine");
    return WINEPREFIX;

def remnove_hardened(device, winefodler, block_output_folder):
    i = 0;
    while True:
        if(i >= len(device)):
            break;
        s2 = device[i];
        s1 = winefodler + "/" + s2 + ":";
        s3 = s1 + ":";
        if(os.path.islink(s1) == True):
            os.unlink(s1);
        if(os.path.islink(s3) == True):
            os.unlink(s3);
        #system("rm -f \"" + s1 + "\"");
        #system("rm -f \"" + s3 + "\"");
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
            os.symlink(block_output_folder, s1, True);
            #system("ln -sf " + "\"" + block_output_folder + "\" " + "\""  + s1 + "\"");
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
    if(os.path.islink(s2) == True):
        os.unlink(s2);
    os.symlink("/", s2, True);
    #os.system("ln -sf " + "/ " + "\"" + winefodler + "/z:" + "\"");
    return 0;

class Wine_hardened_script_gui(QtWidgets.QWidget):
    def __init__(self):
        self.init = 0;
        QtWidgets.QWidget.__init__(self)
        self.title = appname +  " - " + version;
        self.setWindowTitle(self.title);
        self.WINEPREFIX = read_WINEPREFIX();
        self.block_device = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z";
        self.DEVICES = list(string.ascii_lowercase);
        self.block_output_folder = os.path.join("/tmp",  "wine_security");
        self.device_overide = "";
        self.winefodler = os.path.join(self.WINEPREFIX ,"/dosdevices");
        self.config = os.path.join(self.winefodler , "/.hardened.config");
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
        if(self.init == 1):
            self.steammode = 0;
        elif(self.init == 2):
            self.steammode = 1;
        else:
            self.steammode = steammode;
        if(os.path.isdir(wineprefix) == False):
            if(noerror == 0):
                print("WINEPREFIX: " + "\"" + wineprefix + "\" not found!");
                msgBox = QtWidgets.QMessageBox();
                msgBox.setIcon(QtWidgets.QMessageBox.Warning);
                msgBox.setText("WINEPREFIX: " + "\"" + wineprefix + "\" not found!");
                msgBox.exec();
            exit();
        if(steamall == 0 and self.steammode != 0):
            self.title = appname +  " (Steam mode) - " + version;
            self.setWindowTitle(self.title);
            if(wineprefix.find("compatdata") == -1 or wineprefix.find("pfx") == -1):
                if(noerror == 0):
                    print("WINEPREFIX: " + "\"" + wineprefix + "\" not a steam wine folder found!\nremove the -Steam options!");
                    msgBox = QtWidgets.QMessageBox();
                    msgBox.setIcon(QtWidgets.QMessageBox.Warning);
                    msgBox.setText("WINEPREFIX: " + "\"" + wineprefix + "\" not a steam wine folder found!\nremove the -Steam options!");
                    msgBox.exec();
                exit();
        else:
            self.title = appname +  " - " + version;
            self.setWindowTitle(self.title);
            if(wineprefix.find("compatdata") != -1 and wineprefix.find("pfx") != -1):
                self.title = appname +  " (Steam mode) - " + version;
                self.setWindowTitle(self.title);
                self.steammode = 1;
        self.WINEPREFIX = wineprefix;
        self.winefodler = os.path.join(self.WINEPREFIX ,"dosdevices");
        self.config = os.path.join(self.winefodler ,".hardened.config");
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
        #self.steammode = steammode;
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
                if(device_overide[i] == "0" and self.steammode == 0):
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
        if(self.is_blacklsited() == True):
            if(noerror == 0):
                print("ERROR folder is blacklisted");
                msgBox = QtWidgets.QMessageBox();
                msgBox.setIcon(QtWidgets.QMessageBox.Warning);
                msgBox.setText("ERROR folder is blacklisted");
                msgBox.exec();
            exit();
        if(os.path.isfile(self.config) == True):
            if(noerror == 0):
                print("ERROR folder is ready protect");
                msgBox = QtWidgets.QMessageBox();
                msgBox.setIcon(QtWidgets.QMessageBox.Warning);
                msgBox.setText("ERROR folder is ready protect");
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
        if(self.is_blacklsited() == True):
            if(noerror == 0):
                print("ERROR folder is blacklisted");
                msgBox = QtWidgets.QMessageBox();
                msgBox.setIcon(QtWidgets.QMessageBox.Warning);
                msgBox.setText("ERROR folder is blacklisted");
                msgBox.exec();
            exit();
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
        while True:
            fieldialog = QtWidgets.QFileDialog;
            file = fieldialog.getExistingDirectory(self, "WINEPREFIX", home);
            if(file == ""):
                exit();
            if(os.path.exists(file + "/dosdevices")  == True):
                if(self.steammode == 1):
                    if(file.find("compatdata") == -1 or file.find("pfx") == -1):
                        self.steammode = 0;
                        self.init = 1;
                        msgBox.setText("You chose wrong folder, isn't a steam folder. " + appname + " got disable steammode.");
                        msgBox.exec();
                    else:
                        self.init = 0;
                else:
                    if(file.find("compatdata") != -1 or file.find("pfx") != -1):
                        self.init = 2;
                        self.steammode = 1;
                        msgBox.setText("You chose wrong folder, isn't a wine folder. " + appname + " got enable steammode.");
                        msgBox.exec();

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
        #print(s4);
        #print(s4_name);
        i = 0;
        while True:
            if(i >= len(s4)):
                break;
            print(s4_name);
            if(steamauto == 1):
                os.system("protontricks -c \"python '" + script_path + "' -Steam_auto_protect -noerror\" " + s4[i]);
            elif(steamauto == 2):
                os.system("protontricks -c \"python '" + script_path + "' -Steam_auto_remove_protect -noerror\" " + s4[i]);
            i = i +1;


        os.system("rm -f /tmp/tmp_wine_hardend_script.tmp")
        return 0;
    def is_blacklsited(self):
        sblacklsit = self.winefodler + "/" +".blacklist";
        if(os.path.isfile(sblacklsit) == False):
            return False;
        else:
            return True;
        return -1;
    def set_blacklist(self):
        sblacklsit = self.winefodler + "/" +".blacklist";
        if(self.is_blacklsited() == False):
            file1 = open(sblacklsit, "w");
            file1.write(" ");
            file1.close();
            return 0;
        else:
            if(noerror == 0):
                msgBox = QtWidgets.QMessageBox();
                msgBox.setIcon(QtWidgets.QMessageBox.Warning);
                msgBox.setText("ERROR is blacklisted");
                msgBox.exec();
            print("ERROR is blacklisted");
            exit();
    def remvoe_blacklist(self):
        sblacklsit = self.winefodler + "/" +".blacklist";
        if(os.path.isfile(sblacklsit) == False):
            if(noerror == 0):
                msgBox = QtWidgets.QMessageBox();
                msgBox.setIcon(QtWidgets.QMessageBox.Warning);
                msgBox.setText("ERROR is not blacklisted");
                msgBox.exec();
            print("ERROR is not blacklisted");
            exit();
        else:
            os.remove(sblacklsit);
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
elif(add_blacklist == 1):
    mainwindow.set_blacklist();
    mainwindow.close();
elif(remvoe_blacklist == 1):
    mainwindow.remvoe_blacklist();
    mainwindow.close();
else:
    mainwindow.show();
    app.exec_();

