#!/bin/bash

source ~/.bashrc
porteGGA=$1

echo "Porte: TCP$porteGGA 2100$porteGGA"
gnome-terminal -t "GNSSTest" -- bash -c "nc -v 192.168.70.2 2100$porteGGA >> GGA_Ping.txt;"
gnome-terminal -t "NetworkTest" -- bash -c "ping 8.8.8.8 >> GGA_Ping.txt;"
