#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Kubespray.
#
#    Foobar is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Foobar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import logging
import shutil
import os
import sys
import netaddr
import netaddr.core
from git import Repo
from netaddr.strategy import eui48
from ansible.utils.display import Display
display = Display()

def validate_port(port):
    """
    Validates that a port is valid. Returns true if valid, false if not.
    """
    try:
        port_int = int(port)
        if port_int <= 0 or port_int > 65535:
            return False
        else:
            return True

    except ValueError:
        return False


def validate_ip_addr(addr, version=None):
    """
    Validates that an IP address is valid. Returns true if valid, false if
    not. Version can be "4", "6", None for "IPv4", "IPv6", or "either"
    respectively.
    """
    if version == 4:
        return netaddr.valid_ipv4(addr)
    elif version == 6:
        return netaddr.valid_ipv6(addr)
    else:
        return netaddr.valid_ipv4(addr) or netaddr.valid_ipv6(addr)


def canonicalise_ip(addr, version):
    if addr is None:
        return None
    ip = netaddr.IPAddress(addr, version=version)
    return intern(str(ip))


def validate_cidr(cidr, version):
    """
    Validates that a CIDR is valid. Returns true if valid, false if
    not. Version can be "4", "6", None for "IPv4", "IPv6", or "either"
    respectively.
    """
    try:
        ip = netaddr.IPNetwork(cidr, version=version)
        return True
    except (netaddr.core.AddrFormatError, ValueError, TypeError):
        return False


def canonicalise_cidr(cidr, version):
    if cidr is None:
        return None
    nw = netaddr.IPNetwork(cidr, version=version)
    return intern(str(nw))

def query_yes_no(question, default="yes"):
    """Question user input 'Yes' or 'No'"""
    valid = {"yes":True, "y":True, "no":False, "n":False}
    if default == None:
      prompt = " [y/n] "
    elif default == "yes":
      prompt = " [Y/n] "
    elif default == "no":
      prompt = " [y/N] "
    else:
      raise ValueError("Invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please answer with 'yes' or 'no' (or 'y' or 'n').\n")

def get_logger(logfile, loglevel):
    logger = logging.getLogger()
    handler = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(getattr(logging, loglevel.upper()))
    return logger

def clone_git_repo(name, directory, git_repo):
    if os.path.isdir(directory):
        shutil.rmtree(directory)
    display.banner('CLONING %s GIT REPO' % name.upper())
    Repo.clone_from(git_repo,directory)
    display.display('%s repo cloned' % name, color='green')
