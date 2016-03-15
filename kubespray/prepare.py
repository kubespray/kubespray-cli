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

"""
kubespray.prepare
~~~~~~~~~~~~

Generates Ansible inventory to be used with Kubespray
"""
import sys
import yaml
from kubespray.common import get_logger,query_yes_no
from pprint import pprint
from ansible.utils.display import Display

display = Display()
def gen_inventory(options):
    logger = get_logger(options.get('logfile'), options.get('loglevel'))

#class Prepare(object):
#
#    def __init__(self, configfile='/etc/kubespray/kubespray.yml'):
#        self.display = Display()
#        self.configfile = configfile
#        self.logfile = None
#        self.loglevel = None
#
#    def parse_configfile(self):
#        """
#        Retrieve configuration parameters from the config file
#        """
#        try:
#            with open(self.configfile, "r") as f:
#                config = yaml.load(f)
#        except:
#            self.display.error("Can't read configuration file %s" % self.configfile)
#            sys.exit(1)
#        return config
