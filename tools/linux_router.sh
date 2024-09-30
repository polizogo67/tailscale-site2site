#!/bin/bash

# # Install Tailscale
# curl -sSL https://tailscale.com/install.sh | sh

# # Enanble IP forwarding
# echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.conf
# echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.conf
# sudo sysctl -p /etc/sysctl.conf

# Check if CIDR argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <CIDR>"
    exit 1
fi

# Start Tailscale with advertise-routes
# tailscale up --advertise-routes=$1 --snat-subnet-routes=false --accept-routes
exho $1