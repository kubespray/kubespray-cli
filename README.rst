Kubespray wrapper
=================
This tools helps to deploy a kubernetes cluster with ansible. It must
support all ansible parameters.


Requirements
=================

* **Ansible v2.x**
* The current user must have its ssh **public key** installed on the remote servers.
* The current user must be in the sudoers



Installation
=================

::

    pip2 install kubespray


Config file
-----------

A config file can be updated (yaml). (default:
*/etc/kubespray/kubespray.yml* )
This file contains default values for
some parameters that doesn't change frequently
Note these values are overwritten by the command line

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

    kubespray prepare -h
    usage: kubespray prepare [-h] --nodes N [N ...] --masters N [N ...]
                             [-p KUBESPRAY_PATH]
    
    optional arguments:
      -h, --help            show this help message and exit
      --nodes N [N ...]     List of nodes
      --masters N [N ...]   List of masters
      -p KUBESPRAY_PATH, --path KUBESPRAY_PATH
                            Where the Ansible playbooks are installed

::

    kubespray preprare --nodes node1[ansible_ssh_host=10.99.21.1] node2[ansible_ssh_host=10.99.21.2] node3[ansible_ssh_host=10.99.21.3] \
                       --masters node1 node2 \

On cloud providers create vms and generate the inventory

**AWS**
**warn** : not implemented yet

::

    usage: kubespray aws [-h] [--access-key AWS_ACCESS_KEY]
                         [--secret-key AWS_SECRET_KEY] [--type AWS_INSTANCE_TYPE]
                         [--keypair AWS_KEYPAIR_NAME] [--region AWS_REGION]
                         [--security-group AWS_SECURITY_GROUP]
                         [--vpc-id AWS_VPC_ID] [--vpc-subnet AWS_VPC_SUBNET]
                         [--ami AWS_AMI] [--instances CLOUD_INSTANCES_COUNT]
                         [--masters CLOUD_MASTERS_COUNT]
    
    optional arguments:
      -h, --help            show this help message and exit
      --access-key AWS_ACCESS_KEY
                            AWS access key
      --secret-key AWS_SECRET_KEY
                            AWS secret key
      --type AWS_INSTANCE_TYPE
                            AWS instance type
      --keypair AWS_KEYPAIR_NAME
                            AWS key pair name
      --region AWS_REGION   AWS region
      --security-group AWS_SECURITY_GROUP
                            AWS security group
      --vpc-id AWS_VPC_ID   EC2 VPC id
      --vpc-subnet AWS_VPC_SUBNET
                            EC2 VPC regional subnet
      --ami AWS_AMI         AWS AMI
      --instances CLOUD_INSTANCES_COUNT
                            Number of nodes
      --masters CLOUD_MASTERS_COUNT
                            Number of masters
    

::

    kubespray aws --instances 3 --ami <myami> --type <aws_instance_type> \
    [ --aws_access_key <access_key> --aws_secret_key <secret_key> ] [--coreos]

**GCE**
**warn** : not implemented yet

example:

::

    kubespray gce --instances 3 --image <gce_image> --type=<aws_machine_type> --zone=<gce_zone> \
    [--sshkey <keypath>] [--coreos]

Deploy cluster
~~~~~~~~~~~~~~

example: Deploy a kubernetes cluster on CoreOS servers located on GCE

::

    kubespray deploy -n weave -p /tmp/kubespray --gce --coreos

::

    usage: kubespray deploy [-h] [-n {flannel,weave,calico}] [--aws] [--gce]
                            [--upgrade] [--coreos] [--non-interactive]
                            [-p KUBESPRAY_PATH] [--ansible_opts ANSIBLE_OPTS]
    
    optional arguments:
      -h, --help            show this help message and exit
      -n {flannel,weave,calico}, --network-plugin {flannel,weave,calico}
      --aws                 Kubernetes deployment on AWS
      --gce                 Kubernetes deployment on GCE
      --upgrade             Upgrade Kubernetes cluster
      --coreos              bootstrap python on CoreOS
      --non-interactive     Don't prompt user for input
      -p KUBESPRAY_PATH, --path KUBESPRAY_PATH
                            Where the Ansible playbooks are installed
      --ansible_opts ANSIBLE_OPTS
                            Ansible options


- default network plugin : flannel (vxlan) default
- inventory path : "home/<current_user/kubespray/inventory.cfg".
- The option ``--inventory`` allows to use an existing inventory (file or dynamic)
- You can use all Ansible's variables with
``--ansible_opts '-e foo=bar -e titi=toto -vvv'``
**Note** : the value must be enclosed by simple quotes

Infos
~~~~~
**warn** : not implemented yet

::

    kubespray cluster-info

-  binaries version
-  latest deployment date
-  who deployed the cluster
-  network plugin
-  etcd cluster health
