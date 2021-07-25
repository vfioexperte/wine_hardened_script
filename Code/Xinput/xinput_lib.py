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


def list_all_devices():
    devinput = "/dev/input/by-id/";
    array = list_path_einfache(devinput, 0);
    patharray = array[3];
    print(patharray);
    return patharray;

def add_input_device(namedeives):
    devinput = "/dev/input/by-id";
    found_devices = list_all_devices();
    tmp = namedeives.split(",");
    out = [];
    if(len(tmp) >= 1):
        for tmp3 in found_devices:
            for tmp2 in tmp:
                if(tmp3.find(tmp2) >= 1):
                    out.append(devinput + tmp3);
    return out;
