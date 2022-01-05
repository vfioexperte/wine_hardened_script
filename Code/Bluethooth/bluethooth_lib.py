#!/usr/bin/env python
#Copyright (C) 2022  vfio_experte
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

from Code.Usb.usb_lib import *

def check_device_isopen_bluethoot(filepath):
    try:
        tmp = os.open(filepath, os.O_RDONLY);
        os.close(tmp);
        return 1;
    except PermissionError:
        return 0;
    except TypeError:
        return 0;
    except FileNotFoundError:
        return 0;
    return 1;

def find_bluethoot_devides():
    i = 0;
    bdevs = [];
    while True:
        if(i >= 100):
            break;
        if(check_device_isopen_bluethoot("/dev/hiddev" + str(i) == 1)):
            bdevs.append("/dev/hiddev" + str(i));
        i = i +1;
    return bdevs;
