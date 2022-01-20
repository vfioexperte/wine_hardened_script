#!/usr/bin/env python
#Copyright (C) 2022  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#this is a fork from https://github.com/kritzsie/steam-on-docker
#https://pypi.org/project/cryptography/
#start project 12.01.2022

#last edit 13.01.2022

version = "0.1a"

from cryptography.fernet import Fernet
import binascii

def rsa_gerate_keys():
    key = Fernet.generate_key();
    return key;

def rsa_encrypt_byte(b1, key):
    encrypt = Fernet(key);
    return byte_to_hex(encrypt.encrypt(b1));

def rsa_encrypt_str(b1, key):
    encrypt = Fernet(key);
    return byte_to_hex(encrypt.encrypt(b1.encode("utf-8")));

def rsa_decrypt_byte(b1, key):
    decrypt = Fernet(key);
    return decrypt.decrypt(hex_to_byte(b1));

def byte_to_hex(s1):
    return binascii.hexlify(s1).decode();

def hex_to_byte(hex):
    return binascii.unhexlify(hex);
