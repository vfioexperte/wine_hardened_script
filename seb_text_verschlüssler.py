#!/usr/bin/env python
# Copyright (C) 2021  vfio_experte
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
# Warnung der Programmierer hafte nicht auf Schäden oder auf unsachgemäßen Umgang der APP
# 17.05.2021 #start wirting app
# 01.12.2022 last edit

import shlex
import subprocess
import struct
import hashlib
import socket
import platform
import os.path
import os
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
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
import shlex
import subprocess
#import subprocess
#import pty
import os
import sys
import os
import time
import datetime
import requests
import binascii
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import time

version = "v0.2a"
#v0.2a binary file support
print(version)
appname = "Text_verschlüssler"

trenner = b"x"
trenner_str = trenner.decode()

app = QtWidgets.QApplication(sys.argv)


def cmd_start(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True).decode().split("\n")
        return out
    except subprocess.CalledProcessError:
        return []


class sebs_text_verschluessler(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        #self.ip = "127.0.0.1";
        #self.port = 9044;
        #self.self.statusBar().showMessage('Message in statusbar.');
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.showMessage("test")
        self.title = appname + " - " + version
        self.setWindowTitle(self.title)
        self.resize(600, 200)
        self.layoutv1 = QtWidgets.QVBoxLayout(self)

        self.layouth1 = QtWidgets.QHBoxLayout()
        self.layouth2 = QtWidgets.QHBoxLayout()
        self.layouth3 = QtWidgets.QHBoxLayout()
        self.layouth4 = QtWidgets.QHBoxLayout()
        self.layouth5 = QtWidgets.QHBoxLayout()

        self.textbox = QtWidgets.QPlainTextEdit()
        self.layouth1.addWidget(self.textbox)
        self.buttontextverschlusseln = QtWidgets.QPushButton(
            "Text verschlüsseln!")
        self.buttontextentschlusseln = QtWidgets.QPushButton(
            "Text entschlüsseln!")
        self.buttonfileverschlusseln = QtWidgets.QPushButton(
            "File entschlüsseln!")
        self.label_key = QtWidgets.QLabel("key: ")
        self.label_iv = QtWidgets.QLabel("iv: ")
        self.key = QtWidgets.QLineEdit()
        self.iv = QtWidgets.QLineEdit()
        self.layouth2.addWidget(self.label_key)
        self.layouth2.addWidget(self.key)
        self.layouth2.addWidget(self.label_iv)
        self.layouth2.addWidget(self.iv)

        self.layouth3.addWidget(self.buttontextverschlusseln)
        self.layouth3.addWidget(self.buttontextentschlusseln)
        self.layouth3.addWidget(self.buttonfileverschlusseln)
        self.buttontextverschlusseln .clicked.connect(self.text_verschluesseln)
        self.buttontextentschlusseln .clicked.connect(self.text_entschluesseln)
        self.buttonfileverschlusseln .clicked.connect(self.file_verschluesseln)

        self.layoutv1.addLayout(self.layouth1)
        self.layoutv1.addLayout(self.layouth2)
        self.layoutv1.addLayout(self.layouth3)

    def remove_sapce(self, s1):
        s2 = ""
        for tmp in s1:
            if(tmp == " "):
                pass
            elif(tmp == "\t"):
                pass
            elif(tmp == "\n"):
                pass
            else:
                s2 = s2 + tmp
        return s2

    def byte_to_hex(self, s1):
        return binascii.hexlify(s1)

    def add_sapce(self, bytes2, splain):
        sout = ""
        j = 0
        i = 0
        while True:
            if(i >= len(splain)):
                if(j >= len(bytes2)):
                    break
            if(i < len(splain)):
                tmp = splain[i]
            else:
                tmp = ""
            if(j < len(bytes2)):
                tmp2 = bytes2[j]
            else:
                tmp2 = b''
            if(tmp == " "):
                sout = sout + tmp
            elif(tmp == "\t"):
                sout = sout + tmp
            elif(tmp == "\n"):
                sout = sout + tmp
            else:
                sout = sout + self.byte_to_hex(bytes(tmp2)).decode()
                j = j + 1
            i = i + 1
        return sout

    def string_to_hash(self, s1):
        hash = hashlib.sha256()
        hash.update(s1)
        return binascii.unhexlify(hash.hexdigest())

    def string_to_hash_16bit(self, s1):
        hash = hashlib.md5()
        hash.update(s1)
        return binascii.unhexlify(hash.hexdigest())

    def string_to_hex(self, s1):
        return binascii.hexlify(s1).decode()

    def hex_to_String(self, hex):
        return binascii.unhexlify(hex)

    def copy(self, sin, size):
        out = []
        i = 0
        while True:
            if(i >= len(sin)):
                break
            if(i >= size):
                break
            out.append(sin[i])
            i = i + 1
        return bytes(out)

    def analyse(self, sout):
        out = sout
        i = len(out) - 1
        while True:
            if(i <= 0):
                break
            if(out[i] == trenner[0]):
                return i
            i = i - 1
        return -1

    def copy_2(self, sin, i,  size):
        out = []
        while True:
            if(i >= len(sin)):
                break
            if(i >= size):
                break
            out.append(sin[i])
            i = i + 1
        return bytes(out)

    def data_array_Schreiben(self, indata):
        b1 = b" "
        bool1 = 0
        while True:
            if(len(indata) >= 32):
                break
            if(bool1 == 0):
                bool1 = 1
                indata = indata + trenner
            else:
                indata = indata + b1
        return indata

    def text_verschluesseln(self):
        if(self.key.text() == "" or self.iv.text() == ""):
            msgBox2 = QtWidgets.QMessageBox()
            msgBox2.setText("key line edit ist leer oder iv ist leer")
            msgBox2.exec()
            return 0
        text = "Text" + self.textbox.toPlainText()
        bencrypt = self.bytes_encryption(
            self.remove_sapce(self.key.text()).encode(), self.remove_sapce(self.iv.text()).encode(), text.encode())
        self.textbox.setPlainText(self.byte_to_hex(bencrypt).decode())
        return 0

    def text_entschluesseln(self):
        if(self.key.text() == "" or self.iv.text() == ""):
            msgBox2 = QtWidgets.QMessageBox()
            msgBox2.setText("key line edit ist leer oder iv ist leer")
            msgBox2.exec()
            return 0
        text = self.textbox.toPlainText()
        text = self.remove_sapce(text)
        text = self.hex_to_String(text)
        bencrypt = self.bytes_decryption(
            self.remove_sapce(self.key.text()).encode(), self.remove_sapce(self.iv.text()).encode(), text)
        b1 = bencrypt;
        if(self.find_text_or_file(b1) == 1):
            self.textbox.setPlainText(b1.decode()[4::])
        else:
            self.save_file(b1[3::]);
        return 0

    def bytes_decryption(self, key, iv, sin):
        key = self.string_to_hash(key)
        iv = self.string_to_hash_16bit(iv)
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        block = 32
        size2 = len(sin)
        s1 = []
        bout = b""
        j = 0
        key_ = decryptor.update(self.copy_2(sin, j, j + 32))
        j = j + 32
        iv_ = decryptor.update(self.copy_2(sin, j, j + 16))
        j = j + 16
        decryptor.finalize()
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key_), modes.CBC(iv_), backend=backend)
        decryptor = cipher.decryptor()
        while True:
            if(sin[j] == "#".encode()[0]):
                j = j + 1
                break
            s1.append(sin[j])
            j = j + 1
        s1 = bytes(s1).decode()
        size = int(s1)
        i = 0
        while True:
            if(i >= size):
                break
            if(j >= size2):
                break
            if(i + block >= size):
                size_temp = size - i
            else:
                size_temp = block
            bin = self.copy_2(sin, j, j + 32)
            if(size_temp == block):
                bin = decryptor.update(bin)
                bout = bout + bin
            else:
                bin = decryptor.update(bin)
                a = self.analyse(bin)
                bout = bout + self.copy(bin, a)
            i = i + size_temp
            j = j + size_temp
        bin = decryptor.finalize()
        return bout

    def bytes_encryption(self, key, iv, sin):
        key = self.string_to_hash(key)
        iv = self.string_to_hash_16bit(iv)
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        block = 32
        key_ = os.urandom(32)
        iv_ = os.urandom(16)
        bout = encryptor.update(key_)
        bout = bout + encryptor.update(iv_)
        encryptor.finalize()
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key_), modes.CBC(iv_), backend=backend)
        encryptor = cipher.encryptor()
        size = len(sin)
        bout = bout + (str(size) + "#").encode()
        i = 0
        j = 0
        while True:
            if(i >= size):
                break
            if(i + block >= size):
                size_temp = size - i
            else:
                size_temp = block
            bin = self.data_array_Schreiben(self.copy_2(sin, j, j + size_temp))
            if(size_temp == block):
                bin = encryptor.update(bin)
                bout = bout + bin
            else:
                bin = encryptor.update(bin)
                bout = bout + bin
            i = i + size_temp
            j = j + size_temp
        bin = encryptor.finalize()
        return bout

    def find_text_or_file(self, s1):
        try:
            s1 = s1.decode();
            if(len(s1) >= 5):
                if(s1[0] == "T"):
                    if(s1[1] == "e"):
                        if(s1[2] == "x"):
                            if(s1[3] == "t"):
                                return 1;
        except UnicodeDecodeError:
            return 0;
        return 0;

    def save_file(self, b1):
        filename = QtWidgets.QFileDialog.getSaveFileName();
        f1 = open(filename[0], "wb");
        f1.write(b1);
        f1.close();
        return 0;

    def open_file(self):
        filename = QtWidgets.QFileDialog.getOpenFileName();
        f1 = open(filename[0], "rb");
        f1.seek(0, 2);
        size = f1.tell();
        f1.seek(0, 0);
        b1 = f1.read(size);
        f1.close();
        return b1;

    def file_verschluesseln(self):
        file = b"BIN" + self.open_file();
        bencrypt = self.bytes_encryption(
        self.remove_sapce(self.key.text()).encode(), self.remove_sapce(self.iv.text()).encode(), file)
        self.textbox.setPlainText(self.byte_to_hex(bencrypt).decode())
        return 0

mainwindow = sebs_text_verschluessler()
mainwindow.show()
app.exec_()
