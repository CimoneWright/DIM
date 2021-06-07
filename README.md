# DARE MTD 

Python implimentation requires Python3 with standard library 
External Dependencies: None 

This is a simple iptables implementation of a Moving Target Defense rotating the webservers hosting an application. It 
rotates between Apache and Nginx.

The rotating application is on port 80. This is achived by using iptables prerouting and postroutning on the nat table 
to forward packets to Apache and Nginx which are only listening on localhost.

This is currently designed to run on the following operating systems:

* CentOS 7
* Ubuntu 16.0.4
* Debian 9 

Future support should include:

* FreeBSD
* OpenSuse
* Windows (This will require a creative solution maybe bash on windows or cygwin)

## Setup instructions
1. Setup a machine with one of the supported operating systems
2. Setup networking
3. Download Code
4. run the setup.py script. This will configure everything.
5. reboot the system. 
6. run the rotation.sh script to start the rotation.

NOTE: Installation on CentOS requires the use of python3.

After the system is setup, the python setup file can be ran to test the system.

#Production
Example starter
sudo docker run -d -p 27017:27017 --name mongodb mongo

sudo python3 main.py -i 192.168.122.14 -l 80 -m 6 -M 6 -a 8008 -n 8009 -r ./test_iptables.rules -t False


##Helpful commands to filter ports
1. Inspect listing port
``netstat -tulpn | grep :80``
2. find out what is using a port
``lsof -i :80 | grep LISTEN``

#fix to iptables
1. sudo apt-get install tofrodos
2. fromdos /etc/iptables.rules
