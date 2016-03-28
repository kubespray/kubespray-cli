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
kubespray.cloud
~~~~~~~~~~~~

Run Instances on cloud providers and generates inventory
"""

import sys
import os
import yaml
from subprocess import PIPE, STDOUT, Popen, check_output, CalledProcessError
from kubespray.common import get_logger, query_yes_no
from ansible.utils.display import Display
from pprint import pprint
display = Display()


class Cloud(object):
    '''
    Run Instances on cloud providers and generates inventory
    '''
    def __init__(self, options, cloud):
        self.options = options
        self.playbook = os.path.join(options['kubespray_path'], 'local.yml')
        self.inventorycfg = os.path.join(options['kubespray_path'], 'inventory/local.cfg')
        self.logger = get_logger(
            options.get('logfile'),
            options.get('loglevel')
        )
        self.pbook = [{
            'gather_facts': False,
            'hosts': 'localhost',
            'sudo': False,
            'tasks': []
        }]
        self.logger.debug('''
             The following options were used to generate the inventory: %s
             ''' % self.options)

    def write_local_inventory(self):
        '''Generates inventory for local tasks'''
        self.cparser.add_section('local')
        self.cparser.set('local', 'localhost')
        with open(self.filename, 'wb') as self.inventorycfg:
            self.cparser.write(self.inventorycfg)

class AWS(Cloud):

    def __init__(self, options):
        Cloud.__init__(self, options, "aws")
        self.options = options

    def gen_playbook(self):
        data = self.options
        data.pop('func')
        # Options list of ansible EC2 module
        ec2_options = [
            'aws_access_key', 'aws_secret_key', 'count', 'group',
            'instance_type', 'key_name', 'region', 'vpc_subnet_id',
            'image'
        ]
        # Define EC2 task
        ec2_task = {'ec2': {},
                    'name': 'Provision EC2 instances',
                    'register': 'ec2'}
        for opt in ec2_options:
            if opt in self.options.keys():
                d = {opt: self.options[opt]}
                ec2_task['ec2'].update(d)
        self.pbook[0]['tasks'].append(ec2_task)
        # Create inventory from template task
        self.pbook[0]['tasks'].append(
            {'name': 'Template the inventory',
             'template': {'dest': '{{ inventory_path }}',
                          'src': 'templates/inventory.ini.j2'}}
        )
        # Wait for ssh task
        self.pbook[0]['tasks'].append(
            {'local_action': {'host': '{{ item.public_ip }}',
                              'module': 'wait_for',
                              'port': 22,
                              'state': 'started',
                              'timeout': 300},
             'name': 'Wait until SSH is available',
             'with_items': 'ec2.instances'} 
        )
        pprint(self.pbook)
        try:
            with open(self.playbook, "w") as pb:
                pb.write(yaml.dump(self.pbook, default_flow_style=True))
        except IOError:
            display.error('Cant write the playbook %s' % self.playbook)
            sys.exit(1)
        cmd = [os.path.join(self.options['ansible_path'], 'ansible-playbook'),
            '-i', self.inventorycfg, self.playbook]
        try:
            proc = Popen(cmd, stdout=PIPE, stderr=STDOUT, universal_newlines=True, shell=False)
            with proc.stdout:
                for line in iter(proc.stdout.readline, b''):
                     print(line),
            proc.wait()
        except CalledProcessError as e:
            display.error('Deployment failed: %s' % e.output)
            self.logger.critical('Cannot create instances: %s' % e.output)
            sys.exit(1)

