#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Kargo.
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
kargo.inventory
~~~~~~~~~~~~

Ansible inventory management for Kargo
"""

import re
from kargo.common import get_logger
from ansible.utils.display import Display
display = Display()

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


class CfgInventory(object):
    '''
    Read classic ansible inventory file.
    '''

    def __init__(self, options, platform):
        self.options = options
        self.platform = platform
        self.inventorycfg = options['inventory_path']
        file = open(self.inventorycfg, 'w+')
        self.logger = get_logger(options.get('logfile'), options.get('loglevel'))
        self.cparser = configparser.ConfigParser(allow_no_value=True)

    def format_inventory(self, instances):
        inventory = {'all': {'hosts': []},
                     'kube-master': {'hosts': []},
                     'etcd': {'hosts': []},
                     'kube-node': {'hosts': []},
                     'k8s-cluster:children': {'hosts': [
                          {'hostname': 'kube-node', 'hostvars': []},
                          {'hostname': 'kube-master', 'hostvars': []}
                          ]},
                    }
        if len(instances) > 1:
            k8s_masters = instances[0:2]
        else:
            k8s_masters = [instances[0]]
        if len(instances) > 2:
            etcd_members = instances[0:3]
        else:
            etcd_members = [instances[0]]
        if self.platform in ['aws', 'gce']:
            for idx, host in enumerate(instances):
                inventory['all']['hosts'].append(
                    {'hostname': 'node%s' % str(idx + 1), 'hostvars': [
                        {'name': 'ansible_ssh_host', 'value': host['public_ip']}
                        ]}
                )
                inventory['kube-node']['hosts'].append(
                    {'hostname': 'node%s' % str(idx + 1),
                     'hostvars': []}
                )
            for idx, host in enumerate(k8s_masters):
                inventory['kube-master']['hosts'].append(
                    {'hostname': 'node%s' % str(idx + 1),
                     'hostvars': []}
                )
            for idx, host in enumerate(etcd_members):
                inventory['etcd']['hosts'].append(
                    {'hostname': 'node%s' % str(idx + 1),
                     'hostvars': []}
                )
        elif self.platform == 'metal':
            for host in instances:
                r = re.search('(^.*)\[(.*)\]', host)
                inventory_hostname = r.group(1)
                var_str = r.group(2)
                hostvars = list()
                for var in var_str.split(','):
                    hostvars.append({'name': var.split('=')[0], 'value': var.split('=')[1]})
                inventory['all']['hosts'].append(
                    {'hostname': inventory_hostname, 'hostvars': hostvars}
                )
                inventory['kube-node']['hosts'].append(
                    {'hostname': inventory_hostname, 'hostvars': []}
                )
            for host in k8s_masters:
                inventory['kube-master']['hosts'].append(
                    {'hostname': host.split('[')[0], 'hostvars': []}
                )
            for host in etcd_members:
                inventory['etcd']['hosts'].append(
                    {'hostname': host.split('[')[0], 'hostvars': []}
                )
        return(inventory)

    def write_inventory(self, instances):
        '''Generates inventory'''
        if len(instances) < 2:
            display.warning('You should set at least 2 masters')
        if len(instances) < 3:
            display.warning('You should set at least 3 nodes for etcd clustering')
        inventory = self.format_inventory(instances)
        for key, value in inventory.items():
            self.cparser.add_section(key)
            for host in value['hosts']:
                hostvars = str()
                varlist = list()
                for var in host['hostvars']:
                    varlist.append("%s=%s" % (var['name'], var['value']))
                hostvars = " ".join(varlist)
                self.cparser.set(key, "%s\t\t%s" % (host['hostname'], hostvars))
        with open(self.inventorycfg, 'wb') as configfile:
            display.banner('WRITTING INVENTORY')
            self.cparser.write(configfile)
            self.logger.info(
                'the inventory %s was successfuly generated'
                % self.inventorycfg
            )
            self.logger.debug(
                'The following options were used to generate the inventory: %s'
                % self.options
            )
            display.display(
                'Inventory generated : %s'
                % self.inventorycfg, color='green'
            )
