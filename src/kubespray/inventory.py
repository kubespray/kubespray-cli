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
kubespray.inventory
~~~~~~~~~~~~

Ansible inventory management for Kubespray
"""

import os
import re
import functools
from kubespray.common import get_logger
from ansible.utils.display import Display
display = Display()

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


class CfgInventory(object):
    '''
    Read classic ansible inventory file.
    '''

    def __init__(self, options):
        self.options = options
        self.filename = os.path.join(
            options['kubespray_path'], 'inventory/inventory.cfg'
        )
        file = open(self.filename, 'w+')
        self.logger = get_logger(options.get('logfile'), options.get('loglevel'))

        ###
        # stack overflow code. I  bear you to jump the 4 following lines. Please forgive me
        config = StringIO()
        config.write('[HEADsection]\n')
        config.write(open(self.filename).read())
        config.seek(0, os.SEEK_SET)
        #####
        self.cparser = cparser = configparser.ConfigParser(allow_no_value=True)
        cparser.readfp(config)

        section = {}
        server_cache = {}
        for section_name in self.cparser.sections():
            current_section = self.read_section(section_name)
            section.setdefault(section_name, []).extend(current_section)
            server_cache[section_name] = {}
        self._section_dict = section
        self._server_cache = server_cache
        self._global_section = dict(section['HEADsection'])

    def read_section(self, section_name='HEADsection'):
        '''
        Read section (default is the fake section on top on the file), and
        return a list of tuple [(machine_name, dict_properties)]
        the dict propeties is {property_name: property_value} (value possibly unquoted)
        '''
        machine_list = []
        for line, properties_str in self.cparser.items(section_name):
            machine_part = line.split('#', 1)[0]  # get read of comments parts
            machine_part = line.split(None, 1)
            if len(machine_part) == 2:
                # machine_part = ['server_name', 'first_property_name']
                # property_str = 'first_property_value  second_property=second_value ...'
                if properties_str:
                    properties_str = machine_part[1] + '=' + properties_str
                else:
                    properties_str = machine_part[1]
                prop_parse = re.findall(
                    '([\w]+)(?:\s*=\s*(?P<quote>[\'"])?([^\'"=]+)(?P=quote)?|)\s*',
                    properties_str
                )
                properties = dict((key, value) for   key, quote, value in prop_parse)
            else:
                properties = {}
            machine_name = machine_part[0]
            machine_list.append((machine_name, properties))
        return machine_list

    def _get_node(self, section, server_name, server_properties=None):
        '''
        Return a server object, for a specific section?
        Properties given will overide global properties (properties
        At the top of the file without section name).
        For the same section and the same server name, the function will
        return the same object, with properties given
        at the first time the sever as been getted.
        '''
        cache_dict = self._server_cache[section]
        try:
            return cache_dict[server_name]
        except KeyError:
            #Make a copy of global_properties
            properties = dict(self._global_section.get(server_name, {}))
            properties.update(server_properties or {})
            cache_dict[server_name] = server = Server(server_name, properties)
            return server

    def _section_wrapper(self, section, nb=1, without=None):
        '''Function called for each attribute (section name)'''
        blacklist = list(map(str, without or []))

        def iter_server(server_list):
            for server_name, properties in server_list:
                if str(server_name) in blacklist:
                    continue
                else:
                    yield self._get_node(section, server_name, properties)

        gen_server = iter_server(self._section_dict[section])
        if nb >= 0:
            try:
                return [next(gen_server) for _ in range(nb)]
            except StopIteration:
                raise ValueError('There is no %s item(s) in group %s'%(
                    nb, section))
        else:
            return list(gen_server)

    def __getattr__(self, section):
        '''Attribute emulation'''
        if section in self._section_dict:
            return functools.partial(self._section_wrapper, section)
        else:
            raise AttributeError('No such attribute because '
                                    'no such section \'%s\' in file'%section)

    def write_inventory(self):
        '''Generates inventory'''
        if len(self.options['k8s_masters']) < 2:
            display.warning('You should set at least 2 masters')
        if len(self.options['k8s_nodes']) > 2:
            self.options['etcd_members'] = self.options['k8s_nodes'][0:3]
        else:
            self.options['etcd_members'] = [self.options['k8s_nodes'][0]]
            display.warning('You should set at least 3 nodes for etcd clustering')
        self.format_inventory_line('kube-node', self.options['k8s_nodes'])
        self.format_inventory_line('kube-master', self.options['k8s_masters'])
        self.format_inventory_line('etcd', self.options['etcd_members'])
        self.cparser.add_section('k8s-cluster:children')
        self.cparser.set('k8s-cluster:children', 'kube-master')
        self.cparser.set('k8s-cluster:children', 'kube-node')
        with open(self.filename, 'wb') as configfile:
            display.banner('WRITTING INVENTORY')
            self.cparser.write(configfile)
            self.logger.info('the inventory %s was successfuly generated' % self.filename)
            self.logger.debug('The following options were used to generate the inventory: %s' % self.options)
            display.display('Inventory generated : %s' % self.filename, color='green')

    def format_inventory_line(self, section, servers):
        inventory_hostnames = list()
        self.cparser.add_section(section)
        for srv in servers:
            inventory_hostname = srv.split('[')[0]
            self.cparser.set(section, inventory_hostname)
            inventory_hostnames.append(inventory_hostname)
            srv = srv.replace('[', '\t\t')
            srv = srv.replace(']', '')
            srv = srv.replace(',', ' ')
            if srv not in inventory_hostnames:
                self.cparser.set('HEADsection', srv)


class Server(str):

    def __new__(cls, name, properties=None):
        obj = super(Server, cls).__new__(cls, name)
        obj.properties = properties or {}
        return obj

    @property
    def ip(self):
        return self.properties.get('ansible_ssh_host', str(self))

    def __getattr__(self, key):
        try:
            return self.properties[key]
        except KeyError:
            raise AttributeError
