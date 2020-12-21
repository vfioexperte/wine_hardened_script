#!/usr/bin/env python
#Copyright (C) 2020  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#Warnung der Programmierer hafte nicht auf Schäden oder auf unsachgemäßen Umgang der APP
#19.12.2020 #start wirting app
#20.20.2020 alst edit
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import math
version = "v0.2b"
print(version)
appname = "Sebs Sync App";

testmode = 0; # 1 aktivted test mode
if(testmode == 1):
    print("Test mdoe on");

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

app = QtWidgets.QApplication(sys.argv);

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


class seb_sync_clinet_gui(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        #self.ip = "127.0.0.1";
        #self.port = 9044;
        #self.self.statusBar().showMessage('Message in statusbar.');
        self.statusbar = QtWidgets.QStatusBar();
        self.statusbar.showMessage("test");
        self.title = appname + " - " + version;
        self.setWindowTitle(self.title);
        self.resize(600, 200);
        self.layoutv1 = QtWidgets.QVBoxLayout(self)

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
        self.layoutv1.addWidget(self.button)
        self.button.clicked.connect(self.button_Clickes)
        self.button_start_Server = QtWidgets.QPushButton("Start Server");
        self.button_start_Server.clicked.connect(self.start_Server);
        self.button_start_Client = QtWidgets.QPushButton("Start Client");
        self.button_start_Client.clicked.connect(self.start_sync);
        self.layoutv1.addWidget(self.button_start_Server)
        self.layoutv1.addWidget(self.button_start_Client)
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

    def update_progress_info(self, text, progrssbar_value, progrssbar_maxvalue):
        if(self.maxfilecount != 0):
            self.statusbar.showMessage(text + " " + str(self.filecount) + "/" + str(self.maxfilecount));
        else:
            self.statusbar.showMessage(text);
        self.progressbar.setMaximum(progrssbar_maxvalue);
        self.progressbar.setValue(progrssbar_value);
        app.processEvents();
        return 0;
    def start_sync(self):
        aes_key = self.question_aes_key();
        iv_ = self.question_iv_key();
        b1 = 0;
        if(self.textedit_Verzeichniss1.toPlainText() != ""):
            b1 = 1;
            self.update_progress_info("start sync 1.. " + self.textedit_Verzeichniss_name1.toPlainText(), 0, 400);
            self.start_Client("5", "0", self.textedit_Verzeichniss1.toPlainText(), aes_key, iv_);
            self.update_progress_info("start sync 2.. " + self.textedit_Verzeichniss_name1.toPlainText(),0, 400);
            self.start_Client("5", "0", self.textedit_Verzeichniss1.toPlainText(), aes_key, iv_);
        if(self.textedit_Verzeichniss2.toPlainText() != ""):
            b1 = 1;
            self.update_progress_info("start sync 1.. " + self.textedit_Verzeichniss_name2.toPlainText(),0, 400);
            self.start_Client("5", "0", self.textedit_Verzeichniss2.toPlainText(), aes_key, iv_);
            self.update_progress_info("start sync 2.. " + self.textedit_Verzeichniss_name2.toPlainText(),0, 400);
            self.start_Client("5", "0", self.textedit_Verzeichniss2.toPlainText(), aes_key, iv_);
        if(self.textedit_Verzeichniss3.toPlainText() != ""):
            b1 = 1;
            self.update_progress_info("start sync 1.. " + self.textedit_Verzeichniss_name3.toPlainText(),0, 400);
            self.start_Client("5", "0", self.textedit_Verzeichniss3.toPlainText(), aes_key, iv_);
            self.update_progress_info("start sync 2.. " + self.textedit_Verzeichniss_name3.toPlainText(),0, 400);
            self.start_Client("5", "0", self.textedit_Verzeichniss3.toPlainText(), aes_key, iv_);
        if(self.textedit_Verzeichniss4.toPlainText() != ""):
            b1 = 1;
            self.update_progress_info("start sync 1.. " + self.textedit_Verzeichniss_name4.toPlainText(),0, 400);
            self.start_Client("5", "0", self.textedit_Verzeichniss4.toPlainText(), aes_key, iv_);
            self.update_progress_info("start sync 2.. " + self.textedit_Verzeichniss_name4.toPlainText(),0, 400);
            self.start_Client("5", "0", self.textedit_Verzeichniss4.toPlainText(), aes_key, iv_);
        if(b1 == 0):
            msgBox2 = QtWidgets.QMessageBox();
            msgBox2.setText("All Textboxen is empty. please click browse!",0, 400);
            msgBox2.exec();
            self.update_progress_info("sync ende",0, 400);
            return -1;
        msgBox2 = QtWidgets.QMessageBox();
        msgBox2.setText("Sync Fertig!");
        msgBox2.exec();
        if(testmode != 1):
            self.sav();
        self.update_progress_info("sync ende",0, 400);
        return 0;

    def sav(self):
        s1 = self.textedit_Verzeichniss1.toPlainText() + "^" + self.textedit_Verzeichniss_name1.toPlainText() + "^";
        s1 = s1 + self.textedit_Verzeichniss2.toPlainText() + "^" + self.textedit_Verzeichniss_name2.toPlainText() + "^";
        s1 = s1 + self.textedit_Verzeichniss3.toPlainText() + "^" + self.textedit_Verzeichniss_name3.toPlainText() + "^";
        s1 = s1 + self.textedit_Verzeichniss4.toPlainText() + "^" + self.textedit_Verzeichniss_name4.toPlainText() + "^";
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
        dir = fieldialog.getExistingDirectory(self, "bowse sync folder", home,);
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
                msgBox2 = QtWidgets.QMessageBox();
                msgBox2.setText("ERROR Connection File not exist! 1.txt file not found in seleted folder");
                msgBox2.exec();
                print("ERROR Connection File not exist!");
                return [];
            fobj2 = open(stxt, "rb");
            fobj2.seek(0, 2);
            size = fobj2.tell();
            fobj2.seek(0, 0);
            s2 = fobj2.read(size);
            fobj2.close();
            byte2=binascii.unhexlify(s2);
            sbin = os.path.join(folder, "1.bin.aes");
            sbin_decrypt = os.path.join(folder, "1.bin");
            fobj = open(sbin, "wb")
            fobj.write(byte2);
            fobj.close();
            self.file_decrypt(aeskey, iv, sbin, sbin_decrypt);
            fobj3 = open(sbin_decrypt, "rb")
            fobj3.seek(0, 2)
            size = fobj3.tell()
            fobj3.seek(0, 0)
            s2 = fobj3.read(size);
            fobj3.close();
            s2 = s2.decode();
            s3 = s2.split("^");
            ip = s3[0];
            port = int(s3[1]);
            key_ = s3[2];
            iv_ = s3[3];
            hash = s3[4];
            key_ =  self.hex_to_String(key_);
            iv_ = self.hex_to_String(iv_);

            hash_aes_key = hashlib.sha256();
            hash_aes_key.update(str(ip).encode());
            hash_aes_key.update(str(port).encode());
            hash_aes_key.update(key_);
            hash_aes_key.update(iv_);
            hash_aes_key = hash_aes_key.hexdigest();
            os.remove(sbin);
            os.remove(sbin_decrypt);
            if(hash_aes_key != hash):
                msgBox2 = QtWidgets.QMessageBox();
                msgBox2.setText("ERROR Connection File not corupt or passwor wrong!");
                msgBox2.exec();
                print("ERROR Connection File not corupt or passwor wrong!");
                os.remove(sbin);
                os.remove(sbin_decrypt);
                return [];
            return [ip, port, key_, iv_, hash];
        except UnicodeDecodeError:
            msgBox2 = QtWidgets.QMessageBox();
            msgBox2.setText("ERROR Connection File not corupt or passwor wrong!");
            msgBox2.exec();
            print("ERROR Connection File not corupt or passwor wrong!");
            return [];


    def question_dns_or_ip(self):
        msgBox2 = QtWidgets.QMessageBox();
        msgBox2.setText("have you a dns?");
        yesbuttom = QtWidgets.QPushButton("Yes");
        nobuttom = QtWidgets.QPushButton("No");
        msgBox2.addButton(yesbuttom, QtWidgets.QMessageBox.AcceptRole);
        msgBox2.addButton(nobuttom, QtWidgets.QMessageBox.NoRole);
        msgBox2.exec();
        if(msgBox2.clickedButton() == yesbuttom):
            return 1;
        elif(msgBox2.clickedButton() == nobuttom):
            return 0;
        else:
            exit(-1);

    def question_port(self):
        i, okPressed = QtWidgets.QInputDialog.getInt(self, "Get integer","Your port:", 9044, 1, 65000, 1);
        if okPressed:
            if(i >= 1):
                if(i <= 65000):
                    return i;
        else:
            exit(-1);

    def question_textbox(self):
        i, okPressed = QtWidgets.QInputDialog.getInt(self, "Get integer","Starten welcher gespeicherten Textboxen: ", 1, 1, 4, 1);
        if okPressed:
            if(i >= 1):
                if(i <= 4):
                    return i;
        else:
            exit(-1);

    def question_aes_key(self):
        text, okPressed = QtWidgets.QInputDialog.getText(self, "Get text", "your aes key", QtWidgets.QLineEdit.Normal, "");
        if(okPressed and text != ""):
            return self.key_size_anpassen(text.encode());
        else:
            exit(-1);

    def question_iv_key(self):
        text, okPressed = QtWidgets.QInputDialog.getText(self, "Get text", "your aes iv key", QtWidgets.QLineEdit.Normal, "");
        if(okPressed and text != ""):
            return self.iv_size_anpassen(text.encode());
        else:
            exit(-1);

    def question_folder(self):
        while True:
            fieldialog = QtWidgets.QFileDialog;
            file = fieldialog.getExistingDirectory(self, "Sync Folder", "");
            if(os.path.isdir(str(file)) == True):
                return (str(file));

    def start_listen_Server(self, port):
        while True:
            try:
                self.update_progress_info("Server listen..", 0, 100);
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                s.bind(("", port));
                print("Server gestartet");
                return s;
            except OSError:
                print("Die Adresse wird bereits verwendet");
                sleep(15);
        return -1;

    def read_connection_simple_mode(self, addr, komm):
        mode = "";
        while True:
            data = komm.recv(1).decode()
            if data == ";":
                break;
            mode = mode + data;
        return mode;

    def wirte_connection_simple_mode(self, addr, komm, text):
        komm.send((text+";").encode());
        return 0;

    def remove_punkt_aes(self, s2):
        i = 0;
        s1 = "";
        while True:
            if(i >= len(s2)-4):
                break;
            s1 = s1 + s2[i];
            i =i +1;
        return s1;

    def Clinet_file_upload_clinet(self, addr, s, aeskey, iv, folder, id):
        #try:
            self.update_progress_info("upload file..",0, 100);
            block = 1024;
            #self.wirte_connection_simple_mode(addr, s, "1");
            sdir = "";
            array = [0, sdir];
            array = self.listpath(folder, "", array, [], [], []);
            sdir = array[1];
            patharray = array[3];
            ctime = array[4];
            print(sdir);
            sfileid = "";
            id = int(id);
            print(folder);
            #sfile = os.path.join(folder, patharray[id]);
            sfile = "";
            if(Betribsystem == False):
                sfile = folder + patharray[id];
            else:
                sfile = folder + self.flips_schlasch(patharray[id]);
            sfileaes = sfile + ".aes";
            print("file encryption..");
            self.update_progress_info("file encryption..",0, 100);
            self.file_encrypt(aeskey, iv, sfile, sfileaes);
            print("file encryption..ende");
            self.update_progress_info("file encryption..ende",100, 100)
            self.wirte_connection_simple_mode(addr, s, patharray[id] + ".aes");
            fobj = open(sfileaes, "rb");
            hash = hashlib.sha256();
            fobj.seek(0, 2);
            size = fobj.tell();
            fobj.seek(0, 0);
            self.wirte_connection_simple_mode(addr, s, str(size));
            stinfo = os.stat(sfile);
            time_1 = str(stinfo.st_atime) + "," + str(stinfo.st_mtime);
            self.wirte_connection_simple_mode(addr, s, time_1);
            i = 0;
            sizetemp = 0;
            self.update_progress_info("file upload..",0, 100);
            while True:
                if(i >= size):
                    break;
                if(i + block > size):
                    sizetemp = size -i ;
                else:
                    sizetemp = block;
                s1 = fobj.read(sizetemp);
                hash.update(s1);
                s.send(s1)
                i = i + sizetemp;
                if(i != 0 and i % 1500000 == 0):
                    s2 = float(i) * float(100) / float(size);
                    s1 = str(i) + "/" + str(size) + ":" + str(s2) + "%";
                    self.update_progress_info("file upload..", self.float_to_int(s2), 100);
                    print("upload: ", s1);
            fobj.close();
            print("upload: ", 100.0);
            self.update_progress_info("file upload..",100, 100);
            self.update_progress_info("file decryption andere PC..",0, 100);
            print("file decryption andere PC");
            shash = hash.hexdigest();
            hash_  = shash;
            sok = self.read_connection_simple_mode(addr, s);
            self.update_progress_info("file decryption andere PC..",100, 100);
            if(sok == "OK"):
                self.wirte_connection_simple_mode(addr, s, shash);
                b1 = self.read_connection_simple_mode(addr, s);
                if(b1 == "0"):
                    print(shash);
                    print("Ubertragung FAIL");
                    s.close();
                    return -1;
                else:
                    print("Ubertragung OK");
            os.remove(sfileaes);
        #except:
        #    s.close();
        #    return -1;
            s.close();
            return 0;


    def float_to_int(self, zahl):
        return math.floor(zahl)

    def Server_file_upload_client(self, addr, komm, aeskey, iv, folder):
        #try:
            block = 1024;
            print("file encryption andere PC..");
            self.update_progress_info("file encryption andere PC..",0, 100);
            filename = self.read_connection_simple_mode(addr, komm);
            print("file encryption andere PC..ende");
            self.update_progress_info("file encryption andere PC..ende",100, 100);
            size = self.read_connection_simple_mode(addr, komm);
            size = int(size);
            ctime = self.read_connection_simple_mode(addr, komm);
            if(Betribsystem == False):
                filename = folder + filename;
            else:
                filename = folder + self.flips_schlasch(filename);
            if(os.path.isfile(filename) == True):
                komm.close();
                return 0;
            dir = self.filepath_to_mkdirpath(filename);
            os.system("mkdir -p " + "\"" + dir + "\"");
            fobj = open(filename, "wb");
            hash = hashlib.sha256();
            data = "";
            i = 0;
            size_temp = 0;
            self.update_progress_info("file download..",0, 100);
            while True:
                if(i >= size):
                    break;
                if(i + block >= size):
                    sizetemp = size - i;
                else:
                    sizetemp = block;
                data = komm.recv(sizetemp);
                sizetemp = len(data);
                hash.update(data);
                fobj.write(data);
                i = i +sizetemp;
                if(i != 0 and i % 150000 == 0):
                    s2 = float(i) * float(100) / float(size);
                    s1 = str(i) + "/" + str(size) + ":" + str(s2) + "%";
                    print("Downlaod: ", s1);
                    self.update_progress_info("file download..", self.float_to_int(s2), 100);
            hash_ = hash.hexdigest();
            fobj.close();
            print("Downlaod: ", 100.0);
            self.update_progress_info("file download..",100, 100);
            finame_out = self.remove_punkt_aes(filename);
            print("file decryption..");
            self.update_progress_info("file decryption..",0, 100);
            self.file_decrypt(aeskey, iv, filename, finame_out)
            self.wirte_connection_simple_mode(addr, komm, "OK");
            self.update_progress_info("file decryption..ende",100, 100);
            #komm.send("OK;".encode());
            shash = self.read_connection_simple_mode(addr, komm);
            os.remove(filename);
            if(shash == hash_):
                print("Ubertragung OK");
                self.wirte_connection_simple_mode(addr, komm, "1");
                #komm.send("1;".encode());
            else:
                print(shash);
                print(hash_);
                print("Ubertragung FAIL");
                self.wirte_connection_simple_mode(addr, komm, "0");
                #komm.send("0;".encode());
                print(filename);
                os.remove(finame_out);
                komm.close();
                return 0;
            ctime = ctime.split(",");
            os.utime(finame_out,(float(ctime[0]), float(ctime[1])));
            komm.close();
            return 0;
        #except:
        #    komm.close();
        #    return -1;
        #    komm.close();
        #    return 0;
    def clinet_sync(self, addr, komm, aeskey, iv, folder):
        dwid = [];
        up = [];
        size2 =  self.read_connection_simple_mode(addr, komm);
        size2 = int(size2);
        i = 0;
        while True:
            if(i >= size2):
                break;
            sfilepath = "";
            sfilepath = self.read_connection_simple_mode(addr, komm);
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
                dwid.append(i);
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
            print("hash clinet: ", hash_);
            print("hash server: ", server_hash);
            if(hash_ != server_hash):
                if(mtime  > clientst_mtime):
                    dwid.append(str(i));
                elif(mtime  < clientst_mtime):
                    sdir  = "";
                    array = [0, sdir];
                    array = self.listpath(folder, "", array, [], [], []);
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
                        elif(patharray[j] == self.flips_schlasch(sfilepath)):
                            up.append(str(j));
                        j = j +1;
                else:
                    dwid.append(str(i));
            self.wirte_connection_simple_mode(addr, komm, "1");
            i = i +1;
        komm.close();
        print("clinet_sync ende");
        return [dwid, up];

    def clinet_sync_add(self, addr, komm, aeskey, iv, folder):
        print("clinet_sync_add start")
        up = [];
        sdir  = "";
        array = [0, sdir];
        array = self.listpath(folder, "", array, [], [], []);
        sdir = array[1];
        ctime = array[4];
        patharray = array[3];
        idarray = array[2];
        sfileid = "";
        size2 = len(idarray);
        self.wirte_connection_simple_mode(addr, komm, str(size2));
        i = 0;
        while True:
            if(i >= size2 ):
                break;
            sdata = "";
            if(Betribsystem == False):
                sdata = patharray[i];
            else:
                sdata = patharray[i];
            self.wirte_connection_simple_mode(addr, komm, sdata);
            check = self.read_connection_simple_mode(addr, komm);
            if(check == "0"):
                up.append(str(i));
            i = i +1;
        komm.close();
        print("clinet_sync_add ende");
        return up;

        return 0;


    def server_sync_add(self, addr, komm, aeskey, iv, folder):
        size = self.read_connection_simple_mode(0, komm);
        size = int(size);
        i = 0;
        while True:
            if( i>= size):
                break;
            sfilepath = "";
            sfilepath = self.read_connection_simple_mode(0, komm);
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
        komm.close();
        return 0;


    def server_sync(self, addr, komm, aeskey, iv, folder):
        sdir  = "";
        array = [0, sdir];
        array = self.listpath(folder, "", array, [], [], []);
        sdir = array[1];
        ctime = array[4];
        patharray = array[3];
        idarray = array[2];
        size2 = len(idarray);
        self.wirte_connection_simple_mode(addr, komm, str(size2));
        i  = 0;
        while True:
            if(i >= size2):
                break;
            sdata = patharray[i];
            self.wirte_connection_simple_mode(addr, komm, sdata);
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
            b1 = self.read_connection_simple_mode(addr, komm);
            i = i +1;
        komm.close();
        print("server_sync ende");
        return 0;



    def server_liste_senden(self, addr, komm, aeskey, iv, folder):
        #ls server files
        sdir = "";
        array = [0, sdir];
        array = self.listpath(folder, "", array, [], [], []);
        sdir = array[1];
        self.wirte_connection_simple_mode(addr, komm, sdir);
        komm.close();
        return 0;


    def start_Clinet_prozess(self, mode, id, folder, myip, key, iv, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        s.connect((myip, port));

        if(mode == "1"):
            #up
            self.wirte_connection_simple_mode(0, s, "1");
            self.Clinet_file_upload_clinet(0, s, key, iv, folder, id);
        elif(mode == "3"):
            self.wirte_connection_simple_mode(0, s, "3");
            sdir = self.read_connection_simple_mode(0, s);
            print(sdir);
        elif(mode == "4"):
            #dwid
            self.wirte_connection_simple_mode(0, s, "4");
            self.wirte_connection_simple_mode(0, s, id);
            self.Server_file_upload_client(0, s, key, iv, folder);
        elif(mode == "5"):
            #sync
            self.wirte_connection_simple_mode(0, s, "5");
            array = self.clinet_sync(0, s, key, iv, folder);
            s.close();
            return array;
        elif(mode == "7"):
            #sync add
            self.wirte_connection_simple_mode(0, s, "7");
            array = self.clinet_sync_add(0, s, key, iv, folder);
            s.close();
            return array;
        elif(mode == "8"):
            #server size of file server
            self.wirte_connection_simple_mode(0, s, "8");
            self.wirte_connection_simple_mode(0, s, str(self.maxfilecount));
            s.close();
            return [];




        s.close();
        self.aufraumen(folder);
        return [];


    def start_Client(self, mode, id, folder, aes_key, iv_):
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

        if(len(connection_file) == 0):
            return -1;
        myip = connection_file[0];
        port = connection_file[1];
        key = connection_file[2];
        iv =  connection_file[3];
        print(connection_file);
        array = self.start_Clinet_prozess(mode, id, folder, myip, key, iv, port);
        if(len(array) != 0):
            dwid = array[0];
            up = array[1];
            self.filecount = 1;
            self.maxfilecount = len(up) + len(dwid);
            self.start_Clinet_prozess("8", "0", folder, myip, key, iv, port);
            #server size of file server
            print("dwid: ", dwid);
            print("up: ", up);
            for tmp in dwid:
                self.start_Clinet_prozess("4", str(tmp), folder, myip, key, iv, port);
                self.filecount = self.filecount + 1;
            for tmp in up:
                self.start_Clinet_prozess("1",  str(tmp), folder, myip, key, iv, port);
                self.filecount = self.filecount + 1;
            #sync add
            self.filecount = 1;
            array = self.start_Clinet_prozess("7",  "0", folder, myip, key, iv, port);
            self.maxfilecount = len(array);
            self.start_Clinet_prozess("8", "0", folder, myip, key, iv, port);
            #server size of file server
            print("sync_add: ", array);
            for tmp in array:
                self.filecount = self.filecount + 1;
                self.start_Clinet_prozess("1",  str(tmp), folder, myip, key, iv, port);
            self.maxfilecount = 0;
            self.filecount = 0;
            self.start_Clinet_prozess("8", "0", folder, myip, key, iv, port);
        return 0;


    def start_Server(self):
        #folder = self.question_folder();
        aes_key = self.question_aes_key();
        iv_ = self.question_iv_key();
        text = [];
        if(self.textedit_Verzeichniss1.toPlainText() != ""):
            text.append(1);
        if(self.textedit_Verzeichniss2.toPlainText() != ""):
            text.append(2);
        if(self.textedit_Verzeichniss3.toPlainText() != ""):
            text.append(3);
        if(self.textedit_Verzeichniss4.toPlainText() != ""):
            text.append(4);

        if(len(text) == 1):
            if(text[0] == 1):
                self.start_Server_prozess(self.textedit_Verzeichniss1.toPlainText(), aes_key, iv_);
            elif(text[0] == 2):
                self.start_Server_prozess(self.textedit_Verzeichniss2.toPlainText(), aes_key, iv_);
            elif(text[0] == 3):
                self.start_Server_prozess(self.textedit_Verzeichniss3.toPlainText(), aes_key, iv_);
            elif(text[0] == 4):
                self.start_Server_prozess(self.textedit_Verzeichniss4.toPlainText(), aes_key, iv_);
        elif(len(text) == 0):
            msgBox2 = QtWidgets.QMessageBox();
            msgBox2.setText("All Textboxen is empty. please click browse!");
            msgBox2.exec();
            return -1;
        else:
            while True:
                i = self.question_textbox();
                for tmp in text:
                    if(tmp == i):
                        if(text[0] == 1):
                            self.start_Server_prozess(self.textedit_Verzeichniss1.toPlainText(), aes_key, iv_);
                        elif(text[0] == 2):
                            self.start_Server_prozess(self.textedit_Verzeichniss2.toPlainText(), aes_key, iv_);
                        elif(text[0] == 3):
                            self.start_Server_prozess(self.textedit_Verzeichniss3.toPlainText(), aes_key, iv_);
                        elif(text[0] == 4):
                            self.start_Server_prozess(self.textedit_Verzeichniss4.toPlainText(), aes_key, iv_);
        if(testmode != 1):
            self.sav();
        self.update_progress_info("sync ende", 0, 100);
        return 0;


    def start_Server_prozess(self, folder, aes_key, iv_):
        if(Betribsystem == True):
            #widnows
            folder = self.flips_schlasch(folder);
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        #s.bind(("", port));
        self.aufraumen(folder);
        stxt = os.path.join(folder, "1.txt");
        if(os.path.isfile(stxt) == True):
            connection_file = self.read_Connetion_file(folder, aes_key, iv_);
        else:
            msgBox2 = QtWidgets.QMessageBox();
            msgBox2.setText("Conection file (1.txt) not found in the fodler. the APP create a neu 1.txt fiel in the fodler. you must send the 1.txt to teh clinet");
            msgBox2.exec();
            print("Conection file (1.txt) not found in the fodler. the APP create a neu 1.txt fiel in the fodler. you must send the 1.txt to teh clinet");
            connection_file = [];
        if(len(connection_file) == 0):
            if(self.question_dns_or_ip() == 1):
                myip = input("DNS name: ");
                port = self.question_port();
                aes_key_new = os.urandom(32);
                newiv = os.urandom(16);
                self.create_Connetion_file(aes_key, iv_, myip, port, folder, aes_key_new, newiv);
                connection_file = [myip, port, aes_key_new, newiv];


            else:
                myip = self.update_ip();
                port = self.question_port();
                aes_key_new = os.urandom(32);
                newiv = os.urandom(16);
                self.create_Connetion_file(aes_key, iv_, myip, port, folder, aes_key_new, newiv);
                connection_file = [myip, port, aes_key_new, newiv];

        myip = connection_file[0];
        port = connection_file[1];
        key = connection_file[2];
        iv =  connection_file[3];
        print(connection_file);

        if(testmode == 1):
            msgBox2 = QtWidgets.QMessageBox();
            msgBox2.setText("Test Mode aktivirt!");
            msgBox2.exec();
            myip = "127.0.0.1";
        else:
            myip = requests.get('https://www.wikipedia.org').headers['X-Client-IP'];
            if(self.question_dns_or_ip() == 1):
                myip = input("DNS name: ");

        self.create_Connetion_file(aes_key, iv_, myip, port, folder, key, iv);
        connection_file = self.read_Connetion_file(folder, aes_key, iv_);
        server = self.start_listen_Server(port);
        while True:
            server.listen(1);
            komm, addr = server.accept();
            #server_socket = server[0];
            #server_connection = server[1];
            #server_addr = server[2];
            print(server);
            #print(server_connection);
            mode = self.read_connection_simple_mode(0, komm);
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
                self.server_sync(0, komm, key, iv, folder);
            elif(mode == "7"):
                self.server_sync_add(0, komm, key, iv, folder);
            elif(mode == "8"):
                #server size of file server
                tmp = self.read_connection_simple_mode(0, komm);
                tmp = int(tmp);
                komm.close();
                self.maxfilecount = tmp;
                self.filecount = 1;
        self.aufraumen(folder);
        return 0;


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
        print("Decrypt file ende");
        return 0;

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
                #print(len(sin));
                sout = encryptor.update(sin);
                fileout.write(sout);
            i = i + size_temp;
        sout = encryptor.finalize();
        fileout.write(sout);
        print("Encrypt file ende");
        return 0;

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


    def create_Connetion_file(self, aeskey, iv, myip, port, folder, newkey, newiv):
        bin1 = os.path.join(folder, "1.bin");
        bin1_aes = bin1 + ".aes";

        hash_aes_key = hashlib.sha256();
        hash_aes_key.update(str(myip).encode());
        hash_aes_key.update(str(port).encode());
        hash_aes_key.update(newkey);
        hash_aes_key.update(newiv);
        hash_aes_key = hash_aes_key.hexdigest();

        fobj = open(bin1, "wb")
        s1 = myip + "^" + str(port) + "^" + self.string_to_hex(newkey) + "^" + self.string_to_hex(newiv) + "^" + hash_aes_key;
        fobj.write(s1.encode());
        fobj.close();
        self.file_encrypt(aeskey, iv, bin1, bin1_aes);
        fobj2 = open(bin1_aes, "rb")
        fobj2.seek(0, 2)
        size = fobj2.tell()
        fobj2.seek(0, 0)
        s2 = fobj2.read(size);
        fobj2.close();
        hex=binascii.hexlify(s2)
        txt1 = os.path.join(folder, "1.txt");
        fobj = open(txt1, "wb")
        fobj.write(hex);
        fobj.close();
        os.remove(bin1_aes);
        os.remove(bin1);
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
    	print(sdir);
    	sfileid = "";
    	#id = int(id);
    	i = 0;
    	j = 0;
    	while True:
            if(i >= len(patharray)):
                break;
            if(self.find_AES_file(patharray[i]) == True):
                sfile = "";
                if(Betribsystem == False):
                    sfile = os_path_dir + patharray[i];
                else:
                    sfile = os_path_dir + self.flips_schlasch(patharray[i]);
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




mainwindow = seb_sync_clinet_gui();
mainwindow.show();
app.exec_();
