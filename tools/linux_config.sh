#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <IP_ADDRESS>"
    exit 1
fi

IP_ADDRESS=$1
CURRENT_SUBNET=$(ip -o -f inet addr show | awk '/scope global/ {print $4}' | cut -d/ -f1 | cut -d. -f1-3)

if [[ $IP_ADDRESS == $CURRENT_SUBNET.* ]]; then
    echo "The IP address is in the current subnet. Exiting."
    exit 1
fi
sudo ip route add 192.168.1.0/24    via $IP_ADDRESS
sudo ip route add 192.168.69.0/24   via $IP_ADDRESS
sudo ip route add 192.168.70.0/24   via $IP_ADDRESS
sudo ip route add 192.168.71.0/24   via $IP_ADDRESS
sudo ip route add 192.168.72.0/24   via $IP_ADDRESS

ip route show
