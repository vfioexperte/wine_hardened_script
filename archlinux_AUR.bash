#!/bin/bash
#v0.2a
./command_root 'echo " %wheel ALL=(ALL) NOPASSWD: ALL" >>/etc/sudoers && su empty'
