import fileinput
from subprocess import call

class DIMSetupManager:

    def __init__(
            self, distro, package_manager, apache_package, apache_config, 
            nginx_package, nginx_config, iptables_savefile):
        self.distro = distro
        self.package_manager = package_manager
        self.apache_package = apache_package
        self.apache_config = apache_config
        self.nginx_package = nginx_package
        self.nginx_config = nginx_config
        self.iptables_savefile = iptables_savefile

    def get_distro(self):
        return self.distro

    def update_packages(self):
        call([self.package_manager, "-y", "update"])
        call([self.package_manager, "-y", "upgrade"])

    def allow_binding_to_loopback(self, sysconfig_file):
        with open(sysconfig_file, "a") as sysctl_conf:
            sysctl_conf.write("net.ipv4.conf.all.route_localnet = 1\n")

    def install_iptables(self):
        call(["systemctl", "stop", "firewalld"])
        call(["systemctl", "mask", "firewalld"])
        call([self.package_manager, "-y", "iptables-service"])
        call(["systemctl", "enable", "iptables"])

    def install_apache(self):
        call([self.package_manager, "-y", "install", self.apache_package])
        
    def configure_apache(self, apache_port):
        with fileinput.FileInput(self.apache_config, 
                                 inplace=True, backup='.bak') as config:
            for line in config:
                if "Listen 80\n" in line:
                    print(line.replace("Listen 80",
                                       "Listen 127.0.0.1:" + str(apache_port)), end='')
                else:
                    print(line, end='')

    def start_apache(self):
        call(["service", self.apache_package, "restart"])
        call(["systemctl", "enable", self.apache_package])

    def install_nginx(self):
        if "CentOS" in self.distro:
            call([self.package_manager, "-y", "install", "epel-release"])
        call([self.package_manager, "-y", "install", self.nginx_package])

    def configure_nginx(self, nginx_port):
        with fileinput.FileInput(self.nginx_config, inplace=True, backup='.bak') as config:
            for line in config:
                if ' 80 default' in line:
                    print(line.replace(" 80", " 127.0.0.1:" + str(nginx_port)),
                          end='')
                elif ' [::]:80 default' in line:
                    print(line.replace(" [::]:80", " [::1]:" + str(nginx_port)),
                          end='')
                else:
                    print(line, end='')

    def start_nginx(self):
        call(["service", self.nginx_package, "restart"])
        call(["systemctl", "enable", self.nginx_package])
 
    def add_iptables_masquerade(self):
        call(["iptables", "-t", "nat", "-A", "POSTROUTING", "-j", "MASQUERADE"])

    def save_iptables(self):
        with open(self.iptables_savefile,"w") as iptables_rules:
            call(["iptables-save"], stdout=iptables_rules)

