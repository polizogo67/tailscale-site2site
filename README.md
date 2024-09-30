# Tailscale-site2site
Unify you remote networks into a mesh and make everything accessible site to site

Find the [Official Guide](https://tailscale.com/kb/1214/site-to-site) from Tailscale's documentation here.

## Site to Site Networking

You can use site-to-site layer 3 (L3) networking to securely connect two or more subnets on your tailnet.

To create a site-to-site connection between two or more subnets:

1. Select a device within each subnet to act as the subnet router.
2. Configure the subnet routers ([Docs](https://tailscale.com/kb/1019/subnets)):
    1. Install the Tailscale client.
    2. Enable IP forwarding.
    3. Start the Tailscale client with the appropriate configuration options, such as disabling SNAT
3. Approve the subnet routers.
4. Configure the other devices on each subnet.
5. Test the connection between the subnets.

## Example Scenario

| Subnet                    | Subnet A      | Subnet B          |
|----------                 |----------     |----------         |
| Subnet CIDR range         | 192.0.2.0/24  | 198.51.100.0/24   |
| Subnet router IP address  | 192.0.2.2     | 198.51.100.2      |

## Usage

```bash
git clone ...
cd tailscale-site2site
```

### Subnet Router
Gonfigure a subnet router using [linux_router.sh](tools/linux_router.sh)
Replace the advertised subnet you the routers subnet.
```bash
chmod +x tools/linux_router.sh
./tools/linux_router.sh 192.168.1.0/24
```

Alternative, you can follow the process from the [docs](https://tailscale.com/kb/1019/subnets).

You can ping other Tailscale clients by running:
```bash
tailscale status    # lists the tailscale nodes
tailscale ping node # choose & ping an online node
tailscale netcheck  # latency from the relays
```

Perform Test
```bash
# One one Node run
iperf3 -s
# On the other node run
iperf3 -c node
```

Usefull Commands
```bash
ip route show table 52  # Tailscale routing table
```

Add Route to other devices
```bash
sudo ip route add 192.168.69.0/24 via 192.168.1.100
ip route show
tracepath -n 192.168.69.20
```