# Tailscale-site2site
Unify you remote networks into a mesh and make everything accessible site to site

Find the [Official Guide](https://tailscale.com/kb/1214/site-to-site) from Tailscale's documentation here.

## Site to Site Networking

You can use site-to-site layer 3 (L3) networking to securely connect two or more subnets on your tailnet.

To create a site-to-site connection between two or more subnets:

1. Select a device within each subnet to act as the subnet router.
2. Configure the subnet routers:
    1. Install the Tailscale client.
    2. Enable IP forwarding.
    3. Start the Tailscale client.
3. With the appropriate configuration options, such as disabling SNAT
4. Approve the subnet routers.
5. Configure the other devices on each subnet.
Test the connection between the subnets.

## Example Scenario

| Subnet                    | Subnet A      | Subnet B          |
|----------                 |----------     |----------         |
| Subnet CIDR range         | 192.0.2.0/24  | 198.51.100.0/24   |
| Subnet router IP address  | 192.0.2.2     | 198.51.100.2      |
