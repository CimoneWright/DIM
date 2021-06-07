#!/usr/bin/python

# This is a Python version of the DARE setup script
# This script supports the following OS's currently:
# - CentOS 7
# - Ubuntu 16.04
# - Debian 9

import distro
import platform
import sys
import getpass
from subprocess import call
from dim_setup_manager import DIMSetupManager

if __name__=='__main__':
    # Check user is root
    if getpass.getuser() != 'root':
        print("This script must be run as root or with the 'sudo' command!")
        exit(1)
    # Check that we are using Python 3
    try:
        assert sys.version_info >= (3,0)
    except AssertionError:
        print("This script requires Python 3!")
        exit(1)
    # Identify the operating system and initialize
    print("Detecting operating system")
    if "Linux" in platform.system():
        distro, version, sub = distro.linux_distribution()
        if "CentOS" in distro:
            print("Detected CentOS")
            dim_setup = DIMSetupManager("CentOS", "yum", "httpd",
                                   "/etc/httpd/conf/httpd.conf", "nginx_webserver",
                                   "/etc/nginx_webserver/nginx_webserver.conf",
                                   "/etc/sysconfig/iptables")
        elif "debian" in distro:
            print("Detected Debian")
            dim_setup = DIMSetupManager("debian", "apt-get", "apache2",
                                   "/etc/apache2/ports.conf", "nginx_webserver",
                                   "/etc/nginx_webserver/sites-enabled/default",
                                   "/etc/iptables.rules")
        elif "Ubuntu" in distro:
            print("Detected Ubuntu")
            dim_setup = DIMSetupManager("debian", "apt-get", "apache2",
                                   "/etc/apache2/ports.conf", "nginx",
                                   "/etc/nginx/sites-enabled/default",
                                   "/etc/iptables.rules")
    if not dim_setup:
        print("Unsupported or unrecognized operating system")
        exit(1)
    dim_setup.update_packages()
    dim_setup.allow_binding_to_loopback("/etc/sysctl.conf")
    call(["sysctl", "-w", "net.ipv4.conf.all.route_localnet=1"])
    if dim_setup.get_distro()=="CentOS":
        dim_setup.install_iptables()
    dim_setup.install_apache()
    dim_setup.configure_apache("8008")
    dim_setup.start_apache()
    dim_setup.install_nginx()
    dim_setup.configure_nginx("8009")
    call(["rm", dim_setup.nginx_config + ".bak"])
    dim_setup.start_nginx()
    dim_setup.add_iptables_masquerade()
    dim_setup.save_iptables()
    print("Setup complete!")
    print("Restart your system. Then configure Apache and Nginx to serve")
    print("your application. Finally, run 'python3 main.py' to start rotation.")

