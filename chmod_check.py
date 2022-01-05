#!/usr/bin/env python
#Copyright (C) 2020  vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.
#Warnung der Programmierer hafte nicht auf Schäden oder auf unsachgemäßen Umgang der APP

# -*- coding: utf-8 -*-
version = "0.1f"
print(version);


import platform
import os
import sys
import string
import stat

def gourp_check(filepath):
    statt = os.stat(filepath);
    #print(statt);
    return statt.st_uid;

def check_file_exist(spath):
    if(os.path.isfile(spath) == False):
        uid = "-1";
        file1 = open(spath, "w");
        file1.close();
        print("create file look");
        return 1;
    return 0;



def main():
    if(len(sys.argv) > 1):
        username = sys.argv[1];
        uid = sys.argv[2];
        sfiel = "";
        if(check_file_exist("/home/" + username + "/daten/docker_user.look") == 1):
            uid = -1;
            sfiel = "/home/" + username + "/daten/docker_user.look";
        elif(check_file_exist("/home/" + username + "/daten/docker_user.look") == 0):
            sfiel = "/home/" + username + "/daten/docker_user.look";
        elif(check_file_exist("/home/" + username + "/docker_user.look") == 1):
            uid = -1;
            sfiel = "/home/" + username + "/docker_user.look";
        elif(check_file_exist("/home/" + username + "/docker_user.look") == 0):
            sfiel = "/home/" + username + "/docker_user.look";
        else:
            sfiel = "/home/" + username + "/docker_user.look";
        tmp = gourp_check(sfiel);
        print(tmp);
        if(uid == str(tmp)):
            print("OK");
        else:
            print("not OK");
            scmd = "chown -R " + username + ":users " + "/home/" + username;
            print(scmd);
            os.system(scmd);
            scmd2 = "chmod -R 777 " + "/home/" + username;
            print(scmd2);
            os.system(scmd);
    return 0;
main();
