#!/usr/bin/env python3
#Copyright (C) 2020  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#Warnung der Programmierer hafte nicht auf Schäden oder auf unsachgemäßen Umgang der APP
#19.12.2020 #start wirting app
#26.07.2022 last edit
#rollback to 0.6d
version = "v0.8a_zstd_thinker"
#v0.8a_zstd_thinker download size caluclete 0.1a
#0.7p_zstd_thinker_0.1f progrssbar_label 1 of 1 0.2a
#v0.7p_zstd_thinker_0.1e progrssbar_label 1 of 1
#v0.7p_zstd thinker 0.1d window size fix 0.1a
#v0.7m vorschau aplha 0.1a
#v0.7l noquestion mode auto server start 0.1a
#v0.7i ipv6 0.1a beta
#v0.7h aufraumen speed fix 1
#v0.7f sav before start fodler paths 1
#v0.7f fix internet abruch 2 add debug command -testmode_errror
#v0.7d eroor fix ConnectionResetError server sietig abgesichert
#v0.7c fix crash wenn daten nach geschoben werden
#v0.7a zeit anzeige
#v0.6l  speed hak 02
print(version)
appname = "Sebs Sync App";



try:
    import math
    #from PyQt6 import QtWidgets
    #from PyQt6 import QtGui
    import sys
    import os
    import os.path
    import platform
    import socket
    import hashlib
    import sys
    import os
    import os.path
    import struct
    import shlex, subprocess
    #import subprocess
    #import pty
    import os
    import sys
    import os, time, datetime
    import requests
    import binascii
    import os
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    import time
    import json
    import argparse
    import zstd
    from tkinter import *
    import tkinter.simpledialog
    from tkinter import messagebox
    from tkinter.simpledialog import Dialog
    from tkinter.ttk import Progressbar
    import threading

except ImportError:
    import pip
    if(platform.system() == 'Linux'):
        os.system("sudo pacman -Sy tk")
    failed = pip.main(["install", "pywinpty"]);
    failed = pip.main(["install", "requests"]);
    failed = pip.main(["install", "cryptography"]);
    failed = pip.main(["install", "zstd"]);
    failed = pip.main(["install", "tkinter.simpledialog"]);
    #failed = pip.main(["install", "tk"]);

import math
import sys
import os
import os.path
import platform
import socket
import hashlib
import sys
import os
import os.path
import struct
import shlex, subprocess
#import subprocess
#import pty
import os
import sys
import os, time, datetime
import requests
import binascii
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import time
#from PyQt6 import QtWidgets
#from PyQt6 import QtGui
import json
import argparse
import zstd
from tkinter import *
from tkinter import filedialog
import tkinter.simpledialog
from tkinter import messagebox
from tkinter.simpledialog import Dialog
from tkinter.ttk import Progressbar
import threading

parser = argparse.ArgumentParser()
parser.add_argument('-testmode', action='store_true', default=False, dest='boolean_version', help='aktived loacl test mode');
parser.add_argument("-ip", type=str,  default="", dest="ip", help="set force a server ip")
parser.add_argument('-testmode_errror', action='store_true', default=False, dest='testerror', help='aktived loacl test mode simulate error');
parser.add_argument('-noencrypt_mode', action='store_true', default=False, dest='noencrypt_mode', help='disable no encrypt mode Server only');
parser.add_argument("-aeskey", type=str,  default="", dest="aes_key", help="set aeskey")
parser.add_argument("-iv", type=str,  default="", dest="iv_key", help="set iv key")
parser.add_argument("-port", type=str,  default="", dest="port", help="set network port")
parser.add_argument('-ipv6', action='store_true', default=False, dest='ipv6_mode', help='disavble ipv4 enable ipv6');
parser.add_argument('-ipv4', action='store_true', default=False, dest='ipv4_mode', help='disavble ipv6 enable ipv4');
parser.add_argument('-serverstartauto', action='store_true', default=False, dest='serverstartauto', help='start auto server');
parser.add_argument("-serverstartautodir", type=str,  default="", dest="serverstartautodir", help="start auto server dir path")
parser.add_argument('-noqeestionmode', action='store_true', default=False, dest='noqeestionmode', help='server no qestion mode');
results = parser.parse_args();
ip = "";
test_fehelrmode = 0
testmode = 0;
noencrypt_mode = 0;
aes_key = "";
iv_key = "";
port = -1;
ip_mode = -1;
serverstartauto = 0;
noqeestionmode = 0;
serverstartautodir = "";

server_block_übertragungs_länge = 1024*64;
#1024*64 speed fix ipv4 maxmut 64kb
#1024*500
#https://en.wikipedia.org/wiki/Maximum_transmission_unit

if(results.boolean_version == True):
    testmode = 1;
if(results.ip != ""):
    #testmode = 1;
    ip = results.ip

if(results.aes_key != ""):
    aes_key = results.aes_key

if(results.iv_key != ""):
    iv_key = results.iv_key

if(results.port != ""):
    port = int(results.port)

if(results.ipv6_mode == True):
    ip_mode = 6;

if(results.ipv4_mode == True):
    ip_mode = 4;

if(results.serverstartauto == True):
    serverstartauto = 1;
    noqeestionmode = 1;

if(results.serverstartautodir != ""):
    serverstartautodir = results.serverstartautodir;

if(results.noqeestionmode == True):
    noqeestionmode = 1;


if(testmode == 1):
    print("Test mdoe on");
if(testmode == 1 and results.ip != ""):
    print("Test mdoe on with ip:", ip);
if(results.testerror == True):
    print("test fehler mdoe on!");
    test_fehelrmode = 1;

if(results.noencrypt_mode == True):
    print("no encrypt_moder mdoe on!");
    noencrypt_mode = 1;

jason_data = {};

#app = QtWidgets.QApplication(sys.argv);

trenner = b"x";
trenner_str = trenner.decode();

sav_filepaht= "1.sav";

sav_ip= "ip.sav";

home = "";

Betribsystem = False;
if(platform.system() == 'Linux'):
    Betribsystem = False;
else:
    Betribsystem = True;


class seb_sync_clinet_gui():
    def __init__(self):
        if(noencrypt_mode == 0):
            self.noencryptmode = noencrypt_mode;
            self.title = appname + " encrypt mode on - " + version;
        else:
            self.noencryptmode = noencrypt_mode;
            self.title = appname + " encrypt mode off - " + version;
        self.textedit_Verzeichniss1  = "";
        self.filecount = 0;
        self.maxfilecount = 0;
        self.vorschau = False;
        self.progressbar_firststart = 0;
        return
        #QtWidgets.QWidget.__init__(self)
        #self.ip = "127.0.0.1";
        #self.port = 9044;
        #self.statusBar().showMessage('Message in statusbar.');
        self.statusbar = QtWidgets.QStatusBar();
        self.statusbar.showMessage("test");
        if(noencrypt_mode == 0):
            self.noencryptmode = noencrypt_mode;
            self.title = appname + " encrypt mode on - " + version;
        else:
            self.noencryptmode = noencrypt_mode;
            self.title = appname + " encrypt mode off - " + version;
        self.setWindowTitle(self.title);
        self.resize(600, 200);
        self.layoutv1 = QtWidgets.QVBoxLayout(self)
        self.vorschau = False;

        self.layouth00 = QtWidgets.QHBoxLayout(self)
        self.layouth0 = QtWidgets.QHBoxLayout(self)
        self.layouth1 = QtWidgets.QHBoxLayout(self)
        self.layouth2 = QtWidgets.QHBoxLayout(self)
        self.layouth3 = QtWidgets.QHBoxLayout(self)
        self.layouth4 = QtWidgets.QHBoxLayout(self)
        self.layouth5 = QtWidgets.QHBoxLayout(self)
        self.label_Verzeicniss1 = QtWidgets.QLabel("Ordner Path: ")
        self.label_Verzeicniss_name1 = QtWidgets.QLabel("Verzeichnis Namen: ")
        #self.label_Verzeicniss_ip = QtWidgets.QLabel("IP: ")
        #self.label_Verzeicniss_port = QtWidgets.QLabel("Port: ")

        self.textedit_Verzeichniss1 = QtWidgets.QTextEdit()
        self.textedit_Verzeichniss2 = QtWidgets.QTextEdit()
        self.textedit_Verzeichniss3 = QtWidgets.QTextEdit()
        self.textedit_Verzeichniss4 = QtWidgets.QTextEdit()

        self.textedit_Verzeichniss_pushbutton1 = QtWidgets.QPushButton("browse...")
        self.textedit_Verzeichniss_pushbutton2 = QtWidgets.QPushButton("browse...")
        self.textedit_Verzeichniss_pushbutton3 = QtWidgets.QPushButton("browse...")
        self.textedit_Verzeichniss_pushbutton4 = QtWidgets.QPushButton("browse...")



        self.textedit_Verzeichniss_name1 = QtWidgets.QTextEdit()
        self.textedit_Verzeichniss_name2 = QtWidgets.QTextEdit()
        self.textedit_Verzeichniss_name3 = QtWidgets.QTextEdit()
        self.textedit_Verzeichniss_name4 = QtWidgets.QTextEdit()

        self.textedit_Verzeichniss_name1.setText("Ordner1");
        self.textedit_Verzeichniss_name2.setText("Ordner2");
        self.textedit_Verzeichniss_name3.setText("Ordner3");
        self.textedit_Verzeichniss_name4.setText("Ordner4");


        #self.textedit_ip = QtWidgets.QTextEdit();
        #self.textedit_ip.setText(self.ip);
        #self.spinbox_port = QtWidgets.QSpinBox();
        #self.spinbox_port.setMaximum(1);
        #self.spinbox_port.setValue(self.port);
        #self.spinbox_port.setMaximum(10000);

        #self.layouth00.addWidget(self.label_Verzeicniss_ip);
        #self.layouth00.addWidget(self.label_Verzeicniss_port);

        #self.layouth0.addWidget(self.textedit_ip);
        #self.layouth0.addWidget(self.spinbox_port);


        self.layouth1.addWidget(self.label_Verzeicniss1);
        self.layouth1.addWidget(self.label_Verzeicniss_name1);
        self.layouth2.addWidget(self.textedit_Verzeichniss1);
        self.layouth2.addWidget(self.textedit_Verzeichniss_name1);
        self.layouth2.addWidget(self.textedit_Verzeichniss_pushbutton1);
        self.layouth3.addWidget(self.textedit_Verzeichniss2);
        self.layouth3.addWidget(self.textedit_Verzeichniss_name2);
        self.layouth3.addWidget(self.textedit_Verzeichniss_pushbutton2);
        self.layouth4.addWidget(self.textedit_Verzeichniss3);
        self.layouth4.addWidget(self.textedit_Verzeichniss_name3);
        self.layouth4.addWidget(self.textedit_Verzeichniss_pushbutton3);
        self.layouth5.addWidget(self.textedit_Verzeichniss4);
        self.layouth5.addWidget(self.textedit_Verzeichniss_name4);
        self.layouth5.addWidget(self.textedit_Verzeichniss_pushbutton4);

        self.textedit_Verzeichniss_pushbutton1.clicked.connect(self.browse1);
        self.textedit_Verzeichniss_pushbutton2.clicked.connect(self.browse2);
        self.textedit_Verzeichniss_pushbutton3.clicked.connect(self.browse3);
        self.textedit_Verzeichniss_pushbutton4.clicked.connect(self.browse4);


        self.button = QtWidgets.QPushButton();
        self.layoutv1.addLayout(self.layouth00)
        self.layoutv1.addLayout(self.layouth0)
        self.layoutv1.addLayout(self.layouth1)
        self.layoutv1.addLayout(self.layouth2)
        self.layoutv1.addLayout(self.layouth3)
        self.layoutv1.addLayout(self.layouth4)
        self.layoutv1.addLayout(self.layouth5)
        #self.layoutv1.addWidget(self.button)
        #self.button.clicked.connect(self.button_Clickes)
        self.button_start_Server = QtWidgets.QPushButton("Start Server");
        self.button_start_Server.clicked.connect(self.start_Server);
        self.button_start_Client = QtWidgets.QPushButton("Start Client");
        self.button_start_Client.clicked.connect(self.start_sync);
        self.button_start_sav_folder_path = QtWidgets.QPushButton("Sav Folder Paths");
        self.button_start_sav_folder_path.clicked.connect(self.sav);
        self.layoutv1.addWidget(self.button_start_Server)
        self.layoutv1.addWidget(self.button_start_Client)
        self.layoutv1.addWidget(self.button_start_sav_folder_path)
        self.setLayout(self.layoutv1)

        self.progressbar = QtWidgets.QProgressBar(self);
        self.layouth6 = QtWidgets.QHBoxLayout(self);
        self.layouth6.addWidget(self.statusbar);
        self.layouth6.addWidget(self.progressbar);
        self.layoutv1.addLayout(self.layouth6);

        self.progressbar.setValue(0)
        self.progressbar.setMaximum(400);

        if(os.path.isfile(sav_ip) == True):
            fobj = open(sav_ip, "rb");
            fobj.seek(0, 2)
            size = fobj.tell()
            fobj.seek(0, 0)
            s1 = fobj.read(size);
            s1 = s1.decode();
            array = s1.split("^");
            self.ip = array[0];
            self.port = int(array[1]);
            self.textedit_ip.setText(self.ip);
            self.spinbox_port.setValue(self.port);
        self.filecount = 0;
        self.maxfilecount = 0;

        self.update_progress_info("init", 0, 400);
        if(os.path.isfile(sav_filepaht) == True):
            fobj = open(sav_filepaht, "rb");
            fobj.seek(0, 2)
            size = fobj.tell()
            fobj.seek(0, 0)
            s1 = fobj.read(size);
            s1 = s1.decode();
            array = s1.split("^");
            self.textedit_Verzeichniss1.setText(array[0]);
            self.textedit_Verzeichniss_name1.setText(array[1]);
            self.textedit_Verzeichniss2.setText(array[2]);
            self.textedit_Verzeichniss_name2.setText(array[3]);
            self.textedit_Verzeichniss3.setText(array[4]);
            self.textedit_Verzeichniss_name3.setText(array[5]);
            self.textedit_Verzeichniss4.setText(array[6]);
            self.textedit_Verzeichniss_name4.setText(array[7]);

            if(self.textedit_Verzeichniss1.toPlainText() != "" and self.textedit_Verzeichniss_name1.toPlainText() != ""):
                self.textedit_Verzeichniss1.setDisabled(True);
                self.textedit_Verzeichniss_name1.setDisabled(True);
            if(self.textedit_Verzeichniss2.toPlainText() != "" and self.textedit_Verzeichniss_name2.toPlainText() != ""):
                self.textedit_Verzeichniss2.setDisabled(True);
                self.textedit_Verzeichniss_name2.setDisabled(True);
            if(self.textedit_Verzeichniss3.toPlainText() != "" and self.textedit_Verzeichniss_name3.toPlainText() != ""):
                self.textedit_Verzeichniss3.setDisabled(True);
                self.textedit_Verzeichniss_name3.setDisabled(True);
            if(self.textedit_Verzeichniss4.toPlainText() != "" and self.textedit_Verzeichniss_name4.toPlainText() != ""):
                self.textedit_Verzeichniss4.setDisabled(True);
                self.textedit_Verzeichniss_name4.setDisabled(True);

            self.update_progress_info("loading savfile finsihed", 0, 400);

    def update_progress_info(self, text, progrssbar_value, progrssbar_maxvalue, size = -1):
        self.calulate_size_mb = -1;
        if(size != -1):
            self.calulate_size = self.calulate_size + size  ;
            self.calulate_size_mb = self.calulate_size / 1024 / 1024;
        if(progrssbar_value == 0 and progrssbar_maxvalue == 0):
            self.progrssbar_text = text;
        else:
            if(self.calulate_size_mb  != -1):
                self.progrssbar_text = text + " %" + str( self.float_to_int(100 / progrssbar_maxvalue * progrssbar_value) )  + " | " + str(self.filecount) + "/" + str(self.maxfilecount) + " | " + str(self.float_to_int(self.calulate_size_mb)) + "/" +  str(self.float_to_int(self.calulate_max_size / 1024 / 1024)) + "MB";
            else:
                self.progrssbar_text = text + " %" + str( self.float_to_int(100 / progrssbar_maxvalue * progrssbar_value) )  + " | " + str(self.filecount) + "/" + str(self.maxfilecount);
        self.progrssbar_value = progrssbar_value;
        self.progrssbar_maxvalue = progrssbar_maxvalue;
        self.progrssbar['value'] = progrssbar_value;
        self.progrssbar['maximum'] = progrssbar_maxvalue;
        self.progrssbar_label.set(self.progrssbar_text)
        print("#######################PROGRESSBAR_INFO#######################")
        print(self.progrssbar_text)
        #self.progrssbar.start();
        self.window.update_idletasks();
        #self.window.wait_window();
        return 0;
        class mypogressbar():
            def __init__(self, a1):
                pass;
            def init(self, text, progrssbar_value, progrssbar_maxvalue):
                self.root = Tk()
                self.progress = Progressbar(self.root, orient=HORIZONTAL, length=progrssbar_maxvalue, mode='determinate');
                self.progress['value'] = progrssbar_value;
                self.root.update_idletasks();
                self.label_str = StringVar()
                self.root.title(text)
                self.progress.pack(fill="x")
                #self.label_str.set(text)
                self.label = Label( self.root, textvariable=self.label_str, relief=RAISED )
                self.label_str.set(text)
                self.label.pack(fill="x");

            def set(self, text, progrssbar_value, progrssbar_maxvalue):
                self.text = text;
                self.progrssbar_value = progrssbar_value;
                self.progrssbar_maxvalue = progrssbar_maxvalue;
                self.progress['value'] = progrssbar_value;
                self.progress.start();
                self.label_str = self.text;
                self.root.update_idletasks();
                self.root.wait_window()
                #self.progress.stop();
                #self.progress.grid_forget();


            def quit(self):
                self.root.quit();
                self.root.destroy();

        if(self.progressbar_firststart == 0):
            self.progressbar_firststart = 1;
            self.mypogressbar = mypogressbar(text);
            self.mypogressbar.init(text, progrssbar_value, progrssbar_maxvalue);
            self.mypogressbar.quit();
        else:
            self.mypogressbar.set(text, progrssbar_value, progrssbar_maxvalue);

        return 0;

    def start_sync(self):
        if(testmode != 1):
            self.sav();
        #self.button_start_Server.setDisabled(True);
        #self.button_start_Client.setDisabled(True);
        aes_key = self.question_aes_key();
        iv_ = self.question_iv_key();
        b1 = 0;
        stxt = "";
        if(self.textedit_Verzeichniss1 != ""):
            b1 = 1;
            self.listpatharray = [];
            stxt = os.path.join(self.textedit_Verzeichniss1, "1.txt");
            #self.update_progress_info("start sync 1.. " + self.textedit_Verzeichniss_name1, 0, 400);
            self.start_Client("5", "0", self.textedit_Verzeichniss1, aes_key, iv_);
            self.listpatharray = [];
            #self.update_progress_info("start sync 2.. " + self.textedit_Verzeichniss_name1,0, 400);
            self.start_Client("5", "0", self.textedit_Verzeichniss1, aes_key, iv_);
            self.listpatharray = [];
        if(b1 == 0):
            if(noqeestionmode == 0):
                #msgBox2 = QtWidgets.QMessageBox();
                #msgBox2.setText("All Textboxen is empty. please click browse!",0, 400);
                #msgBox2.exec();
                messagebox.showinfo("ERROR", "All Textboxen is empty. please click browse!")
            self.update_progress_info("sync ende",0, 400);
            self.listpatharray = [];
            if(os.path.isfile(stxt) == True):
                os.remove(stxt)
            return -1;
        if(noqeestionmode == 0):
            #msgBox2 = QtWidgets.QMessageBox();
            #msgBox2.setText("Sync Fertig!");
            #msgBox2.exec();
            messagebox.showinfo("fertig", "Sync Fertig!")
        if(testmode != 1):
            self.sav();
        self.update_progress_info("sync ende",0, 400);
        #self.button_start_Server.setDisabled(False);
        #self.button_start_Client.setDisabled(False);
        if(os.path.isfile(stxt) == True):
            os.remove(stxt)
        return 0;

    def sav(self):
        s1 = self.textedit_Verzeichniss1 + "^" + "1" + "^";
        fobj = open(sav_filepaht, "wb");
        fobj.write(s1.encode());
        fobj.close();
        return 0;

    def button_Clickes(self):
        self.start_Server();
        return 0;

        s1 = self.textedit_Verzeichniss1.toPlainText() + "^" + self.textedit_Verzeichniss_name1.toPlainText() + "^";
        s1 = s1 + self.textedit_Verzeichniss2.toPlainText() + "^" + self.textedit_Verzeichniss_name2.toPlainText() + "^";
        s1 = s1 + self.textedit_Verzeichniss3.toPlainText() + "^" + self.textedit_Verzeichniss_name3.toPlainText() + "^";
        s1 = s1 + self.textedit_Verzeichniss4.toPlainText() + "^" + self.textedit_Verzeichniss_name4.toPlainText() + "^";
        fobj = open(sav_filepaht, "wb");
        fobj.write(s1.encode());
        fobj.close();

        #self.ip = self.textedit_ip.toPlainText();
        #self.port = self.spinbox_port.value();
        #s1 = self.ip + "^" + str(self.port) + "^";
        #fobj = open(sav_ip, "wb");
        #fobj.write(s1.encode());
        #fobj.close();

        self.title  = appname + " - " + version + " run..";
        self.setWindowTitle(self.title);
        run_cmd(self.textedit_Verzeichniss1.toPlainText());
        run_cmd(self.textedit_Verzeichniss2.toPlainText());
        run_cmd(self.textedit_Verzeichniss3.toPlainText());
        run_cmd(self.textedit_Verzeichniss4.toPlainText());
        self.title  = appname + " - " + version + " ..fertig";
        self.setWindowTitle(self.title);
        return 0;

    def browse_dir(self):
        fieldialog = QtWidgets.QFileDialog;
        dir = fieldialog.getExistingDirectory(self, "browse sync folder", home,);
        return dir;

    def browse1(self):
        dir = self.browse_dir();
        if(os.path.isdir(dir) == False):
            self.browse1();
        self.textedit_Verzeichniss1.setText(dir);
        return 0;

    def browse2(self):
        dir = self.browse_dir();
        if(os.path.isdir(dir) == False):
            self.browse2();
        self.textedit_Verzeichniss2.setText(dir);
        return 0;

    def browse3(self):
        dir = self.browse_dir();
        if(os.path.isdir(dir) == False):
            self.browse3();
        self.textedit_Verzeichniss3.setText(dir);
        return 0;

    def browse4(self):
        dir = self.browse_dir();
        if(os.path.isdir(dir) == False):
            self.browse4();
        self.textedit_Verzeichniss4.setText(dir);
        return 0;

    def read_Connetion_file(self, folder, aeskey, iv):
        try:
            stxt = os.path.join(folder, "1.txt");
            if(os.path.isfile(stxt) == False):
                if(noqeestionmode == 0):
                    #msgBox2 = QtWidgets.QMessageBox();
                    #msgBox2.setText("ERROR Connection File not exist! 1.txt file not found in seleted folder");
                    #msgBox2.exec();
                    messagebox.showinfo("ERROR", "ERROR Connection File not exist! 1.txt file not found in seleted folder")
                print("ERROR Connection File not exist!");
                return [];
            if(len(self.json_array) != 0):
                return self.json_array;
            #fobj2 = open(stxt, "rb");
            #fobj2.seek(0, 2);
            #size = fobj2.tell();
            #fobj2.seek(0, 0);
            #s2 = fobj2.read(size);
            #fobj2.close();
            #byte2=binascii.unhexlify(s2);
            #byte_1bin = self.bytes_decryption(aeskey, iv, byte2);
            if(self.json_file_read(stxt) != 0):
                return [];
            #self.json_aes = jason_data['sav_data']['aes'];
            #self.json_iv = jason_data['sav_data']['iv'];
            #self.json_aes_hash = jason_data['sav_data']['aes_hash'];
            #self.json_iv_hash = jason_data['sav_data']['iv_hash'];
            #self.json_myip =  jason_data['sav_data']['myip'];
            #self.json_port =  jason_data['sav_data']['port'];
            ip = self.json_myip;
            port = self.json_port;
            hash = self.json_aes_hash;
            key_ = self.bytes_decryption(aeskey, iv, self.json_aes);
            iv_ = self.bytes_decryption(aeskey, iv, self.json_iv);
            ipv6 = self.ipv6;
            #s2 = byte_1bin.decode();
            #s3 = s2.split("^");
            #ip = s3[0];
            #port = int(s3[1]);
            #key_ = s3[2];
            #iv_ = s3[3];
            #hash = s3[4];
            #key_ =  self.hex_to_String(key_);
            #iv_ = self.hex_to_String(iv_);

            hash_aes_key = hashlib.sha256();
            hash_aes_key.update(str(ip).encode());
            hash_aes_key.update(str(port).encode());
            hash_aes_key.update(key_);
            hash_aes_key.update(iv_);
            hash_aes_key = hash_aes_key.hexdigest();
            #os.remove(sbin);
            #os.remove(sbin_decrypt);

            print("hash_aes_key: ", hash_aes_key)
            print("hash: ", hash)
            if(hash_aes_key != hash):
                if(noqeestionmode == 0):
                    #msgBox2 = QtWidgets.QMessageBox();
                    #msgBox2.setText("ERROR Connection File not corupt or passwor wrong!");
                    #msgBox2.exec();
                    messagebox.showinfo("ERROR", "ERROR Connection File not corupt or passwor wrong!")
                print("ERROR Connection File not corupt or passwor wrong!");
                #os.remove(sbin);
                #os.remove(sbin_decrypt);
                return [];
            if(noencrypt_mode == 0):
                self.noencryptmode = noencrypt_mode;
                self.title = appname + " encrypt mode on - " + version;
            else:
                self.noencryptmode = noencrypt_mode;
                self.title = appname + " encrypt mode off - " + version;
                if(noqeestionmode == 0):
                    #msgBox2 = QtWidgets.QMessageBox();
                    #msgBox2.setText("Warning encrypt mode off!");
                    #msgBox2.exec();
                    messagebox.showinfo("Warning", "Warning encrypt mode off!")

            self.json_array = [ip, port, key_, iv_, hash, ipv6, self.noencryptmode];
            return self.json_array;
        except UnicodeDecodeError:
            if(noqeestionmode == 0):
                #msgBox2 = QtWidgets.QMessageBox();
                #msgBox2.setText("ERROR Connection File not corupt or passwor wrong!");
                #msgBox2.exec();
                messagebox.showinfo("ERROR", "ERROR Connection File not corupt or passwor wrong!")
            print("ERROR Connection File not corupt or passwor wrong!");
            return [];
        except IndexError:
            if(noqeestionmode == 0):
                #msgBox2 = QtWidgets.QMessageBox();
                #msgBox2.setText("ERROR Connection File not corupt or passwor wrong!");
                #msgBox2.exec();
                messagebox.showinfo("ERROR", "ERROR Connection File not corupt or passwor wrong!")
            print("ERROR Connection File not corupt or passwor wrong!");
            return [];


    def question_dns_or_ip(self):
        if(ip != ""):
            return 1;
        #msgBox2 = QtWidgets.QMessageBox();
        #msgBox2.setText("have you a dns?");
        tmp = self.my_yes_no_dialog("have you a dns?")
        #yesbuttom = QtWidgets.QPushButton("Yes");
        #nobuttom = QtWidgets.QPushButton("No");
        #yesbuttom = msgBox2.addButton("Yes", QtWidgets.QMessageBox.ButtonRole.AcceptRole);
        #nobuttom = msgBox2.addButton("No", QtWidgets.QMessageBox.ButtonRole.NoRole);


        #out = msgBox2.exec();
        if(tmp == 1):
            return 1;
        elif(tmp == 0):
            return 0;
        else:
            exit(-1);


    def question_port(self):
        if(port != -1):
            return port;
        i = tkinter.simpledialog.askinteger("Get integer", "Your port:");
        #i, okPressed = QtWidgets.QInputDialog.getInt(self, "Get integer","Your port:", 9044, 1, 65000, 1);
        if(i >= 1):
            if(i <= 65000):
                return i;
        else:
            exit(-1);

    def question_textbox(self):
        i = tkinter.simpledialog.askinteger("Get integer", "Your port:");
        #i, okPressed = QtWidgets.QInputDialog.getInt(self, "Get integer","Starten welcher gespeicherten Textboxen: ", 1, 1, 4, 1);
        if okPressed:
            if(i >= 1):
                if(i <= 4):
                    return i;
        else:
            exit(-1);

    def question_aes_key(self):
        if(aes_key != ""):
            return aes_key.encode();
        text = tkinter.simpledialog.askstring("Get text", "your aes key");
        #text, okPressed = QtWidgets.QInputDialog.getText(self, "Get text", "your aes key");
        if(text != ""):
            return self.key_size_anpassen(text.encode());
        else:
            exit(-1);

    def question_ip(self):
        if(ip != ""):
            return ip.encode();
        text = tkinter.simpledialog.askstring("Get text", "your ip or dns name");
        #text, okPressed = QtWidgets.QInputDialog.getText(self, "Get text", "your ip or dns name");
        if(text != ""):
            return text.encode();
        else:
            exit(-1);

    def question_iv_key(self):
        if(iv_key != ""):
            return iv_key.encode();
        text = tkinter.simpledialog.askstring("Get text", "your aes iv key");
        #text, okPressed = QtWidgets.QInputDialog.getText(self, "Get text", "your aes iv key");
        if(text != ""):
            return self.iv_size_anpassen(text.encode());
        else:
            exit(-1);

    def question_folder(self):
        while True:
            fieldialog = QtWidgets.QFileDialog;
            file = fieldialog.getExistingDirectory(self, "Sync Folder", "");
            if(os.path.isdir(str(file)) == True):
                return (str(file));

    def question_server_ipv6_or_ipv4(self):
        if(ip_mode !=  -1):
            return ip_mode;
        while True:
            text = tkinter.simpledialog.askstring("Get text",  "server on ipv6 (6) or ipv4 (4)?")
            #text, okPressed = QtWidgets.QInputDialog.getText(self, "Get text", "server on ipv6 (6) or ipv4 (4)?");
            if(text != ""):
                if(text == "4"):
                    return 4;
                elif(text == "6"):
                    return 6;
                else:
                    print("ERROR Falsche eingabe Bitte nocheinmal 4 oder 6 eingebn!");
            else:
                exit(-1);

    def start_listen_Server(self, port, ip_system):
        #ip_system = self.question_server_ipv6_or_ipv4();
        while True:
            try:
                if(ip_system == 4):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                    s.bind(("", port));
                    print("Server gestartet IPv4");
                    return s;
                elif(ip_system == 6):
                    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM);
                    s.bind(("", port));
                    print("Server gestartet IPv6");
                    return s;
            except OSError:
                print("Die Adresse wird bereits verwendet");
                time.sleep(60);
            except ConnectionResetError:
                print("Sync ERROR");
            except BrokenPipeError:
                return ""
        return -1;

    def read_connection_simple_mode(self, addr, komm):
        try:
            mode = "";
            while True:
                data = komm.recv(1).decode()
                if data == ";":
                    break;
                mode = mode + data;
            return mode;
        except ConnectionResetError:
            return "";
        except BrokenPipeError:
            return ""

    def wirte_connection_simple_mode(self, addr, komm, text):
        try:
            komm.send((text+";").encode());
            return 0;
        except ConnectionResetError:
            return "";
        except BrokenPipeError:
            return ""

    def remove_punkt_aes(self, s2):
        i = 0;
        s1 = "";
        while True:
            if(i >= len(s2)-4):
                break;
            s1 = s1 + s2[i];
            i =i +1;
        return s1;

    def send_encrypt(self, addr, s, aeskey, iv, messege):
        try:
            bout = self.bytes_encryption(aeskey ,iv, messege.encode());
            size = len(bout);
            self.wirte_connection_simple_mode(addr, s, str(size));
            s.send(bout);
            return 0;
        except ConnectionResetError:
            return "";
        except BrokenPipeError:
            return ""

    def recive_decrypt(self, addr, s, aeskey, iv):
        try:
            size = self.read_connection_simple_mode(addr, s);
            if(size == ""):
                return "";
            size = int(size);
            i = 0;
            b1 = b'';
            while True:
                if(i >= size):
                    break;
                b1 = b1 + s.recv(1);
                i = i +1;
            b1 = self.bytes_decryption(aeskey ,iv, b1);
            return b1.decode();
        except ConnectionResetError:
            return "";
        except BrokenPipeError:
            return ""

    def send_stream_encrypt(self, addr, s, aeskey, iv, messege):
        try:
            bout = self.bytes_encryption(aeskey ,iv, zstd.compress(messege));
            size = len(bout);
            self.wirte_connection_simple_mode(addr, s, str(size));
            s.send(bout);
            return 0;
        except ConnectionResetError:
            return "";
        except BrokenPipeError:
            return ""

    def recive_stream_decrypt(self, addr, s, aeskey, iv):
        try:
            size = self.read_connection_simple_mode(addr, s);
            if(size == ""):
                return "";
            size = int(size);
            i = 0;
            b1 = b'';
            block = 32;
            while True:
                if(i >= size):
                    break;
                if(i + block >= size):
                    sizetemp = size -i;
                else:
                    sizetemp = block;
                b2 = s.recv(sizetemp);
                sizetemp = len(b2);
                b1 = b1 + b2;
                i = i +sizetemp;
            b1 = self.bytes_decryption(aeskey ,iv, b1);
            return zstd.decompress(b1);
        except ConnectionResetError:
            return "";
        except BrokenPipeError:
            return ""

    def Clinet_file_upload_clinet(self, addr, s, aeskey, iv, folder, id):
        #upload
        #try:
            #self.aufraumen(folder);
            self.status_starttime = time.time()
            self.status_downloadedbytes = 0
            self.status_totaltransfertime = 0
            self.update_progress_info("upload file..",0, 100);
            block = server_block_übertragungs_länge;
            sdir = "";
            array = [0, sdir];
            if(len(self.listpatharray) == 0):
                self.listpatharray = self.listpath(folder, "", array, [], [], []);
            array = self.listpatharray;
            sdir = array[1];
            patharray = array[3];
            ctime = array[4];
            #print(sdir);
            sfileid = "";
            id = int(id);
            #print(folder);
            sfile = "";
            if(Betribsystem == False):
                sfile = folder + patharray[id];
            else:
                sfile = folder + self.flips_schlasch(patharray[id]);
            self.send_encrypt(addr, s,  aeskey, iv, patharray[id]);
            fobj = open(sfile, "rb");
            filename = sfile;
            hash = hashlib.sha256();
            fobj.seek(0, 2);
            size = fobj.tell();
            fobj.seek(0, 0);
            if(self.wirte_connection_simple_mode(addr, s, str(size)) == ""):
                print("ERROR Übertragung fehler");
                return -1;

            stinfo = os.stat(sfile);
            print("filename: ", sfile);
            time_1 = str(stinfo.st_atime) + "," + str(stinfo.st_mtime);
            if(self.wirte_connection_simple_mode(addr, s, time_1) == ""):
                print("ERROR Übertragung fehler");
                return -1;
            i = 0;
            sizetemp = 0;
            self.update_progress_info("file upload..",0, 100);
            size3 = 0;
            while True:
                if(i >= size):
                    break;
                if(i + block > size):
                    sizetemp = size -i ;
                else:
                    sizetemp = block;
                s1 = fobj.read(sizetemp);
                size3 = size3 + len(s1)
                hash.update(s1);
                if(test_fehelrmode == 1):
                    print("Test fehler erzeugt hash defck")
                    eroor_simulator_list = list(s1);
                    eroor_simulator = eroor_simulator_list[0] + 1;
                    if(eroor_simulator >= 255):
                        eroor_simulator = 0;
                    eroor_simulator_list[0] = eroor_simulator;
                    s1 = bytes(eroor_simulator_list);
                if(self.send_stream_encrypt(addr, s, aeskey, iv, s1) == ""):
                    print("ERROR Übertragung fehler");
                    #os.remove(filename);
                    return -1;
                i = i + sizetemp;
                timenow = time.time()
                self.status_downloadedbytes = i
                self.status_totaltransfertime = timenow - self.status_starttime;
                if(i != 0 and i % 45 == 0):
                    if(self.status_downloadedbytes != 0 and self.status_totaltransfertime != 0):
                        #size = 100
                        #self.status_downloadedbytes = X
                        if(size != 0):
                            self.zeit1 = self.status_downloadedbytes * 100 / size;
                        else:
                            self.zeit1 = 0;
                        #self.zeit1 =
                        #self.status_totaltransfertime =  self.zeit1
                        #X = 100%
                        if(self.zeit1 != 0 and self.status_totaltransfertime != 0 and self.status_starttime != 0):
                            self.zeit2 = self.status_totaltransfertime * (100 -self.zeit1)   / self.zeit1;
                        else:
                            self.zeit2 = 0;
                        #print("Zeit1: ", self.zeit1)
                        #print("Zeit2: ", self.zeit2)
                    s2 = float(i) * float(100) / float(size);
                    s1 = str(i) + "/" + str(size) + ":" + str(s2) + "%";
                    self.update_progress_info("file upload.." + " Zeit: ~" +  str(self.float_to_int(self.zeit2)) + "sec ", self.float_to_int(s2), 100, size3);
                    size3 = 0;
                    #print("upload: ", s1);
            fobj.close();
            print("upload: ", 100.0);
            self.update_progress_info("file upload..",100, 100);
            shash = hash.hexdigest();
            hash_  = shash;
            sok = self.read_connection_simple_mode(addr, s);
            if(sok == "OK"):
                self.send_encrypt(addr, s, aeskey, iv, hash_);
                b1 = self.read_connection_simple_mode(addr, s);
                if(b1 == ""):
                    print("ERROR Übertragung fehler");
                    #os.remove(filename);
                    self.aufraumen(folder);
                    s.close();
                    return -1;
                elif(b1 == "0"):
                    print(shash);
                    print("Ubertragung FAIL");
                    self.aufraumen(folder);
                    s.close();
                    #os.remove(filename);
                    return -1;
                else:
                    print("Ubertragung OK");
            #os.remove(sfileaes);
        #except:
        #    s.close();
        #    return -1;
            s.close();
            self.aufraumen(folder);
            return 0;


    def float_to_int(self, zahl):
        return math.floor(zahl)

    def Server_file_upload_client(self, addr, komm, aeskey, iv, folder):
        #download
        #try:
            #self.aufraumen(folder);
            self.status_starttime = time.time()
            self.status_downloadedbytes = 0
            self.status_totaltransfertime = 0
            block = server_block_übertragungs_länge;
            print("file encryption andere PC..");
            self.update_progress_info("file encryption andere PC..",0, 100);
            filename = self.recive_decrypt(addr, komm, aeskey, iv);
            #filename = self.read_connection_simple_mode(addr, komm);
            print("file encryption andere PC..ende");
            self.update_progress_info("file encryption andere PC..ende",100, 100);
            size = self.read_connection_simple_mode(addr, komm);
            if(size == ""):
                print("ERROR Übertragung fehler");
            size = int(size);
            ctime = self.read_connection_simple_mode(addr, komm);
            if(ctime == ""):
                print("ERROR Übertragung fehler");
            if(Betribsystem == False):
                filename = folder + filename;
            else:
                filename = folder + self.flips_schlasch(filename);
            dir = self.filepath_to_mkdirpath(filename);
            if(Betribsystem == False):
                os.system("mkdir -p " + "\"" + dir + "\"");
            else:
                os.system("mkdir " + "\"" + dir + "\"");
            print("filename: ", filename);
            filename_aes = filename + ".aes";
            fobj = open(filename_aes, "wb");
            hash = hashlib.sha256();
            data = "";
            i = 0;
            size_temp = 0;
            size3 = 0;
            self.update_progress_info("file download..",0, 100);
            while True:
                if(i >= size):
                    break;
                if(i + block >= size):
                    sizetemp = size - i;
                else:
                    sizetemp = block;
                data = self.recive_stream_decrypt(addr, komm, aeskey, iv);
                if(data == ""):
                    print("ERROR Übertragung fehler");
                    os.remove(filename_aes);
                    self.aufraumen(folder);
                sizetemp = len(data);
                hash.update(data);
                fobj.write(data);
                size3 = size3 + len(data)
                i = i +sizetemp;
                timenow = time.time()
                self.status_downloadedbytes = i
                self.status_totaltransfertime = timenow - self.status_starttime;
                if(i != 0 and i % 45 == 0):
                    if(self.status_downloadedbytes != 0 and self.status_totaltransfertime != 0):
                        if(size != 0):
                            self.zeit1 = self.status_downloadedbytes * 100 / size;
                        else:
                            self.zeit1 = 0;
                        if(self.zeit1 != 0 and self.status_totaltransfertime != 0 and self.status_starttime != 0):
                            self.zeit2 = self.status_totaltransfertime * (100 -self.zeit1)   / self.zeit1;
                        else:
                            self.zeit2 = 0;
                        #print("Zeit1: ", self.zeit1)
                        #print("Zeit2: ", self.zeit2)
                        s2 = float(i) * float(100) / float(size);
                        s1 = str(i) + "/" + str(size) + ":" + str(s2) + "%";
                        #print("Downlaod: ", s1);
                        self.update_progress_info("file download.." + " Zeit: ~" +  str(self.float_to_int(self.zeit2)) + "sec ", self.float_to_int(s2), 100, size3);
                        size3 = 0;
            hash_ = hash.hexdigest();
            fobj.close();
            if(self.wirte_connection_simple_mode(addr, komm, "OK") == ""):
                print("ERROR Übertragung fehler");
                #os.remove(filename_aes);
                self.aufraumen(folder);
                return -1;


            shash = self.recive_decrypt(addr, komm, aeskey, iv);
            if(shash == ""):
                print("ERROR Übertragung fehler");
                #os.remove(filename_aes);
                self.aufraumen(folder);
                return -1;
            if(shash == hash_):
                print("Ubertragung OK");
                if(os.path.isfile(filename) == True):
                    os.remove(filename);
                os.rename(filename_aes, filename);
                if(self.wirte_connection_simple_mode(addr, komm, "1") == ""):
                    print("ERROR Übertragung fehler");
                    #os.remove(filename_aes);
                    self.aufraumen(folder);
                    return -1;
            else:
                print(shash);
                print(hash_);
                print("Ubertragung FAIL");
                if(self.wirte_connection_simple_mode(addr, komm, "0") == ""):
                    print("ERROR Übertragung fehler");
                    #os.remove(filename_aes);
                    self.aufraumen(folder);
                    return -1;
                print(filename);
                #os.remove(filename_aes);
                komm.close();
                self.aufraumen(folder);
                return -1;
            ctime = ctime.split(",");
            os.utime(filename,(float(ctime[0]), float(ctime[1])));
            komm.close();
            self.aufraumen(folder);
            return 0;
        #except:
        #    komm.close();
        #    return -1;
        #    komm.close();
        #    return 0;
    def clinet_sync(self, addr, komm, aeskey, iv, folder):
        dwid = [];
        up = [];
        paths_dwid = [];
        paths_up = [];
        up_size = [];
        dwid_size = [];
        size2 =  self.read_connection_simple_mode(addr, komm);
        size2 = int(size2);
        i = 0;
        while True:
            if(i >= size2):
                break;
            sfilepath = "";
            sfilepath = self.recive_decrypt(addr, komm, aeskey, iv);
            file_timestampserver = self.read_connection_simple_mode(addr, komm);
            spath = folder + sfilepath;
            servetime = file_timestampserver.split(",");
            atime = float(servetime[0]);
            mtime = float(servetime[1]);
            clientst_atime = 0.0;
            clientst_mtime = 0.0;
            if(os.path.isfile(spath) == True):
                stinfo = os.stat(spath);
                clientst_atime= float(stinfo.st_atime);
                clientst_mtime = float(stinfo.st_mtime);
            else:
                server_hash = self.read_connection_simple_mode(addr, komm);
                size = self.read_connection_simple_mode(addr, komm);
                dwid.append(i);
                paths_dwid.append(sfilepath);
                dwid_size.append(int(size));
                self.wirte_connection_simple_mode(addr, komm, "1");
                i = i +1;
                continue;
            fobj = open(spath, "rb");
            hash = hashlib.sha256();
            fobj.seek(0, 2);
            size = fobj.tell();
            fobj.seek(0, 0);
            block = 1024*1024;
            k = 0;
            sizetemp = 0;
            while True:
                sizetemp = 0;
                if(k >= size):
                    break;
                if( k + block <= size):
                    sizetemp = block;
                elif(k + block > size):
                    sizetemp = size - k;
                s1 = fobj.read(sizetemp);
                hash.update(s1);
                k = k + sizetemp;
                if(k != 0 and k % 1500000 == 0):
                    sx1 = float(k) * float(100) / float(size);
                    s1 = str(k) + "/" + str(size) + ":" + str(sx1) + "%";
                    print("checksums: ", sx1);
            fobj.close();
            shash = hash.hexdigest();
            hash_  = shash;
            server_hash = self.read_connection_simple_mode(addr, komm);
            size = self.read_connection_simple_mode(addr, komm);
            print("hash clinet: ", hash_);
            print("hash server: ", server_hash);
            if(hash_ != server_hash):
                if(mtime  > clientst_mtime):
                    dwid.append(str(i));
                    dwid_size.append(int(size));
                    paths_dwid.append(sfilepath);
                elif(mtime  < clientst_mtime):
                    sdir  = "";
                    array = [0, sdir];
                    if(len(self.listpatharray) == 0):
                        self.listpatharray = self.listpath(folder, "", array, [], [], []);
                    array = self.listpatharray;
                    sdir = array[1];
                    patharray = array[3];
                    idarray = array[2];
                    sfileid = "";
                    j = 0;
                    while True:
                        if(j >= len(idarray)):
                            break;
                        if(patharray[j] == sfilepath):
                            up.append(str(j));
                            up_size.append(int(size));
                            paths_up.append(sfilepath);
                        elif(patharray[j] == self.flips_schlasch(sfilepath)):
                            up.append(str(j));
                            up_size.append(int(size));
                            paths_up.append(sfilepath);
                        j = j +1;
                else:
                    dwid.append(str(i));
                    paths_dwid.append(sfilepath);
            self.wirte_connection_simple_mode(addr, komm, "1");
            i = i +1;
        self.maxsize_array = [up_size, dwid_size];
        self.calulate_array_maxsize();
        self.wirte_connection_simple_mode(addr, komm, str(self.calulate_max_size));
        self.calulate_size = 0;
        komm.close();
        print("clinet_sync ende");
        return [dwid, up, paths_dwid, paths_up];

    def clinet_sync_add(self, addr, komm, aeskey, iv, folder):
        print("clinet_sync_add start")
        up = [];
        up_size = [];
        paths_up = [];
        sdir  = "";
        array = [0, sdir];
        if(len(self.listpatharray) == 0):
            self.listpatharray = self.listpath(folder, "", array, [], [], []);
        array = self.listpatharray;
        sdir = array[1];
        ctime = array[4];
        patharray = array[3];
        idarray = array[2];
        sfileid = "";
        size2 = len(idarray);
        if(self.wirte_connection_simple_mode(addr, komm, str(size2)) == ""):
            return -1;
        i = 0;
        while True:
            if(i >= size2 ):
                break;
            sdata = "";
            if(Betribsystem == False):
                sdata = patharray[i];
            else:
                sdata = patharray[i];
            self.send_encrypt(addr, komm, aeskey, iv, sdata);
            sfilepath = sdata;
            spath = "";
            if(Betribsystem == False):
                spath = folder + sfilepath;
            else:
                spath = folder + self.flips_schlasch(sfilepath);
            check = self.read_connection_simple_mode(addr, komm);
            if(check == "0"):
                up.append(str(i));
                paths_up.append(patharray)
                if(os.path.isfile(spath) == True):
                    f1 = open(spath, "r");
                    f1.seek(0, 2);
                    size3 = f1.tell();
                    f1.close();
                    up_size.append(int(size3))
                else:
                    up_size.append(int(0))
            i = i +1;
        self.maxsize_array = [up_size, []];
        self.calulate_array_maxsize();
        self.wirte_connection_simple_mode(addr, komm, str(self.calulate_max_size));
        komm.close();
        self.calulate_size = 0;
        print("clinet_sync_add ende");
        return [[], up, [], paths_up];


    def server_sync_add(self, addr, komm, aeskey, iv, folder):
        size = self.read_connection_simple_mode(0, komm)
        if(size == ""):
            return -1;
        size = int(size);
        size2 = "";
        i = 0;
        while True:
            if( i>= size):
                break;
            sfilepath = "";
            sfilepath = self.recive_decrypt(addr, komm, aeskey, iv);
            spath = "";
            if(Betribsystem == False):
                spath = folder + sfilepath;
            else:
                spath = folder + self.flips_schlasch(sfilepath);
            if(os.path.isfile(spath) == True):
                self.wirte_connection_simple_mode(addr, komm, "1");
            else:
                self.wirte_connection_simple_mode(addr, komm, "0");
            i = i +1;
        self.calulate_max_size = int(self.read_connection_simple_mode(0, komm));
        komm.close();
        self.calulate_size = 0;
        return 0;


    def server_sync(self, addr, komm, aeskey, iv, folder):
        sdir  = "";
        array = [0, sdir];
        if(len(self.listpatharray) == 0):
            self.listpatharray = self.listpath(folder, "", array, [], [], []);
        array = self.listpatharray;
        sdir = array[1];
        ctime = array[4];
        patharray = array[3];
        idarray = array[2];
        size2 = len(idarray);
        if(self.wirte_connection_simple_mode(addr, komm, str(size2)) == ""):
            return -1;
        i  = 0;
        while True:
            if(i >= size2):
                break;
            sdata = patharray[i];
            self.send_encrypt(addr, komm, aeskey, iv, sdata);
            s1 = "";
            if(Betribsystem == False):
                s1 = folder + patharray[i];
            else:
                s1 = folder + self.flips_schlasch(patharray[i]);
            stinfo = os.stat(s1);
            time_1 = str(stinfo.st_atime) + "," + str(stinfo.st_mtime);
            self.wirte_connection_simple_mode(addr, komm, time_1);
            fobj = open(s1, "rb")
            hash = hashlib.sha256();
            fobj.seek(0, 2);
            size = fobj.tell();
            fobj.seek(0, 0);
            block = 1024*1024;
            k = 0;
            sizetemp = 0;
            while True:
                sizetemp = 0;
                if( k >= size):
                    break;
                if( k + block <= size):
                    sizetemp = block;
                elif(k + block > size):
                    sizetemp = size - k;
                s1 = fobj.read(sizetemp);
                hash.update(s1);
                k = k + sizetemp;
                if(k != 0 and i % 1500000 == 0):
                    s2 = float(k) * float(100) / float(size);
                    s1 = str(k) + "/" + str(size) + ":" + str(s2) + "%";
                    print("Checksume: ",s1);
            fobj.close();
            shash = hash.hexdigest();
            self.wirte_connection_simple_mode(addr, komm, shash);
            self.wirte_connection_simple_mode(addr, komm, str(size))
            b1 = self.read_connection_simple_mode(addr, komm);
            i = i +1;
        self.calulate_size = 0;
        self.calulate_max_size = int(self.read_connection_simple_mode(0, komm));
        komm.close();
        print("server_sync ende");
        return 0;



    def server_liste_senden(self, addr, komm, aeskey, iv, folder):
        #ls server files
        sdir = "";
        array = [0, sdir];
        if(len(self.listpatharray) == 0):
            self.listpatharray = self.listpath(folder, "", array, [], [], []);
        array = self.listpatharray;
        sdir = array[1];
        self.send_encrypt(addr, komm, aeskey, iv, sdir.encode());
        #self.wirte_connection_simple_mode(addr, komm, sdir);
        komm.close();
        return 0;

    def start_Clinet_prozess(self, mode, id, folder, myip, key_, iv_, port, ipv6):
        i = 0;
        while True:
            tmp = self.start_Clinet_prozess_2(mode, id, folder, myip, key_, iv_, port, ipv6);
            if(len(tmp) == 1):
                if(tmp[0] == -1):
                    time.sleep(1);
                    i = i +1;
                    if(i >= 25):
                        return [-1];
                elif(tmp[0] == -2):
                    i = 0;
                else:
                    return tmp;
            else:
                return tmp;
            time.sleep(1);
            i = i +1;
            if(i >= 25):
                return [-1];

    def client_socket_connect(self, myip, port, ipv6):
        try:
            if(ipv6 == 6):
                print("Cleint conenct with ipv6")
                s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM);
                s.connect((myip, port));
                return s;
            else:
                print("Cleint conenct with ipv4")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                s.connect((myip, port));
                return s;
        except OSError:
            print("ERROR no Server found!");
            if(noqeestionmode == 0):
                #msgBox2 = QtWidgets.QMessageBox();
                #msgBox2.setText("ERROR no Server found!");
                #msgBox2.exec();
                messagebox.showinfo("ERROR", "ERROR no Server found!")
            return -1;
    def start_Clinet_prozess_2(self, mode, id, folder, myip, key_, iv_, port, ipv6):
        self.aufraumen(folder);
        s = self.client_socket_connect(myip, port, ipv6);
        if(s == -1):
            return [-1];
        if(mode == "10"):
            #connection file download
            self.wirte_connection_simple_mode(0, s, "0");
            b1 = self.read_connection_simple_mode(0, s);
            spath = os.path.join(folder, "1.txt");
            if(Betribsystem == True):
                spath = self.flips_schlasch(spath);
            file1 = open(spath, "w");
            file1.write(b1);
            file1.close();
            s.close();
            return [];
        self.wirte_connection_simple_mode(0, s, "1");
        key = self.recive_stream_decrypt(0, s, key_, iv_);
        iv = self.recive_stream_decrypt(0, s, key_, iv_);
        #print(len(key));
        #print(len(iv));
        if(mode == "1"):
            #up
            self.send_encrypt(0, s, key, iv, "1");
            while True:
                if(self.Clinet_file_upload_clinet(0, s, key, iv, folder, id) == 0):
                    break;
                else:
                    return [-2];

        elif(mode == "3"):
            self.send_encrypt(0, s, key, iv, "3");
            sdir = self.read_connection_simple_mode(0, s);
            #print(sdir);
        elif(mode == "4"):
            #dwid
            self.send_encrypt(0, s, key, iv, "4");
            self.wirte_connection_simple_mode(0, s, id);
            while True:
                if(self.Server_file_upload_client(0, s, key, iv, folder) == 0):
                    break;
                else:
                    return [-2];
        elif(mode == "5"):
            #sync
            self.send_encrypt(0, s, key, iv, "5");
            array = self.clinet_sync(0, s, key, iv, folder);
            s.close();
            return array;
        elif(mode == "7"):
            #sync add
            self.send_encrypt(0, s, key, iv, "7");
            array = self.clinet_sync_add(0, s, key, iv, folder);
            s.close();
            return array;
        elif(mode == "8"):
            #server size of file server
            self.send_encrypt(0, s, key, iv, "8");
            self.wirte_connection_simple_mode(0, s, str(self.maxfilecount));
            s.close();
            return [];
        elif(mode == "9"):
            self.send_encrypt(0, s, key, iv, "9");
            self.wirte_connection_simple_mode(0, s, version);
            tmp = self.read_connection_simple_mode(0, s);
            if(tmp == "0"):
                print("ERROR version nicht comptible!");
                s.close();
                if(noqeestionmode == 0):
                    #msgBox2 = QtWidgets.QMessageBox();
                    #msgBox2.setText("ERROR version nicht comptible!");
                    #msgBox2.exec();
                    messagebox.showinfo("ERROR", "ERROR version nicht comptible!")
                return [-1];
            s.close();
            return [];





        s.close();
        self.aufraumen(folder);
        return [];


    def start_Client(self, mode, id, folder, aes_key, iv_):
        stxt = os.path.join(folder, "1.txt");
        #if(os.path.isfile(stxt) == True):
        #    os.remove(stxt)
        self.json_array = [];

        self.vorschau_bak = self.vorschau;



        while True:
            b1 = 0;
            if(Betribsystem == True):
                #windows
                folder = self.flips_schlasch(folder);
            self.filecount = 0;
            self.maxfilecount = 0;
            #folder = self.question_folder();
            self.aufraumen(folder);
            #print("folder: ", folder);
            #aes_key = self.question_aes_key();
            #iv_ = self.question_iv_key();
            connection_file = self.read_Connetion_file(folder, aes_key, iv_);
            if(len(connection_file) != 0):
                myip = connection_file[0];
                port = connection_file[1];
                key = connection_file[2];
                iv =  connection_file[3];
                ipv6 = connection_file[5];
                #print(connection_file);
                tmp = self.start_Clinet_prozess("10", "0", folder, myip, key, iv, port, ipv6);
                if(len(tmp) == 1):
                    if(tmp[0] == -1):
                        myip = self.question_ip();
                        port = self.question_port();
                        key = "";
                        iv = "";
                        tmp = self.start_Clinet_prozess("10", "0", folder, myip, key, iv, port, ipv6);
                        if(len(tmp) == 1):
                            if(tmp[0] == -1):
                                self.mesage_eroor();
                                return -1;
            else:
                myip = self.question_ip();
                port = self.question_port();
                ipv6 = self.question_server_ipv6_or_ipv4();
                key = "";
                iv = "";
                tmp = self.start_Clinet_prozess("10", "0", folder, myip, key, iv, port, ipv6);
                if(len(tmp) == 1):
                    if(tmp[0] == -1):
                        self.mesage_eroor();
                        return -1;

            tmp = self.start_Clinet_prozess("10", "0", folder, myip, key, iv, port, ipv6);
            if(len(tmp) == 1):
                if(tmp[0] == -1):
                    myip = self.question_ip();
                    port = self.question_port();
                    key = "";
                    iv = "";
                    tmp = self.start_Clinet_prozess("10", "0", folder, myip, key, iv, port, ipv6);
            connection_file = self.read_Connetion_file(folder, aes_key, iv_);
            if(len(connection_file) == 0):
                return -1;
            myip = connection_file[0];
            port = connection_file[1];
            key = connection_file[2];
            iv =  connection_file[3];
            ipv6 = connection_file[5];
            self.noencryptmode = connection_file[6];
            #print(connection_file);
            tmp = self.start_Clinet_prozess("9", "0", folder, myip, key, iv, port, ipv6);
            if(tmp == -1):
                self.mesage_eroor();
                return -1;
            array = self.start_Clinet_prozess(mode, id, folder, myip, key, iv, port, ipv6);
            if(len(array) != 0):
                dwid = array[0];
                up = array[1];
                if(len(dwid) == 0 and len(up) == 0):
                    b1 = 1;
                self.filecount = 0;
                self.maxfilecount = len(up) + len(dwid);
                if(self.start_Clinet_prozess("8", "0", folder, myip, key, iv, port, ipv6) == -1):
                    self.mesage_eroor();
                    return -1;
                #server size of file server
                #print("dwid: ", dwid);
                #print("up: ", up);
                if(self.vorschau_bak == True):
                    self.vorschau_bak = False;
                    self.prozess_vorschau(array);
                for tmp in dwid:
                    if(self.start_Clinet_prozess("4", str(tmp), folder, myip, key, iv, port, ipv6) == -1):
                        self.mesage_eroor();
                        return -1;
                    self.filecount = self.filecount + 1;
                for tmp in up:
                    if(self.start_Clinet_prozess("1",  str(tmp), folder, myip, key, iv, port, ipv6) == -1):
                        self.mesage_eroor();
                        return -1;
                    self.filecount = self.filecount + 1;
                #sync add
                self.filecount = 0;
                array_tmp = self.start_Clinet_prozess("7",  "0", folder, myip, key, iv, port, ipv6);
                if(array == -1):
                    self.mesage_eroor();
                    return -1;
                array = array_tmp[1];
                if(self.vorschau_bak == True):
                    self.vorschau_bak = False;
                    self.prozess_vorschau(array);
                self.maxfilecount = len(array);
                if(self.start_Clinet_prozess("8", "0", folder, myip, key, iv, port, ipv6) == -1):
                    self.mesage_eroor();
                    return -1;
                #server size of file server
                print("sync_add: ", array);
                self.listpatharray = [];
                for tmp in array:
                    self.filecount = self.filecount + 1;
                    if(self.start_Clinet_prozess("1",  str(tmp), folder, myip, key, iv, port, ipv6) == -1):
                        self.mesage_eroor();
                        return -1;
                self.maxfilecount = 0;
                self.filecount = 0;
                if(self.start_Clinet_prozess("8", "0", folder, myip, key, iv, port, ipv6) == -1):
                    self.mesage_eroor();
                    return -1;
                print("sync ende")
            if(b1 == 1):
                self.aufraumen(folder);
                break;
        stxt = os.path.join(folder, "1.txt");
        #if(os.path.isfile(stxt) == True):
        #    os.remove(stxt)
        return 0;



    def start_Server(self):
        if(serverstartautodir != ""):
            self.json_array = [];
            self.listpatharray = [];
            self.button_start_Server.setDisabled(True);
            self.button_start_Client.setDisabled(True);
            ip_system = self.question_server_ipv6_or_ipv4();
            self.b1 = 1;
            #folder = self.question_folder();
            aes_key = self.question_aes_key();
            iv_ = self.question_iv_key();
            text = [];
            self.textedit_Verzeichniss1 = serverstartautodir;
            self.start_Server_prozess(self.textedit_Verzeichniss1, aes_key, iv_, ip_system);
            exit();
        if(testmode != 1):
            self.sav();
        self.json_array = [];
        self.listpatharray = [];
        #self.button_start_Server.setDisabled(True);
        #self.button_start_Client.setDisabled(True);
        ip_system = self.question_server_ipv6_or_ipv4();
        self.b1 = 1;
        #folder = self.question_folder();
        aes_key = self.question_aes_key();
        iv_ = self.question_iv_key();
        text = [];
        if(self.textedit_Verzeichniss1 != ""):
            text.append(1);

        if(len(text) == 1):
            if(text[0] == 1):
                self.json_array = [];
                self.listpatharray = [];
                self.start_Server_prozess(self.textedit_Verzeichniss1, aes_key, iv_, ip_system);
        elif(len(text) == 0):
            if(noqeestionmode == 0):
                #msgBox2 = QtWidgets.QMessageBox();
                #msgBox2.setText("All Textboxen is empty. please click browse!");
                #msgBox2.exec();
                messagebox.showinfo("ERROR", "All Textboxen is empty. please click browse!")
            return -1;
        else:
            while True:
                i = self.question_textbox();
                for tmp in text:
                    if(tmp == i):
                        if(text[0] == 1):
                            self.listpatharray = [];
                            self.json_array = [];
                            self.start_Server_prozess(self.textedit_Verzeichniss1, aes_key, iv_, ip_system);

        if(testmode != 1):
            self.sav();
        self.update_progress_info("sync ende", 0, 100);
        self.listpatharray = [];
        self.button_start_Server.setDisabled(False);
        self.button_start_Client.setDisabled(False);
        return 0;

    def server_read_connectionfile(self, folder, aes_key, iv_):
        stxt = "";
        if(Betribsystem == True):
            #widnwos
            stxt = folder + "\1.txt";
        else:
            #Linux
            stxt = folder + "/1.txt";
        if(os.path.isfile(stxt) == True):
            connection_file = self.read_Connetion_file(folder, aes_key, iv_);
            if(len(connection_file) != 0 and testmode == 0 and self.question_dns_or_ip() == 1):
                myip = self.question_ip();
                port = connection_file[1];
                aes_key_new = connection_file[2];
                newiv = connection_file[3];
                ipv6 = self.question_server_ipv6_or_ipv4();
                #print(connection_file);
                self.create_Connetion_file(aes_key, iv_, myip.decode(), port, folder, aes_key_new, newiv, ipv6);
                return(self.read_Connetion_file(folder, aes_key, iv_));
            else:
                myip = requests.get('https://www.wikipedia.org').headers['X-Client-IP'].encode("utf-8");
                ipv6 = self.question_server_ipv6_or_ipv4();
                if(testmode == 1 and ip != "" and self.b1 != 2):
                    myip = ip;
                    if(noqeestionmode == 0):
                        msgBox2 = QtWidgets.QMessageBox();
                        msgBox2.setText("Test Mode aktivirt! force ip: "+ myip);
                        msgBox2.exec();
                    self.b1 = 2;
                elif(testmode == 1 and self.b1 != 2):
                    myip = "127.0.0.1";
                    #myip = "192.168.111.30"
                    if(noqeestionmode == 0):
                        msgBox2 = QtWidgets.QMessageBox();
                        msgBox2.setText("Test Mode aktivirt!");
                        msgBox2.exec();
                    self.b1 = 2;
                port = self.question_port();
                aes_key_new = os.urandom(64);
                newiv = os.urandom(16);
                #ipv6 = connection_file[5];
                print(connection_file);
                self.create_Connetion_file(aes_key, iv_, myip.decode(), port, folder, aes_key_new, newiv, ipv6);
                return(self.read_Connetion_file(folder, aes_key, iv_));

        else:
            if(noqeestionmode == 0):
                #msgBox2 = QtWidgets.QMessageBox();
                #msgBox2.setText("Conection file (1.txt) not found in the fodler. the APP create a neu 1.txt fiel in the fodler. you must send the 1.txt to teh clinet");
                #msgBox2.exec();
                messagebox.showinfo("ERROR", "Conection file (1.txt) not found in the fodler. the APP create a neu 1.txt fiel in the fodler. you must send the 1.txt to teh clinet")
            print("Conection file (1.txt) not found in the fodler. the APP create a neu 1.txt fiel in the fodler. you must send the 1.txt to teh clinet");
            connection_file = [];
            if(self.question_dns_or_ip() == 1):
                myip = self.question_ip();
                ipv6 = self.question_server_ipv6_or_ipv4();
                port = self.question_port();
                aes_key_new = os.urandom(64);

                newiv = os.urandom(16);
                self.create_Connetion_file(aes_key, iv_, myip.decode(), port, folder, aes_key_new, newiv, ipv6);
                return(self.server_read_connectionfile(folder, aes_key, iv_));
            else:
                myip = requests.get('https://www.wikipedia.org').headers['X-Client-IP'].encode("utf-8");
                ipv6 = self.question_server_ipv6_or_ipv4();
                if(testmode == 1 and self.b1 != 2):
                    myip = "127.0.0.1";
                    if(noqeestionmode == 0):
                        msgBox2 = QtWidgets.QMessageBox();
                        msgBox2.setText("Test Mode aktivirt!");
                        msgBox2.exec();
                    self.b1 = 2;
                port = self.question_port();
                aes_key_new = os.urandom(256);

                newiv = os.urandom(16);
                self.create_Connetion_file(aes_key, iv_, myip.decode(), port, folder, aes_key_new, newiv, ipv6);
                return(self.read_Connetion_file(folder, aes_key, iv_));
            return 0;

    def start_Server_prozess(self, folder, aes_key, iv_, ip_system):
        stxt = os.path.join(folder, "1.txt");
        if(os.path.isfile(stxt) == True):
            os.remove(stxt)
        self.aufraumen(folder);
        if(Betribsystem == True):
            #widnows
            folder = self.flips_schlasch(folder);
        connection_file = self.server_read_connectionfile(folder, aes_key, iv_);
        myip = connection_file[0];
        port = connection_file[1];
        key2 = connection_file[2];
        iv2 =  connection_file[3];
        ipv6 = connection_file[5];
        #print(connection_file);
        server = self.start_listen_Server(port, ipv6);
        while True:
            self.update_progress_info("Server listen..", 0, 100);
            server.listen(1);
            komm, addr = server.accept();
            #server_socket = server[0];
            #server_connection = server[1];
            #server_addr = server[2];
            #print(server);
            #print(server_connection);
            #mode = self.read_connection_simple_mode(0, komm);
            connectifileexist = self.read_connection_simple_mode(0, komm);
            if(connectifileexist == "0"):
                spath = os.path.join(folder, "1.txt");
                if(Betribsystem == True):
                    spath = self.flips_schlasch(spath);
                file1 = open(spath, "r");
                file1.seek(0, 2);
                size = file1.tell();
                file1.seek(0, 0);
                b1 = file1.read(size);
                file1.close();
                self.wirte_connection_simple_mode(0, komm, b1);
                komm.close();
            else:
                key = os.urandom(512);
                iv = os.urandom(16);
                self.send_stream_encrypt(0, komm, key2, iv2, key);
                self.send_stream_encrypt(0, komm, key2, iv2, iv);
                mode = self.recive_decrypt(0, komm, key, iv);
                if(mode == "1"):
                    #file upload Client
                    self.Server_file_upload_client(0, komm, key, iv, folder);
                    self.filecount = self.filecount + 1;
                elif(mode == "3"):
                    self.server_liste_senden(0, komm, key, iv, folder);
                elif(mode == "4"):
                    id = self.read_connection_simple_mode(0, komm);
                    self.Clinet_file_upload_clinet(0, komm, key, iv, folder, id);
                    self.filecount = self.filecount + 1;
                elif(mode == "5"):
                    self.listpatharray = []
                    self.update_progress_info("start sync.. ",0, 100);
                    self.listpatharray = []
                    self.server_sync(0, komm, key, iv, folder);
                    self.listpatharray = []
                    self.update_progress_info("start sync.. ende",100, 100);
                    self.listpatharray = []
                elif(mode == "7"):
                    self.listpatharray = []
                    self.update_progress_info("start sync add.. ",0, 100);
                    self.listpatharray = []
                    self.server_sync_add(0, komm, key, iv, folder);
                    self.listpatharray = []
                    self.update_progress_info("start sync add.. ende",0, 100);
                    self.listpatharray = []
                elif(mode == "8"):
                    #server size of file server
                    self.update_progress_info("start size of files.. ",0, 100);
                    tmp = self.read_connection_simple_mode(0, komm);
                    tmp = int(tmp);
                    komm.close();
                    self.update_progress_info("start size of files.. ",100, 100);
                    self.maxfilecount = tmp;
                    self.filecount = 1;
                elif(mode == "9"):
                    self.update_progress_info("start version check.. ",0, 100);
                    tmp = self.read_connection_simple_mode(0, komm);
                    if(tmp == version):
                        self.wirte_connection_simple_mode(0, komm, "1");
                        self.update_progress_info("start version check.. ok",100, 100);
                        print("start version check.. OK");
                    else:
                        self.wirte_connection_simple_mode(0, komm, "0");
                        self.update_progress_info("start version check.. ERROR",100, 100);
                        print("start version check.. ERROR");
                    komm.close();
        self.aufraumen(folder);
        stxt = os.path.join(folder, "1.txt");
        if(os.path.isfile(stxt) == True):
            os.remove(stxt)
        return 0;

    def string_to_hash(self, s1):
        hash = hashlib.sha256();
        hash.update(s1);
        return binascii.unhexlify(hash.hexdigest());

    def file_hash(self, fielpath):
        block = 1024;
        filein = open(fielpath, "rb");
        filein.seek(0, 2);
        size = "";
        size = filein.tell();
        filein.seek(0, 0);
        hash = hashlib.sha256();
        i = 0;
        while True:
            if(i >= size):
                break;
            if(i + block >= size):
                size_temp = size -i;
            else:
                 size_temp = block;
            sin = filein.read(size_temp);
            hash.update(sin);
            i = i + size_temp;
        return hash.hexdigest();



    def file_decrypt(self, key, iv, fileinpath, fileoutpath):
        print("Decrypt file: " + fileinpath);
        backend = default_backend();
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend);
        decryptor = cipher.decryptor();
        block = 32;
        filein = open(fileinpath, "rb");
        fileout = open(fileoutpath, "wb");
        filein.seek(0, 2);
        size = "";
        size = filein.tell();
        filein.seek(0, 0);
        if(size == 0):
            filein.close();
            fileout.close();
            return 0;
        key_ = decryptor.update(filein.read(32));
        iv_ = decryptor.update(filein.read(16));
        decryptor.finalize();
        backend = default_backend();
        cipher = Cipher(algorithms.AES(key_), modes.CBC(iv_), backend=backend);
        decryptor = cipher.decryptor();
        size = "";
        while True:
            b1 = filein.read(1).decode();
            if(b1 == "#"):
                break;
            size = size  + b1;
        #print(size);
        size = int(size);
        i = 0;
        while True:
            if(i >= size):
                break;
            if(i + block >= size):
                size_temp = size -i;
            else:
                 size_temp = block;
            #print("sizetemp: ", size_temp);
            sin = filein.read(32);
            #sin = filein.read(size_temp);
            #print(len(sin));
            if(size_temp == block):
                sout = decryptor.update(sin);
                fileout.write(sout)
            else:
                #print(len(sin));
                sout = decryptor.update(sin);
                a = self.analyse(sout);
                #print("a: ", a);
                sout = self.copy(sout, a);
                fileout.write(sout);
            i = i + size_temp;
        sout = decryptor.finalize();
        fileout.write(sout);
        fileout.close();
        filein.close();
        print("Decrypt file ende");
        return self.file_hash(fileoutpath);

    def file_encrypt(self, key, iv, fileinpath, fileoutpath):
        print("Encrypt file: " + fileinpath);
        backend = default_backend();
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend);
        encryptor = cipher.encryptor();
        block = 32;
        filein = open(fileinpath, "rb");
        fileout = open(fileoutpath, "wb");
        filein.seek(0, 2);
        size = filein.tell();
        filein.seek(0, 0);

        if(size == 0):
            filein.close();
            fileout.close();
            return 0;
        key_ = os.urandom(32);
        iv_ = os.urandom(16);
        fileout.write(encryptor.update(key_));
        fileout.write(encryptor.update(iv_));
        encryptor.finalize();
        backend = default_backend();
        cipher = Cipher(algorithms.AES(key_), modes.CBC(iv_), backend=backend);
        encryptor = cipher.encryptor();
        fileout.write( ( str(size) + "#" ).encode());
        i = 0;
        while True:
            if(i >= size):
                break;
            if(i + block >= size):
                size_temp = size -i;
            else:
                 size_temp = block;
            #print("sizetemp: ", size_temp);
            sin = self.data_array_Schreiben(filein.read(size_temp));
            #sin = filein.read(size_temp);
            #print(len(sin));
            if(size_temp == block):
                sout = encryptor.update(sin);
                fileout.write(sout)
            else:
                print(len(sin));
                sout = encryptor.update(sin);
                fileout.write(sout);
            i = i + size_temp;
        sout = encryptor.finalize();
        fileout.write(sout);
        fileout.close();
        filein.close();
        print("Encrypt file ende");
        return self.file_hash(fileinpath);

    def copy(self, sin, size):
        out = [];
        i = 0;
        while True:
            if(i >= len(sin)):
                break;
            if(i >= size):
                break;
            out.append(sin[i]);
            i = i +1;
        return bytes(out);

    def analyse(self, sout):
        out = sout;
        i = len(out) -1;
        while True:
            if(i <= 0):
                break;
            if(out[i] == trenner[0]):
                return i;
            i = i -1;
        return -1;


    def array_remove(self, array, size):
        out_a = "";
        i = 0;
        while True:
            if(i >= len(array)):
                break;
            if(i >= size):
                break;
            if(size == len(out_a)):
                break;
            out_a = out_a + array[i];
            i = i +1;
        return out_a.encode();

    def key_size_anpassen(self, key):
        if(len(key) > 32):
            key = self.array_remove(key, 32);
        while True:
            if(len(key) == 32):
                break;
            key = key + " ".encode();
        return key;

    def iv_size_anpassen(self, key):
        if(len(key) > 16):
            key = self.array_remove(key, 16);
        while True:
            if(len(key) == 16):
                break;
            key = key + " ".encode();
        return key;

    def data_array_Schreiben(self, indata):
        b1 = b" ";
        bool1 = 0;
        while True:
            if(len(indata) >= 32):
                break;
            if(bool1 == 0):
                bool1 = 1;
                indata = indata  + trenner;
            else:
                indata = indata  + b1;
        return indata;
    def update_ip(self):
        myip = requests.get('https://www.wikipedia.org').headers['X-Client-IP']
        return myip;

    def string_to_hex(self, s1):
        return binascii.hexlify(s1).decode();

    def hex_to_String(self, hex):
        return binascii.unhexlify(hex);

    def create_Connetion_file(self, aeskey, iv, myip, port, folder, newkey, newiv, ipv6):
        stxt = os.path.join(folder, "1.txt");
        hash_aes_key = hashlib.sha256();
        hash_aes_key.update(str(myip).encode());
        hash_aes_key.update(str(port).encode());
        hash_aes_key.update(newkey);
        hash_aes_key.update(newiv);
        #self.json_aes = jason_data['sav_data']['aes'];
        #self.json_iv = jason_data['sav_data']['iv'];
        #self.json_aes_hash = jason_data['sav_data']['aes_hash'];
        #self.json_iv_hash = jason_data['sav_data']['iv_hash'];
        #self.json_myip =  jason_data['sav_data']['myip'];
        #self.json_port =  jason_data['sav_data']['port'];
        hash_aes_key = hash_aes_key.hexdigest();

        newkey = self.bytes_encryption(aeskey, iv, newkey);
        newiv = self.bytes_encryption(aeskey, iv, newiv);
        self.json_file_write(stxt, newkey, newiv, hash_aes_key, "", myip, port, ipv6);

        #s1 = myip + "^" + str(port) + "^" + self.string_to_hex(newkey) + "^" + self.string_to_hex(newiv) + "^" + hash_aes_key;
        #bin1_aes = self.bytes_encryption(aeskey, iv, s1.encode());
        #hex=binascii.hexlify(bin1_aes)
        #txt1 = os.path.join(folder, "1.txt");
        #fobj = open(txt1, "wb")
        #fobj.write(hex);
        #fobj.close();
        #os.remove(bin1_aes);
        #os.remove(bin1);
        return 0;

    def listpath(self, path, rpath, array, idarray, patharray, ctime):
        #File list
        j = array[0];
        sdir = array[1];
        list = os.listdir(path)
        size = len(list);
        sout = "";
        i = 0;
        if(size == 0):
            return [j, sdir, idarray, patharray, ctime];
        while True:
            spath = path + "/" + list[i];
            if(os.path.islink(spath) == True):
                i = i +1;
                if( i== size):
                    break;
            elif(os.path.isdir(spath) == True):
                rpath2 = rpath + "/" + list[i];
                i =  i+1;
                array = [j, sdir];
                array = self.listpath(spath, rpath2, array, idarray, patharray, ctime);
                idarray = array[2];
                patharray = array[3];
                ctime = array[4];
                j = array[0];
                sdir = array[1];
                if( i== size):
                    break;
            else:
                sdir = sdir + "ID: " + str(j) + " | " + rpath + "/" + list[i] + "\n";
                idarray.append(j);
                s1 = rpath + "/" + list[i];
                patharray.append(s1);
                ctime.append("");
                i = i+ 1;
                j = j +1;
                if( i== size):
                    break;
        return [j, sdir, idarray, patharray, ctime]



    def aufraumen(self, os_path_dir):
        print("aufraumen..");
        sdir  = "";
        array = [0, sdir];
        array = self.listpath(os_path_dir, "", array, [], [], []);
        sdir = array[1];
        patharray = array[3];
        ctime = array[4];
        #print(sdir);
        sfileid = "";
        #id = int(id);
        i = 0;
        j = 0;
        while True:
            if(i >= len(patharray)):
                break;
            if(self.find_AES_file(patharray[i]) == True):
                sfile = "";
                sfile = os_path_dir + patharray[i];
                if(Betribsystem == True):
                    sfile = self.flips_schlasch(sfile);
                print(sfile);
                os.remove(sfile);
                j = j +1;
            i = i +1;
        print("Datei gelöscht: " + str(j));

    def setfilename(self, filename):
    	s1 = filename;
    	size = len(s1);
    	i = size-1;
    	iout = 0;
    	while True:
    		if(s1[i] == "\\" or s1[i] == "/"):
    			iout = i;
    			break;
    		i = i -1;
    	i = iout+1;
    	s2  = "";
    	while True:
    		if( i >= size):
    			break;
    		s2 = s2 + s1[i];
    		i = i +1;
    	return s2;

    def setfilename3(self, filename):
    	s1 = filename;
    	size = len(s1);
    	i = size-1;
    	iout = 0;
    	if(i == -1):
    		return s1;
    	while True:
    		if(s1[i] == "\\" or s1[i] == "/"):
    			iout = i;
    			break;
    		i = i -1;
    	i = 0;
    	s2  = "";
    	while True:
    		if( i >= iout):
    			break;
    		s2 = s2 + s1[i];
    		i = i +1;
    	return s2;

    def setfileanme2(self, filename):
    	s1 = filename;
    	size = len(s1);
    	i = 0;
    	s2 = "";
    	while True:
    		if(i == size):
    			break;
    		s2 = s2 + s1[i];
    		i = i+1;
    	return s2;


    def remove_schlash(self, filename):
    	s1 = filename;
    	size = len(s1);
    	if(size == 0):
    		return s1;
    	i = 0;
    	if(s1[0] == '\\' or s1[0] == '/'):
    		i = i+1;
    	s2 = "";
    	while True:
    		if(i == size):
    			break;
    		s2 = s2 + s1[i];
    		i = i+1;
    	return s2;

    def filepath_to_mkdirpath(self, filename):
    	s1 = filename;
    	size = len(s1);
    	i = size-1;
    	iout = 0;
    	if(i == -1):
    		return s1;
    	while True:
    		if(s1[i] == "\\" or s1[i] == "/"):
    			iout = i;
    			break;
    		i = i -1;
    	i = 0;
    	s2  = "";
    	while True:
    		if( i >= iout):
    			break;
    		s2 = s2 + s1[i];
    		i = i +1;
    	return s2;



    def remove_punkt_aes(self, data):
    	i = 0;
    	s1 = "";
    	while True:
    		if(i >= len(data)-4):
    			break;
    		s1 = s1 + data[i];
    		i = i + 1;
    	return s1;

    def flips_schlasch(self, s1):
    	s2 = "";
    	i = 0;
    	while True:
    		if(i >= len(s1)):
    			break;
    		if(s1[i] == "/"):
    			s2 = s2 + "\\";
    		else:
    			s2 = s2 + s1[i];
    		i = i +1;
    	return s2;

    def find_AES_file(self, s1):
    	if(len(s1) >= 5):
    		i = 0;
    		while True:
    			if(i +3 >= len(s1)):
    				break;
    			if(s1[i] == "."):
    				if(s1[i+1] == "a"):
    					if(s1[i+2] == "e"):
    						if(s1[i+3] == "s"):
    							return True;
    			i = i +1;
    	return False;

    def copy_2(self, sin, i,  size):
        out = [];
        while True:
            if(i >= len(sin)):
                break;
            if(i >= size):
                break;
            out.append(sin[i]);
            i = i +1;
        return bytes(out);

    def bytes_decryption(self, key, iv, sin):
        if(self.noencryptmode == 1):
            return sin;
        key = self.string_to_hash(key);
        backend = default_backend();
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend);
        decryptor = cipher.decryptor();
        block = 32;
        size2 = len(sin);
        s1 = [];
        bout = b"";
        j = 0;
        key_ =  decryptor.update(self.copy_2(sin, j, j+ 32));
        j = j + 32;
        iv_ =  decryptor.update(self.copy_2(sin, j, j+ 16));
        j = j + 16;
        decryptor.finalize();
        backend = default_backend();
        cipher = Cipher(algorithms.AES(key_), modes.CBC(iv_), backend=backend);
        decryptor = cipher.decryptor();
        while True:
            if(sin[j] == "#".encode()[0]):
                j = j +1;
                break;
            s1.append(sin[j]);
            j = j +1;
        s1 = bytes(s1).decode();
        size = int(s1);
        i = 0;
        while True:
            if(i >= size):
                break;
            if(j >= size2):
                break;
            if(i + block >= size):
                size_temp = size -i;
            else:
                 size_temp = block;
            bin = self.copy_2(sin,j, j+ 32);
            #sin = filein.read(size_temp);
            if(size_temp == block):
                bin = decryptor.update(bin);
                bout = bout + bin;
            else:
                bin = decryptor.update(bin);
                a = self.analyse(bin);
                bout = bout + self.copy(bin, a);
            i = i + size_temp;
            j = j + size_temp;
        bin = decryptor.finalize();
        #bout = bout + bin;
        #print("ende decrypt");
        return bout;

    def bytes_encryption(self, key, iv, sin):
        if(self.noencryptmode == 1):
            return sin;
        key = self.string_to_hash(key);
        backend = default_backend();
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend);
        encryptor = cipher.encryptor();
        block = 32;
        key_ = os.urandom(32);
        iv_ = os.urandom(16);
        bout = encryptor.update(key_);
        bout = bout  + encryptor.update(iv_);
        encryptor.finalize();
        backend = default_backend();
        cipher = Cipher(algorithms.AES(key_), modes.CBC(iv_), backend=backend);
        encryptor = cipher.encryptor();
        size = len(sin);
        bout = bout + (str(size) + "#" ).encode();
        i = 0;
        j = 0;
        while True:
            if(i >= size):
                break;
            if(i + block >= size):
                size_temp = size -i;
            else:
                 size_temp = block;
            bin = self.data_array_Schreiben(self.copy_2(sin,j, j+ size_temp));
            #sin = filein.read(size_temp);
            #print(len(bin));
            if(size_temp == block):
                bin = encryptor.update(bin);
                bout = bout + bin;
            else:
                bin = encryptor.update(bin);
                bout = bout + bin;
            i = i + size_temp;
            j = j + size_temp;
        bin = encryptor.finalize();
        #bout = bout + bin;
        #print("ende encrypt");
        return bout;

    def json_file_write(self, sfile, aes, iv, aes_hash, iv_hash, myip, port, ipv6):
        jason_data['sav_data'] = {'aes': binascii.hexlify(aes).decode(), 'iv' : binascii.hexlify(iv).decode(), 'aes_hash' : aes_hash, 'iv_hash' : iv_hash, "myip" : myip, "port" : port, "ipv6" : ipv6, "noencryptmode" : self.noencryptmode};
        with open(sfile, "w") as write_file:
            json.dump(jason_data, write_file);
            write_file.close();
        return 0;

    def json_file_read(self, sfile):
        if(os.path.isfile(sfile) == False):
            return 0;
        with open(sfile, "r") as read_file:
            try:
                jason_data  = json.load(read_file)
                self.json_aes = binascii.unhexlify(jason_data['sav_data']['aes'].encode());
                self.json_iv = binascii.unhexlify(jason_data['sav_data']['iv'].encode());
                self.json_aes_hash = jason_data['sav_data']['aes_hash'];
                self.json_iv_hash = jason_data['sav_data']['iv_hash'];
                self.json_myip =  jason_data['sav_data']['myip'];
                self.json_port =  jason_data['sav_data']['port'];
                self.ipv6 = jason_data['sav_data']['ipv6'];
                self.noencryptmode =  jason_data['sav_data']['noencryptmode'];
                read_file.close();
            except json.decoder.JSONDecodeError:
                return -1;
            except TypeError:
                return -1;
            except KeyError:
                return -1;
        return 0;

    def mesage_eroor(self):
        if(noqeestionmode == 0):
            return 0;
        #msgBox2 = QtWidgets.QMessageBox();
        #msgBox2.setText("ERROR in der übertragung!");
        #yesbuttom = QtWidgets.QPushButton("Yes");
        #nobuttom = QtWidgets.QPushButton("No");
        #msgBox2.addButton(yesbuttom, QtWidgets.QMessageBox.AcceptRole);
        #msgBox2.addButton(nobuttom, QtWidgets.QMessageBox.NoRole);
        #msgBox2.exec();
        messagebox.showinfo("ERROR", "ERROR in der übertragung!")
        #if(msgBox2.clickedButton() == yesbuttom):
        #    return 1;
        #elif(msgBox2.clickedButton() == nobuttom):
        #    return 0;
        #else:
        #    exit(-1);
        return 0;

    def prozess_vorschau(self, array):
        dwid = array[0];
        up = array[1];
        paths_dwid = array[2];
        paths_up = array[3];
        msgBox2 = QtWidgets.QMessageBox();
        msgBox2.setText("Download files from Server: " + str(len(paths_dwid)) + "\n" + "Uploade files to Server: " + str(len(paths_up))+ "\n");
        msgBox2.exec();
        return 0

    def my_yes_no_dialog(self, text):
        tmp = messagebox.askyesno(text, text)
        print(tmp);
        if(tmp == True):
            return 1;
        elif(tmp == False):
            return 0;
        else:
            exit();


        class MyDialog():
            def __init__(self, a1):
                pass;
            def init(self, text):
                print("text: ", text)
                self.root = Tk()
                self.label_str = StringVar()
                self.root.title(text)
                #self.label_str.set(text)
                self.label_str.set(text)
                self.label = Label( self.root, textvariable=self.label_str, relief=RAISED )
                #self.label["textvariable"] = StringVar().set(text);
                self.label.pack(fill="x")
                self.root.minsize(width=800, height=200)
                self.root.geometry('800x200+0+0')

                self.out_ = 0;
                def yes():
                    self.out_ = 1;
                    self.root.quit();
                def no():
                    self.out_ = 0;
                    self.root.quit();
                self.button_yes = Button(self.root, text ="yes", command = yes)
                self.button_yes.pack()
                self.button_no = Button(self.root, text ="no", command = no)
                self.button_no.pack()
                self.root.mainloop()
            def out(self):
                return self.out_;
            def quit(self):
                self.root.quit();
                self.root.destroy();
        tmp = MyDialog("");
        tmp.init(text);
        tmp.quit();
        return (tmp.out());

    def set_verzeichnis(self, text):
        self.textedit_Verzeichniss1 = text;
        return 0;

    def progressbar_infos():
        return [self.progrssbar_value, self.progrssbar_maxvalue, self.progrssbar_text]

    def ser_progressbar(self, progressbar, label):
        self.progrssbar = progressbar;
        self.progrssbar_label = label;
        return 0;

    def set_Window(self, window):
        self.window = window;
        return 0;

    def calulate_array_maxsize(self):
        a1 = self.maxsize_array;
        up_size = self.maxsize_array[0];
        dwid_size = self.maxsize_array[1];
        size = 0;
        for tmp in up_size:
            size = size + tmp;
        for tmp in dwid_size:
            size = size + tmp;
        self.calulate_max_size = size;
        return 0;









mainwindow = seb_sync_clinet_gui();
if(serverstartauto == 1):
    mainwindow.start_Server();
else:
    root = Tk()
    label_str = StringVar()
    label = Label( root, textvariable=label_str, relief=RAISED )
    label_str.set("Sync Ordner")
    label.pack()

    LineEdit = Entry(root)
    LineEdit["borderwidth"] = "2px"
    LineEdit.pack()

    def ordner_browse():
        filename = filedialog.askdirectory()
        LineEdit.delete(0,END);
        LineEdit.insert(0, [filename])
        mainwindow.set_verzeichnis(filename);
    button_start_browse = Button(root, text ="browse..", command = ordner_browse)
    button_start_browse.pack()

    def start_Server_():
        threading.Thread( target=mainwindow.start_Server()).start();
    button_start_Server = Button(root, text ="start Server", command = start_Server_)
    button_start_Server.pack()

    def start_Client_():
        threading.Thread( target=mainwindow.start_sync()).start();
        #mainwindow.start_sync();
    button_start_Client = Button(root, text ="start Client", command = start_Client_)
    button_start_Client.pack()

    progress = Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate');
    progress['value'] = 0;
    progress['maximum'] = 100;
    #self.root.update_idletasks();
    label_str2 = StringVar()
    #self.root.title(text)
    progress.pack(fill="x")
    #self.label_str.set(text)
    label = Label( root, textvariable=label_str2, relief=RAISED )
    label_str2.set("")
    label.pack(fill="x");

    mainwindow.ser_progressbar(progress, label_str2);
    mainwindow.set_Window(root)

    root.title(mainwindow.title)
    root.minsize(width=800, height=200)
    root.geometry('800x200+0+0')
    root.mainloop()
    #mainwindow.show();
    #app.exec();
