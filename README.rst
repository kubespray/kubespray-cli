Kargo wrapper
=================
This tool helps to deploy a kubernetes cluster with ansible.


**Note**: The following choices are done automatically for redundancy.
According to the number of nodes on your cluster:

* The 2 firsts nodes will have master components installed
* The 3 firsts nodes will be members of the etcd cluster

You should have at least 3 nodes but you can spawn only one instance for tests purposes.


Requirements
=================

* **Ansible v2.x**
* The current user must have its ssh **public key** installed on the remote servers.
* The remote user (option --user) must be in the sudoers with no password



Installation
=================

::

    pip2 install kargo


Config file
-----------

A config file can be updated (yaml). (default:
*/etc/kargo/kargo.yml* )
This file contains default values for
some parameters that don't change frequently
Note these values are overwritten by the command line

::

    inventory_path: "/usr/lib/kargo/ansible/inventory"
    loglevel: "info"
    aws_access_key: "<aws_key>"
    aws_secret_key: "<aws_secret_key>"
    key_name: "<aws_keypair_name>"
    image: "<aws_ami>"
    instance_type: "<aws_instance_type>"
    group: "<aws_security_group>"
    vpc_subnet_id: "<aws_vpc_id>"
    region: "<aws_region>"

    gce_sshkey_path: "/home/foo/.ssh/id_rsa"
    ...

Basic usage
-----------

Generate inventory for a baremetal cluster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following options are mandatory

On **baremetal**

::

    usage: kargo prepare [-h] [-p KARGO_PATH] [--config CONFIGFILE] [--version]
                         [-y] --nodes N [N ...]
    
    optional arguments:
      -h, --help            show this help message and exit
      -p KARGO_PATH, --path KARGO_PATH
                            Where the Ansible playbooks are installed
      --config CONFIGFILE   Config file
      --version             show program's version number and exit
      -y, --assumeyes       When a yes/no prompt would be presented, assume that
                            the user entered "yes"
      --nodes N [N ...]     List of nodes


The command below will just clone the git repository and creates the inventory
The hostvars must be separated by a **comma without spaces**

::

    kargo preprare --nodes node1[ansible_ssh_host=10.99.21.1] node2[ansible_ssh_host=10.99.21.2] node3[ansible_ssh_host=10.99.21.3]



Run instances and generate the inventory on Clouds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**AWS**


::

    usage: kargo aws [-h] [-p KARGO_PATH] [--config CONFIGFILE] [--version] [-y]
                     [--access-key AWS_ACCESS_KEY] [--secret-key AWS_SECRET_KEY]
                     [--type INSTANCE_TYPE] [--keypair KEY_NAME] [--region REGION]
                     [--security-group GROUP] [--vpc-id AWS_VPC_ID]
                     [--vpc-subnet VPC_SUBNET_ID] [--ami AWS_AMI] --instances
                     COUNT
    
    optional arguments:
      -h, --help            show this help message and exit
      -p KARGO_PATH, --path KARGO_PATH
                            Where the Ansible playbooks are installed
      --config CONFIGFILE   Config file
      --version             show program's version number and exit
      -y, --assumeyes       When a yes/no prompt would be presented, assume that
                            the user entered "yes"
      --access-key AWS_ACCESS_KEY
                            AWS access key
      --secret-key AWS_SECRET_KEY
                            AWS secret key
      --type INSTANCE_TYPE  AWS instance type
      --keypair KEY_NAME    AWS key pair name
      --region REGION       AWS region
      --security-group GROUP
                            AWS security group
      --vpc-id AWS_VPC_ID   EC2 VPC id
      --vpc-subnet VPC_SUBNET_ID
                            EC2 VPC regional subnet
      --ami AWS_AMI         AWS AMI
      --instances COUNT     Number of nodes

if the config file is filled with the proper information you just need to run the following command


::

    kargo aws --instances 3 [--coreos]


**GCE**
**warn** : not implemented yet

example:


::

    kargo gce --instances 3 --image <gce_image> --type=<aws_machine_type> --zone=<gce_zone> \
    [--sshkey <keypath>] [--coreos]


Deploy cluster
~~~~~~~~~~~~~~

example: Deploy a kubernetes cluster on CoreOS servers located on GCE


::

    kargo deploy -u core -p /kargo-dc1 --gce --coreos


::

    usage: kargo deploy [-h] [-p KARGO_PATH] [--config CONFIGFILE] [--version]
                        [-y] [-u ANSIBLE_USER] [-n {flannel,weave,calico}] [--aws]
                        [--gce] [--upgrade] [--coreos]
                        [--ansible_opts ANSIBLE_OPTS]
    
    optional arguments:
      -h, --help            show this help message and exit
      -p KARGO_PATH, --path KARGO_PATH
                            Where the Ansible playbooks are installed
      --config CONFIGFILE   Config file
      --version             show program's version number and exit
      -y, --assumeyes       When a yes/no prompt would be presented, assume that
                            the user entered "yes"
      -u ANSIBLE_USER, --user ANSIBLE_USER
                            Ansible SSH user (remote user)
      -n {flannel,weave,calico}, --network-plugin {flannel,weave,calico}
      --aws                 Kubernetes deployment on AWS
      --gce                 Kubernetes deployment on GCE
      --upgrade             Upgrade Kubernetes cluster
      --coreos              bootstrap python on CoreOS
      --ansible_opts ANSIBLE_OPTS
                            Ansible options


- default network plugin : flannel (vxlan) default
- default kargo_path : "/home/<current_user>/kargo"
- inventory path : "<kargo_path>/inventory/inventory.cfg".
- The option ``--inventory`` allows to use an existing inventory (file or dynamic)
- You can use all Ansible's variables with
``--ansible_opts '-e foo=bar -e titi=toto -vvv'``
**Note** : the value must be enclosed by simple quotes
