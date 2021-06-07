import argparse
import getpass
import sys
import ipaddress
import socket
import errno
from pathlib import Path

class ParameterParser:

    def __init__(self):
        self.aparser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        self.parse_command_line_args()

    def is_root_user(self):
        is_root = False
        if getpass.getuser() == 'root':
            is_root = True
        else:
            print("This script must be run as root or with the 'sudo' command!")
        return is_root

    def has_python_version_greater_than_3(self):
        is_python3 = False
        try:
            assert sys.version_info >= (3, 0)
            is_python3 = True
        except AssertionError:
            print("This script requires Python 3!")
        return is_python3

    def is_valid_ip(self, args):
        # Setting external IP of the server from user input
        is_ip = False
        if args.external_ip:
            try:
                args.external_ip = ipaddress.ip_address(str(args.external_ip))
                is_ip = True
            except ValueError as error:
                print(error)
                print("The IP address you entered is invalid")
        return is_ip

    def has_iptables_file(self, args):
        has_file = False
        iptables_path = Path(args.iptables_rules)
        if iptables_path.exists():
            has_file = True
        else:
            print("iptables file path is invalid")
        return has_file

    def is_valid_rotation_time(self, args):
        is_valid = False
        min_wait = args.min_wait_sec
        max_wait = args.max_wait_sec
        # check for valid range for wait values and sets them based on user input or defaults min=1 max=5
        if max_wait < min_wait:
            raise ValueError('Max wait "{}" cannot be less than min wait "{}"'.format(
                str(max_wait), str(min_wait)))
        elif min_wait == None or max_wait == None:
            raise AttributeError("You must set the min wait and max wait times on" +
                                 "this object before calling this function.")
        else:
            is_valid = True
        return is_valid

    def is_open_port(self, port):
        open_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            is_open = open_socket.connect_ex(('localhost', port)) == 0
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                print("Port:", port, " is already in use")
            else:
                print(e)
        return is_open

    def parse_command_line_args(self):
        self.aparser.add_argument("-i", "--host_ip", action="store", default=None, required=True,
                             dest="external_ip", help="\n".join([
                "Set the external IP address of the server"]))
        self.aparser.add_argument("-l", "--live_port", action="store", default=80, type=int,
                             dest="live_port", help="\n".join([
                "set the live port that public requests will be coming from"]))
        self.aparser.add_argument("-m", "--min_wait_sec", action="store", default=1, type=int,
                             dest="min_wait_sec", help="\n".join([
                "set the minimum rotation time that will be randomly selected"]))
        self.aparser.add_argument("-M", "--max_wait_sec", action="store", default=5, type=int,
                             dest="max_wait_sec", help="\n".join([
                "set the maximum rotation time that will be randomly selected"]))
        self.aparser.add_argument("-a", "--apache_port", action="store", default=8008, type=int,
                             dest="apache_port", help="\n".join([
                    "set the port that apache is listening to on localhost"]))
        self.aparser.add_argument("-n", "--nginx_port", action="store", default=8009, type=int,
                             dest="nginx_port", help="\n".join([
                    "set the port that nginx_webserver is listening to on localhost"]))
        self.aparser.add_argument("-r", "--rules", action="store", required=True, type=str,
                             dest="iptables_rules", help="\n".join([
                "set the location of the iptables rules save file" + "\n" +
                "Defaults by operating system:" + "\n" +
                "- Ubuntu/Debian: /etc/iptables.rules" + "\n" +
                "- CentOS: /etc/sysconfig/iptables"]))
        self.aparser.add_argument("-t", "--test_flag", action="store", default=False, required=True, type=bool,
                                  dest="test_flag", help="\n".join([
                "Set the test flag to gather data"]))

    def has_invalid_input(self):
        args = self.get_args()
        return not (self.is_root_user() and
                self.has_python_version_greater_than_3() and
                self.is_valid_ip(args) and
                self.is_valid_rotation_time(args) and
                self.has_iptables_file(args))

    def get_args(self):
        return self.aparser.parse_args()