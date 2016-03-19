Kubespray wrapper
=================

This tools helps to deploy a kubernetes cluster with ansible. It must
support all ansible parameters.

Config file
-----------

A config file can be updated (yaml). (default:
*/etc/kubespray/kubespray.yml* ) This file contains default values for
some parameters that doesn't change frequently

::

    inventory_path: "/usr/lib/kubespray/ansible/inventory"
    loglevel: "info"

    aws_access_key: "mykey"
    aws_secret_key: "mykey"

    gce_sshkey_path: "/home/foo/.ssh/id_rsa"

Basic usage
-----------

Generate inventory
~~~~~~~~~~~~~~~~~~

The following options are mandatory

On **baremetal**

::

    kubespray preprare --nodes node1[ansible_ssh_host=10.99.21.1] node2[ansible_ssh_host=10.99.21.2] node3[ansible_ssh_host=10.99.21.3] \
                       --masters node1 node2 \

On cloud providers create vms and generate the inventory **AWS**

::

    kubespray aws --instances 3 --ami <myami> --type <aws_instance_type> \
    [ --aws_access_key <access_key> --aws_secret_key <secret_key> ] [--coreos]

**GCE**

::

    kubespray gce --instances 3 --image <gce_image> --type=<aws_machine_type> --zone=<gce_zone> \
    [--sshkey <keypath>] [--coreos]

Deploy cluster
~~~~~~~~~~~~~~

::

    kubespray deploy [-n|--network-plugin <net_plugin>] [--aws|--gce] [--upgrade] [--ansible_opts] [-i|--inventory <inventory>] [-u|--user <ssh_user>]

- default network plugin : flannel (vxlan) default
- inventory path : "home/<current_user/kubespray/inventory.cfg".
- The option ``--inventory`` allows to use an existing inventory (file or dynamic)
- You can use all Ansible's variables with
``--ansible_opts '-e foo=bar -e titi=toto -vvv'``
**Note** : the value must be enclosed by simple quotes
- option ``--user`` : if the user (default value: current user) is not root the following options are passed to ansible
``-u <user> -e ansible_ssh_user=<user> -b --become-user=root``

Infos
~~~~~

::

    kubespray cluster-info

-  binaries version
-  latest deployment date
-  who deployed the cluster
-  network plugin
-  etcd cluster health
