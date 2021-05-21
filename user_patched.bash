#!/bin/bash
#version=0.1
usermod -u 1000 empty
rm /dev/input/* 
/root/chmod_check.py 'empty' '1000' 
export PWD=/home/empty
su empty
