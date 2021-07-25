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




def list_path_einfache(path, link_ignore):
    sdir  = "";
    array = [0, sdir];
    if(link_ignore == 1):
        array = listpath_ohne_link(path, "", array, [], [], []);
        return array;
    else:
        array = listpath(path, "", array, [], [], []);
        return array;
    return array;


def listpath_ohne_link(path, rpath, array, idarray, patharray, ctime):
    #File list
    sdir = array[1];
    list = os.listdir(path)
    size = len(list);
    sout = "";
    i = 0;
    j = 0;
    if(size == 0):
        return [j, sdir, idarray, patharray];
    while True:
        spath = path + "/" + list[i];
        if(os.path.isdir(spath) == True):
            rpath2 = rpath + "/" + list[i];
            i =  i+1;
            array = [j, sdir];
            array = listpath(spath, rpath2, array, idarray, patharray, ctime);
            idarray = array[2];
            patharray = array[3];
            ctime = array[4];
            j = array[0];
            sdir = array[1];
            if( i== size):
                break;
        elif(os.path.islink(spath) == True):
            i = i+ 1;
            j = j +1;
            if( i== size):
                break;
        elif(os.path.isfile(spath) == True):
            sdir = sdir + "ID: " + str(j) + " | " + rpath + "/" + list[i] + "\n";
            idarray.append(j);
            s1 = rpath + "/" + list[i];
            patharray.append(s1);
            ctime.append(os.path.getmtime(spath));
            i = i+ 1;
            j = j +1;
            if( i== size):
                break;
        else:
            sdir = sdir + "ID: " + str(j) + " | " + rpath + "/" + list[i] + "\n";
            idarray.append(j);
            s1 = rpath + "/" + list[i];
            patharray.append(s1);
            ctime.append(os.path.getmtime(spath));
            i = i+ 1;
            j = j +1;
            if( i== size):
                break;
    return [j, sdir, idarray, patharray, ctime]


def listpath(path, rpath, array, idarray, patharray, ctime):
    #File list
    sdir = array[1];
    list = os.listdir(path)
    size = len(list);
    sout = "";
    i = 0;
    j = 0;
    if(size == 0):
        return [j, sdir, idarray, patharray];
    while True:
        spath = path + "/" + list[i];
        if(os.path.isdir(spath) == True):
            rpath2 = rpath + "/" + list[i];
            i =  i+1;
            array = [j, sdir];
            array = listpath(spath, rpath2, array, idarray, patharray, ctime);
            idarray = array[2];
            patharray = array[3];
            ctime = array[4];
            j = array[0];
            sdir = array[1];
            if( i== size):
                break;
        elif(os.path.islink(spath) == True):
            sdir = sdir + "ID: " + str(j) + " | " + rpath + "/" + list[i] + "\n";
            idarray.append(j);
            s1 = rpath + "/" + list[i];
            patharray.append(s1);
            ctime.append(os.path.getmtime(spath));
            i = i+ 1;
            j = j +1;
            if( i== size):
                break;
        elif(os.path.isfile(spath) == True):
            sdir = sdir + "ID: " + str(j) + " | " + rpath + "/" + list[i] + "\n";
            idarray.append(j);
            s1 = rpath + "/" + list[i];
            patharray.append(s1);
            ctime.append(os.path.getmtime(spath));
            i = i+ 1;
            j = j +1;
            if( i== size):
                break;
        else:
            sdir = sdir + "ID: " + str(j) + " | " + rpath + "/" + list[i] + "\n";
            idarray.append(j);
            s1 = rpath + "/" + list[i];
            patharray.append(s1);
            ctime.append(os.path.getmtime(spath));
            i = i+ 1;
            j = j +1;
            if( i== size):
                break;
    return [j, sdir, idarray, patharray, ctime]
