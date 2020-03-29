#!/usr/bin/env python3.8
#Copyright (C) 2020 vfio_experte
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.

import os
import os.path
import pty
import posixpath

version = "0.6f beta";
print(version);

#def system(cmd, sin = ""):
#	s1 = cmd.split(" ");
#	pipeout, pipein = pty.openpty();
#	process = subprocess.Popen(cmd,stdin=pipeout, stderr=subprocess.STDOUT);#stdout=pipein	
#	os.write(pipein, sin.encode());
#	os.close(pipeout);
#	process.wait();
#	return 0;
def system(cmd):
	os.system(cmd);


def read_WINEPREFIX():
	WINEPREFIX = "";
	try:
		WINEPREFIX = os.environ['WINEPREFIX'];
	except KeyError:
		home = os.environ['HOME'];
		WINEPREFIX = home + "/.wine";
	return WINEPREFIX;

def remnove_hardened(device, winefodler, block_output_folder):
	i = 0;
	while True:
		if(i >= len(device)):
			break;
		s2 = device[i];
		s1 = winefodler + "/" + s2 + ":";
		s3 = s1 + ":";
		#print("rm -f \"" + s1 + "\"");
		system("rm -f \"" + s1 + "\"");
		#print("rm -f \"" + s3 + "\"");
		system("rm -f \"" + s3 + "\"");
		i = i +1;

def add_hardened(device, winefodler, block_output_folder):
	remnove_hardened(device, winefodler, block_output_folder);
	i = 0;
	while True:
		if(i >= len(device)):
			break;
		s2 = device[i];
		s1 = winefodler + "/" + s2 + ":";
		#print("ln -sf " + "\"" + block_output_folder + "\" " + "\""  + s1 + "\"");
		system("ln -sf " + "\"" + block_output_folder + "\" " + "\""  + s1 + "\"");
		i = i +1;

#0 is hardened
#1 is remove hardened
def questions1(WINEPREFIX, config):
	while True:
		print("---------------");
		print(WINEPREFIX);
		print("[0]\twine prefix hardened");
		print("[1]\twine prefix remove hardened");
		choice = input("your choice?:");
		if(choice == '0'):
			if(os.path.isfile(config) == True):
				print("ERROR WINEPREFIX is hardened please start remove hardened before you run hardened!");
				exit();
			return 0;
		elif(choice == '1'):
			if(os.path.isfile(config) == False):
				print("ERROR WINEPREFIX not hardened please start hardened before you run remove hardened!");
				exit();
			return 1;
		else:
			print("Error bad input!");
	return -1;


def questions3(s1, s2):
	while True:
		print("---------------");
		if(os.path.islink(s1) == True):
			print(s2 + "\t[" + os.path.realpath(s1) + "]");
		else:
			print(s1);
		choice = input("deleting and add a dummy device?[y,n]");
		if(choice == 'y'):
			return 1;
		elif(choice == 'n'):
			return 2;
		else:
			print("Error bad input!");
	return -1;

def read_config_file(config):
	if(os.path.isfile(config) == False):
		return -1;
	file1 = open(config, "r");
	file1.seek(0, 2);
	size = file1.tell();
	file1.seek(0, 0);
	b1 = file1.read(size);
	file1.close();
	return b1;

def write_config_file(config, device_overide):
	file1 = open(config, "w");
	file1.write(device_overide)
	file1.close();
	return 0;	

def exist_device(device, mode, winefodler, config):
	if(mode == 1):
		if(os.path.isfile(config) == True):
			return(read_config_file(config));
	device_overide = "";
	i = 0;
	while True:
		if(i >= len(device)):
			break;
		s2 = device[i];
		s1 = winefodler + "/" + s2 + ":";
		if(os.path.islink(s1) == True):
			if(questions3(s1, s2) == 2):
				#no
				device_overide = device_overide + "0" + ",";
			else:
				device_overide = device_overide + "1" + ",";
		else:
			device_overide = device_overide + "1" + ",";
				
		i = i +1;
	return device_overide;


def calulate1(device, device_overide, block_device):
	device_rm = "";
	device_overide2 = device_overide.split(",");
	i =0;
	while True:
		if(i >= len(device)):
			break;
		if(device_overide2[i] == '1'):
			device_rm = device_rm + device[i] + ",";
		i = i + 1;
	return device_rm;


def questions2(WINEPREFIX, mode, block_device):
	while True:
		print("---------------");
		print("WINEPREFIX:");
		print(WINEPREFIX);
		print("---------------");
		if(mode == 0):
			print("create dummy devices: " +  block_device);
		else:
			print("rm dummy devices: " +  block_device);
		print("is all correct?");
		print("[y] yes");
		print("[n] no and cancel");
		choice = input("your choice?:");
		if(choice == 'y'):
			return 0;
		elif(choice == 'n'):
			return 1;
		else:
			print("Error bad input!");
			questions2(WINEPREFIX);
		print("---------------");
	return -1;


def restore_device_z(winefodler):
	s2 = winefodler + "/" + "z" + ":";
	while True:	
		print("---------------");
		if(os.path.islink(s2) == True):
			print("z" + "\t[" + os.path.realpath(s2) + "]");
		else:
			print("z");
		choice = input("restore device?[y,n]");
		if(choice == 'y'):
			print("restore z:");
			#print("ln -sf " + "/ " + "\"" + winefodler + "/z:" + "\"");
			os.system("ln -sf " + "/ " + "\"" + winefodler + "/z:" + "\"");
			return 1;
		elif(choice == 'n'):
			return 2;
		else:
			print("Error bad input!");
	return -1;
		
	
def main():
	#infos reading
	WINEPREFIX = "";
	WINEPREFIX = read_WINEPREFIX();
	if(os.path.isdir(WINEPREFIX) == False):
		print("WINEPREFIX: " + "\"" + WINEPREFIX + "\" not found!"); 
		exit();
	block_device = "a,b,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z"
	DEVICES = block_device.split(",");
	block_output_folder = "/tmp"
	device_overide = "";
	winefodler = WINEPREFIX + "/dosdevices"
	config = winefodler + "/.hardened.config";
	mode = 0;
	#0 is hardened
	#1 is remove hardened
	mode = questions1(WINEPREFIX, config);
	device_overide = exist_device(DEVICES, mode, winefodler, config);
	block_device = calulate1(DEVICES, device_overide, block_device);
	device = block_device.split(",");
	if(questions2(WINEPREFIX, mode, block_device) == 0):
		if(mode == 0):
			add_hardened(device, winefodler, block_output_folder);
			write_config_file(config, device_overide);
			system("wine64 winecfg");
			exit();
		elif(mode == 1):
			remnove_hardened(device, winefodler, block_output_folder);
			restore_device_z(winefodler);
			system("rm \"" + config + "\"");
			system("wine64 winecfg");
			exit();
		else:
			print("FANTAL ERROR");
			exit();
	
	
main();

