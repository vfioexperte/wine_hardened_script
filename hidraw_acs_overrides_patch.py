#!/usr/bin/env python
#Copyright (C) 2022  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#Warnung der Programmierer hafte nicht auf Schäden oder auf unsachgemäßen Umgang der APP

# -*- coding: utf-8 -*-
version = "0.1b"
print(version);


import platform
import os
import sys
import string
import stat

def check_device_isopen_hidraw(filepath):
    try:
        tmp = os.open(filepath, os.O_RDONLY);
        os.close(tmp);
        return 1;
    except PermissionError:
        return 1;
    except TypeError:
        return 1;
    except FileNotFoundError:
        return 0;
    return 1;

def main():
    i = 0;
    while True:
        if(i >= 100):
            break;
        if(check_device_isopen_hidraw("/dev/hidraw" + str(i)) == 0):
            i = i +1;
            continue;
        os.system("chmod -R 777 " + "/dev/hidraw" + str(i));
        i = i +1;
    print("hidraw acs overrides gepatch!")
main();
