#!/bin/bash

# Install Tailscale
curl -sSL https://tailscale.com/install.sh | sh

# Check if CIDR argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <CIDR>"
    exit 1
fi

echo "Advertising: $1"

sudo rm -rf /etc/sysctl.d/99-tailscale.conf
# Enanble IP forwarding
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
sudo sysctl -p /etc/sysctl.d/99-tailscale.conf

# Start Tailscale with advertise-routes
sudo tailscale up --advertise-routes=$1 --accept-routes #  --snat-subnet-routes=false
iptables -t mangle -A FORWARD -o tailscale0 -p tcp -m tcp \
        --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu