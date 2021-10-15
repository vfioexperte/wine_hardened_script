#!/usr/bin/env python
#Copyright (C) 2021  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#this is a fork from https://github.com/kritzsie/steam-on-docker

version = "0.1a"

import platform
import os
import sys
import string
import subprocess
import time
import math
import json
jason_data = {};



def read_config():
    if(os.path.isfile(config_file) == False):
        print("read_config() ERROR not found " + config_file + " file in the fodler");
        exit(1);
    file1 = open(config_file, "r");
    file1.seek(0, 2);
    size = file1.tell();
    file1.seek(0, 0);
    b1 = file1.read(size);
    file1.close();
    i = 0;
    config = [];
    config_temp = "";
    config_temp1 = [];
    l1 = -1;
    l2 = -1;
    while True:
        if(i >= len(b1)):
            break;
        if(i + 11 < len(b1) and (b1[i] == 'd' and b1[i+1] == 'o' ) and (b1[i+2] == 'c' and b1[i+3] == 'k' ) and (b1[i+4] == 'e' and b1[i+5] == 'r' ) and (b1[i+6] == '_' and b1[i+7] == 'u' ) and (b1[i+8] == 's' and b1[i+9] == 'e' ) and (b1[i+10] == 'r' )):
            l1 = 1;
        elif(i + 10 < len(b1) and (b1[i] == 'g' and b1[i+1] == 'p' ) and (b1[i+2] == 'u' and b1[i+3] == '_' ) and (b1[i+4] == 'r' and b1[i+5] == 'e' ) and (b1[i+6] == 'n' and b1[i+7] == 'd' ) and (b1[i+8] == 'e' and b1[i+9] == 'r' )):
             l1 = 2;
        elif(i + 15 < len(b1) and (b1[i] == 'd' and b1[i+1] == 'i' ) and (b1[i+2] == 's' and b1[i+3] == 'k' ) and (b1[i+4] == '_' and b1[i+5] == 'd' ) and (b1[i+6] == 'e' and b1[i+7] == 'v' ) and (b1[i+8] == 'i' and b1[i+9] == 'c' ) and (b1[i+10] == 'e'  and  b1[i+11] == '_' ) and   (b1[i+12] == 'n'  and  b1[i+13] == 'a' ) and (b1[i+14] == 'm'  and  b1[i+15] == 'e' )):
            l1 = 3;
        elif(i + 16 < len(b1) and (b1[i] == 'z' and b1[i+1] == 'u' ) and (b1[i+2] == 'g' and b1[i+3] == 'r' ) and (b1[i+4] == 'i' and b1[i+5] == 'f' ) and (b1[i+6] == 'f' and b1[i+7] == '_' ) and (b1[i+8] == 'a' and b1[i+9] == 'u' ) and (b1[i+10] == 'f'  and  b1[i+11] == '_' ) and   (b1[i+12] == 'm'  and  b1[i+13] == 'e' ) and (b1[i+14] == 'd'  and  b1[i+15] == 'i' ) and  b1[i+16] == 'a' ):
            l1 = 4;
        elif(i + 21 < len(b1) and (b1[i] == 's' and b1[i+1] == 'a' ) and (b1[i+2] == 'v' and b1[i+3] == '_' ) and (b1[i+4] == 'h' and b1[i+5] == 'o' ) and (b1[i+6] == 'm' and b1[i+7] == 'e' ) and (b1[i+8] == '_' and b1[i+9] == 'd' ) and (b1[i+10] == 'o'  and  b1[i+11] == 'c' ) and   (b1[i+12] == 'k'  and  b1[i+13] == 'e' ) and (b1[i+14] == 'r'  and  b1[i+15] == '_' ) and  (b1[i+16] == 'f' and b1[i+17] == 'o') and (b1[i+18] == 'l' and b1[i+19] == 'd') and  (b1[i+20] == 'e' and b1[i+21] == 'r') ):
            l1 = 5;
        elif(i + 11 < len(b1) and (b1[i] == 's' and b1[i+1] == 'h' ) and (b1[i+2] == 'a' and b1[i+3] == 'r' ) and (b1[i+4] == 'e' and b1[i+5] == '_' ) and (b1[i+6] == 'f' and b1[i+7] == 'o' ) and (b1[i+8] == 'l' and b1[i+9] == 'd' ) and (b1[i+10] == 'e'  and  b1[i+11] == 'r' )):
            if(i + 17 < len(b1) and (b1[i+12] == '_' and b1[i+13] == 'd' ) and (b1[i+14] == 'a' and b1[i+15] == 't' ) and (b1[i+16] == 'e' and b1[i+17] == 'n' )):
                l1 = 6;
            elif(i + 18 < len(b1) and (b1[i+12] == '1' and b1[i+13] == '_' ) and (b1[i+14] == 'a' and b1[i+15] == 'k' ) and (b1[i+16] == 't' and b1[i+17] == 'i' )  and (b1[i+18] == 'v')):
                l1 = 7;
            elif(i + 18 < len(b1) and (b1[i+12] == '1')):
                l1 = 8;
        elif(i + 13 < len(b1) and (b1[i] == 'n' and b1[i+1] == 'e' ) and (b1[i+2] == 't' and b1[i+3] == 'w' ) and (b1[i+4] == 'o' and b1[i+5] == 'r' ) and (b1[i+6] == 'k' and b1[i+7] == '_' ) and (b1[i+8] == 'd' and b1[i+9] == 'i' ) and (b1[i+10] == 's'  and  b1[i+11] == 'a' ) and   (b1[i+12] == 'b'  and  b1[i+13] == 'l' ) ):
            l1 = 9;
        elif(i + 20 < len(b1) and (b1[i] == 's' and b1[i+1] == 't' ) and (b1[i+2] == 'e' and b1[i+3] == 'a' ) and (b1[i+4] == 'm' and b1[i+5] == '_' ) and (b1[i+6] == 'c' and b1[i+7] == 'o' ) and (b1[i+8] == 'n' and b1[i+9] == 't' ) and (b1[i+10] == 'r'  and  b1[i+11] == 'o' ) and   (b1[i+12] == 'l'  and  b1[i+13] == 'l' ) and (b1[i+14] == 'e'  and  b1[i+15] == 'r' ) and (b1[i+16] == '_'  and  b1[i+17] == 'b' )and (b1[i+18] == 'o'  and  b1[i+19] == 'o' )and  b1[i+20] == 'l' ):
            l1 = 10;
        elif(i + 10 < len(b1) and (b1[i] == 'u' and b1[i+1] == 's' ) and (b1[i+2] == 'b' and b1[i+3] == '_' ) and (b1[i+4] == 's' and b1[i+5] == 'h' ) and (b1[i+6] == 'a' and b1[i+7] == 'r' ) and (b1[i+8] == 'i' and b1[i+9] == 'n' ) and (b1[i+10] == 'g' )):
            l1 = 11;
        elif(i + 7 < len(b1) and (b1[i] == 'u' and b1[i+1] == 's' ) and (b1[i+2] == 'b' and b1[i+3] == '_' ) and (b1[i+4] == 'n' and b1[i+5] == 'a' ) and (b1[i+6] == 'm' and b1[i+7] == 'e' ) ):
            l1 = 12;
        elif(i + 14 < len(b1) and (b1[i] == 'u' and b1[i+1] == 's' ) and (b1[i+2] == 'b' and b1[i+3] == '_' ) and (b1[i+4] == 'h' and b1[i+5] == 'i' ) and (b1[i+6] == 'd' and b1[i+7] == 'r' ) and (b1[i+8] == 'a' and b1[i+9] == 'w' ) and (b1[i+10] == '_'  and  b1[i+11] == 'n' ) and   (b1[i+12] == 'a'  and  b1[i+13] == 'm' ) and (b1[i+14] == 'e' )):
            l1 = 13;
        elif(i + 11 < len(b1) and (b1[i] == 'd' and b1[i+1] == 'o' ) and (b1[i+2] == 'c' and b1[i+3] == 'k' ) and (b1[i+4] == 'e' and b1[i+5] == 'r' ) and (b1[i+6] == '_' and b1[i+7] == 'b' ) and (b1[i+8] == 'u' and b1[i+9] == 'i' ) and (b1[i+10] == 'l' and b1[i+11] == 'd')):
            l1 = 14;
        elif(i + 11 < len(b1) and (b1[i] == 'd' and b1[i+1] == 'o' ) and (b1[i+2] == 'c' and b1[i+3] == 'k' ) and (b1[i+4] == 'e' and b1[i+5] == 'r' ) and (b1[i+6] == '_' and b1[i+7] == 'i' ) and (b1[i+8] == 'n' and b1[i+9] == 'p' ) and (b1[i+10] == 'u' and b1[i+11] == 't')):
            l1 = 15;
        elif(i + 15 < len(b1) and (b1[i] == 'd' and b1[i+1] == 'o' ) and (b1[i+2] == 'c' and b1[i+3] == 'k' ) and (b1[i+4] == 'e' and b1[i+5] == 'r' ) and (b1[i+6] == '_' and b1[i+7] == 'm' ) and (b1[i+8] == 'a' and b1[i+9] == 'x' ) and (b1[i+10] == 'm' and b1[i+11] == 'e')  and   (b1[i+12] == 'm' and b1[i+13] == 'o') and (b1[i+14] == 'r' and b1[i+15] == 'y') ):
            l1 = 16;#maxmemory
        elif(i + 13 < len(b1) and (b1[i] == 'd' and b1[i+1] == 'o' ) and (b1[i+2] == 'c' and b1[i+3] == 'k' ) and (b1[i+4] == 'e' and b1[i+5] == 'r' ) and (b1[i+6] == '_' and b1[i+7] == 'm' ) and (b1[i+8] == 'a' and b1[i+9] == 'x' ) and (b1[i+10] == 'c' and b1[i+11] == 'p')  and   (b1[i+12] == 'u' and b1[i+13] == 's') ):
            l1 = 17;#maxcpus
        elif(i + 11 < len(b1) and (b1[i] == 'n' and b1[i+1] == 'e' ) and (b1[i+2] == 't' and b1[i+3] == 'w' ) and (b1[i+4] == 'o' and b1[i+5] == 'r' ) and (b1[i+6] == 'k' and b1[i+7] == '_' ) and (b1[i+8] == 'h' and b1[i+9] == 'o' ) and (b1[i+10] == 's' and b1[i+11] == 't')  ):
            l1 = 18;#network_host
        elif(i + 11 < len(b1) and (b1[i] == 'p' and b1[i+1] == 'o' ) and (b1[i+2] == 'r' and b1[i+3] == 't' ) and (b1[i+4] == 'f' and b1[i+5] == 'o' ) and (b1[i+6] == 'r' and b1[i+7] == 'w' ) and (b1[i+8] == 'd' and b1[i+9] == 'i' ) and (b1[i+10] == 'n' and b1[i+11] == 'g')  ):
            l1 = 19;#portforwding
        elif(i + 6 < len(b1) and (b1[i] == 'd' and b1[i+1] == 'b' ) and (b1[i+2] == 'u' and b1[i+3] == 's' ) and (b1[i+4] == '_' and b1[i+5] == 'r' ) and (b1[i+6] == 'w' ) ):
            l1 = 20;#dbus_rw
        elif(i + 11 < len(b1) and (b1[i] == 'p' and b1[i+1] == 'a' ) and (b1[i+2] == 'c' and b1[i+3] == 'm' ) and (b1[i+4] == 'a' and b1[i+5] == 'n' ) and (b1[i+6] == '_' and  b1[i+7] == 'c') and (b1[i+8] == 'a' and  b1[i+9] == 'c') and (b1[i+10] == 'h' and  b1[i+11] == 'e') ):
            l1 = 21;#pacman_cache
        elif(i + 2 < len(b1) and (b1[i] == 'd' and b1[i+1] == 'n' ) and (b1[i+2] == 's') ):
            l1 = 22;#dns
        elif(i + 3 < len(b1) and (b1[i] == 'i' and b1[i+1] == 'p' ) and  (b1[i+2] == 'v' and b1[i+3] == '4' ) ):
            l1 = 23;#ipv4
        elif(i + 12 < len(b1) and (b1[i] == 'w' and b1[i+1] == 'i' ) and  (b1[i+2] == 'r' and b1[i+3] == 'e' ) and (b1[i+4] == 'g' and b1[i+5] == 'u' ) and (b1[i+6] == 'a' and b1[i+7] == 'r' )and (b1[i+8] == 'd' and b1[i+9] == '_' )and (b1[i+10] == 'f' and b1[i+11] == 'i' )and (b1[i+12] == 'x') ):
            l1 = 24;#wireguard_fix
        elif(i + 5 < len(b1) and (b1[i] == 'n' and b1[i+1] == 'o' ) and  (b1[i+2] == 's' and b1[i+3] == 'u' ) and (b1[i+4] == 'd' and b1[i+5] == 'o' )  ):
            l1 = 25#nosudo
        elif(i + 16 < len(b1) and (b1[i] == 'r' and b1[i+1] == 'u' ) and (b1[i+2] == 'n' and b1[i+3] == '_' ) and (b1[i+4] == 'i' and b1[i+5] == 'n' ) and (b1[i+6] == '_' and b1[i+7] == 'b' ) and (b1[i+8] == 'a' and b1[i+9] == 'c' ) and (b1[i+10] == 'k' and b1[i+11] == 'g')  and   (b1[i+12] == 'r' and b1[i+13] == 'o') and (b1[i+14] == 'u' and b1[i+15] == 'n') and (b1[i+16] == 'd') ):
            l1 = 26;#run_in_background
        elif(i + 4 < len(b1) and (b1[i] == 't' and b1[i+1] == 't' ) and (b1[i+2] == 'y' and b1[i+3] == 'o' ) and (b1[i+4] == 'n' )):
            l1 = 27;#ttyon
        elif(i + 21 < len(b1) and (b1[i] == 'p' and b1[i+1] == 'a' ) and (b1[i+2] == 'c' and b1[i+3] == 'm' ) and (b1[i+4] == 'a' and b1[i+5] == 'n' ) and (b1[i+6] == '_' and b1[i+7] == 'p' ) and (b1[i+8] == 'a' and b1[i+9] == 'k' ) and (b1[i+10] == 'g' and b1[i+11] == 'a')  and   (b1[i+12] == 'g' and b1[i+13] == 'e') and b1[i+14] == "_" and (b1[i+15] == 'i' and b1[i+16] == 'n') and (b1[i+17] == 's' and b1[i+18] == 't') and (b1[i+19] == 'a' and b1[i+20] == 'l') and (b1[i+21] == 'l' )):
            l1 = 28#pacman_pakgage_install
        elif(l1 >= 1):
            i = i +1;
            if(b1[i] != ' '):
                #config_temp = config_temp  + b1[i];
                i = i +1;
                while True:
                    if(i >= len(b1)):
                        break;
                    if(b1[i] == '\n'):
                        break;
                    if(b1[i] == '='):
                        l2 = 1;
                        if(b1[i+1] == ' '):
                            i = i +1;
                    elif(l2 == 1):
                        config_temp = config_temp  + b1[i];
                    i = i +1;
                if(l1 == 1):
                    config_temp1.append("docker_user");
                elif(l1 == 2):
                    config_temp1.append("gpu_render");
                elif(l1 == 3):
                    config_temp1.append("disk_device_name");
                elif(l1 == 4):
                    config_temp1.append("zugriff_auf_media");
                elif(l1 == 5):
                    config_temp1.append("sav_home_docker_folder");
                elif(l1 == 6):
                    config_temp1.append("share_folder_daten");
                elif(l1 == 7):
                    config_temp1.append("share_folder1_aktiv");
                elif(l1 == 8):
                    config_temp1.append("share_folder1");
                elif(l1 == 9):
                    config_temp1.append("network_disable");
                elif(l1 == 10):
                    config_temp1.append("steam_controller_bool");
                elif(l1 == 11):
                    config_temp1.append("usb_sharing");
                elif(l1 == 12):
                    config_temp1.append("usb_name");
                elif(l1 == 13):
                    config_temp1.append("usb_hidraw_name");
                elif(l1 == 14):
                    config_temp1.append("docker_build");
                elif(l1 == 15):
                    config_temp1.append("docker_input");
                elif(l1 == 16):
                    config_temp1.append("maxmemory");
                elif(l1 == 17):
                    config_temp1.append("maxcpus");
                elif(l1 == 18):
                    config_temp1.append("network_host");
                elif(l1 == 19):
                    config_temp1.append("portforwding");
                elif(l1 == 20):
                    config_temp1.append("dbus_rw");
                elif(l1 == 21):
                    config_temp1.append("pacman_cache");
                elif(l1 == 22):
                    config_temp1.append("dns");
                elif(l1 == 23):
                    config_temp1.append("ipv4");
                elif(l1 == 24):
                    config_temp1.append("wireguard_fix");
                elif(l1 == 25):
                    config_temp1.append("nosudo");
                elif(l1 == 26):
                    config_temp1.append("run_in_background");
                elif(l1 == 27):
                    config_temp1.append("ttyon");
                elif(l1 == 28):
                    config_temp1.append("pacman_pakgage_install");
                else:
                    print("ERROR l1 nciht gefunden!");
                    exit(-1);
                config_temp1.append(config_temp);
                config.append(config_temp1);
                config_temp1 = [];
                config_temp = "";
                l1 = -1;
                l2 = -1;

        i = i +1;
    print(config);
    return config;
