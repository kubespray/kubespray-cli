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
kubespray.deplay.baremetal
~~~~~~~~~~~~

Deploy kubernetes on a baremetal infrastructure
"""

import sys
import os
import re
from subprocess import PIPE,STDOUT,Popen,check_output
from kubespray.common import get_logger,query_yes_no
from ansible.utils.display import Display
display = Display()

def run_playbook(options):
    inventorycfg = os.path.join(options['kubespray_path'], 'inventory/inventory.cfg')

    # Run ssh-agent and store identities
    sshagent = check_output('ssh-agent')
    ssh_envars = re.findall('\w*=[\w*-\/.*]*', sshagent)
    for v in ssh_envars:
        os.environ[v.split('=')[0]] = v.split('=')[1]
    proc = Popen('ssh-add', stdout=PIPE, stderr=STDOUT, stdin=PIPE, shell=True)
    proc.stdin.write('password\n')
    proc.stdin.flush()
    response_stdout, response_stderr = proc.communicate()
    display.display(response_stdout)
    if response_stderr:
        display.error(response_stderr)
    
    # Check SSH connections
    display.banner('CHECKING SSH CONNECTIONS')
    cmd = [os.path.join(options['ansible_path'], 'ansible'), '--ssh-extra-args', '-o StrictHostKeyChecking=no',
           '-u',  '%s' % options['ansible_user'], '-e', 'ansible_ssh_user=%s' % options['ansible_user'],
           '-b', '--become-user=root', '-m', 'ping','all',  '-i', inventorycfg]
    proc = Popen(cmd, stdout=PIPE, stderr=STDOUT, universal_newlines=True, shell=False)
    with proc.stdout:
        for line in iter(proc.stdout.readline, b''):
             print line,
    proc.wait()
    if proc.returncode != 0:
        display.error('Some of your hosts from the inventory %s are not reachable' % inventorycfg)
        sys.exit(1)
    else:
        display.display('All hosts are reachable', color='green')

    # Run Kubespray playbook
    display.banner('RUN PLAYBOOK')
    cmd = [os.path.join(options['ansible_path'], 'ansible-playbook'), '--ssh-extra-args', '-o StrictHostKeyChecking=no',
           '-e', 'kube_network_plugin=%s' % options['network_plugin'], '-u',  '%s' % options['ansible_user'], 
           '-e', 'ansible_ssh_user=%s' % options['ansible_user'], '-b', '--become-user=root', '-i', inventorycfg, 
           os.path.join(options['kubespray_path'], 'cluster.yml')]
    if 'ansible_opts' in options.keys():
        cmd = cmd + options['ansible_opts'].split(' ')
    display.display(' '.join(cmd), color='bright blue')
    proc = Popen(cmd, stdout=PIPE, stderr=STDOUT, universal_newlines=True, shell=False)
    with proc.stdout:
        for line in iter(proc.stdout.readline, b''):
             print line,
    proc.wait()
    if proc.returncode != 0:
        display.error('Cluster deployment failed')
        sys.exit(1)
#    
#            display.banner('WRITTING INVENTORY')
#            self.logger.info('the inventory %s was successfuly generated' % self.filename)
#            self.logger.debug('The following options were used to generate the inventory: %s' % self.options)
#            display.display('Inventory generated : %s' % self.filename, color='green')
