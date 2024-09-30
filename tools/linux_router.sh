#!/bin/bash


# Install Tailscale
curl -sSL https://tailscale.com/install.sh | sh

# Check if CIDR argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <CIDR>"
    exit 1
fi

echo "Advertising: $1"

# Enanble IP forwarding
# echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.conf
# echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.conf
# sudo sysctl -p /etc/sysctl.conf
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
sudo sysctl -p /etc/sysctl.d/99-tailscale.conf



# Start Tailscale with advertise-routes
tailscale up --advertise-routes=$1 --snat-subnet-routes=false --accept-routes