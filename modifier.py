import socket
import struct
import psutil
from itertools import product
import os
import platform
import yaml
from typing import List, Set

def get_network_interfaces():
    interfaces = psutil.net_if_addrs()
    ipv4_addr = {}

    for interface_name, interface_addresses in interfaces.items():
        for address in interface_addresses:
            if address.family == socket.AF_INET:  # IPv4 address
                ipv4_addr[interface_name] = address.address
        #     elif address.family == socket.AF_INET6:  # IPv6 address
        #         ip_addresses[interface_name] = address.address
    return ipv4_addr


def ip_in_subnet(ip, subnet):
    ipaddr = struct.unpack('>I', socket.inet_aton(ip))[0]
    netaddr, bits = subnet.split('/')
    netaddr = struct.unpack('>I', socket.inet_aton(netaddr))[0]
    mask = (0xFFFFFFFF << (32 - int(bits))) & 0xFFFFFFFF
    return (ipaddr & mask) == (netaddr & mask)

def filter_known_subnets(subnets):
    ipv4 = get_network_interfaces()
    unknown = set(subnets)
    for ip, subnet in product(ipv4.values(), subnets):
        if ip_in_subnet(ip, subnet):
            print(f"DISCARDING: IP {ip} belongs to subnet {subnet}")
            unknown.discard(subnet)
            break
    return sorted(unknown)


def create_ip_routes_linux(subnets, gateway:str):
    script = "#!/bin/bash\n"
    for subnet in subnets:
        script += f"sudo ip route add {subnet} via {gateway}\n"
    script += "ip route show\n"

    # Add Comments to revert changes
    script += "\n# Commands to delete the routes\n"
    for subnet in subnets:
        script += f"# sudo ip route del {subnet} via {gateway}\n"

    # Save File
    script_path = "./add_routes.sh"
    with open(script_path, "w") as file: file.write(script)
    print(f"Script saved to {script_path}")

    # Execute Script
    os.chmod("./add_routes.sh", 0o755)
    os.system(script_path)

def create_ip_routes_windows(subnets, gateway:str):
    script = "\n"
    for subnet in subnets:
        script += f"New-NetRoute -DestinationPrefix {subnet} -NextHop {gateway} \n"

    script += "Get-NetRoute\n"

    # Add Comments to revert changes
    script += "\n# Commands to delete the routes\n"
    for subnet in subnets:
        script += f"# Remove-NetRoute -DestinationPrefix {subnet} -NextHop {gateway}\n"

    # Save File
    script_path = "./add_routes.ps1"
    with open(script_path, "w") as file:
        file.write(script)
    print(f"Script saved to {script_path}")

    # Execute Script
    os.system(f"powershell -ExecutionPolicy Bypass -File {script_path}")

class ConfigParser:

    def __init__(self, path:str) -> None:
        self.path:str = path
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        with open(path, 'r') as file:
            self.data = yaml.safe_load(file)

    def getGateway(self) -> str:
        return self.data['gateway']

    def getSubnets(self) -> Set[str]:
        return set(self.data['subnets'])

    def __repr__(self) -> str:
        return str(self.data)


def main() -> None:

    import argparse
    import yaml

    parser = argparse.ArgumentParser(description="Create IP routes for Site 2 Site GATEWAY")
    parser.add_argument("--config", "-cfg", type=str, required=True, help="Path to the configuration YAML file")
    parser.add_argument("--gateway", "-g", type=str, help="Path to the configuration YAML file")
    args = parser.parse_args()

    cfg = ConfigParser(args.config)

    unknown = filter_known_subnets(cfg.getSubnets())

    os_type = platform.system()
    print(f"Running on {os_type} ...")

    match os_type:
        case "Windows":
            create_ip_routes_windows(unknown, cfg.getGateway())
        case "Linux":
            # create_ip_routes_linux(unknown, cfg.getGateway())
            create_ip_routes_windows(unknown, cfg.getGateway())



if __name__ == "__main__":
    main()