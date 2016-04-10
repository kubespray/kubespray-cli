Kargo wrapper
=============

This tool helps to deploy a kubernetes cluster with ansible.

**Note**: The following choices are done automatically for redundancy.
According to the number of nodes on your cluster:

-   The 2 firsts nodes will have master components installed
-   The 3 firsts nodes will be members of the etcd cluster

You should have at least 3 nodes but you can spawn only one instance for
tests purposes.

Example on GCE:
[![asciicast](https://asciinema.org/a/38yu9fh7r2lq2hd4xlvtngadp.png)](https://asciinema.org/a/38yu9fh7r2lq2hd4xlvtngadp?speed=4)

Requirements
============

-   **Ansible v2.x**
-   The current user must have its ssh **public key** installed on the
    remote servers.
-   The remote user (option --user) must be in the sudoers with no
    password

Installation
============

### Python pip

    pip2 install kargo


### Docker image
Alternatively you can use the docker image `k8s-kargocli` as follows:

    docker run -it -v /home/smana/kargoconf:/etc/kargo quay.io/smana/k8s-kargocli:latest /bin/bash

The mounted directory contains kargo's configuration as well as keys

Config file
-----------

A config file can be updated (yaml). (default: */etc/kargo/kargo.yml* ) </br>
This file contains default values for some parameters that don't change
frequently </br>
**Note** these values are **overwritten** by the command line.


    # Common options
    # ---------------
    # Path where the kargo ansible playbooks will be installed
    # Defaults to current user's home directory if not set
    # kargo_path: "/tmp"
    # Default inventory path
    kargo_git_repo: "https://github.com/kubespray/kargo.git"
    # Logging options
    loglevel: "info"
    #
    # Google Compute Engine options
    # ---------
    machine_type: "n1-standard-1"
    image: "debian-8-kubespray"
    service_account_email: "kubespray-ci-1@appspot.gserviceaccount.com"
    pem_file: "/home/smana/kargo.pem"
    project_id: "kubespray-ci-1"
    zone: "us-east1-c"
    ...

Basic usage
-----------

### Generate inventory for a baremetal cluster

On **baremetal**

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

The command below will just clone the git repository and creates the
inventory.
The hostvars must be separated by a **comma without spaces**

    kargo preprare --nodes node1[ansible_ssh_host=10.99.21.1] node2[ansible_ssh_host=10.99.21.2] node3[ansible_ssh_host=10.99.21.3]

### Run instances and generate the inventory on Clouds

**AWS**

    usage: kargo aws [-h] [-p KARGO_PATH] [--config CONFIGFILE] [-y]
                     [-i INVENTORY_PATH] [--access-key AWS_ACCESS_KEY]
                     [--secret-key AWS_SECRET_KEY] [--type INSTANCE_TYPE]
                     [--keypair KEY_NAME] [--region REGION]
                     [--security-group GROUP] [--vpc-id AWS_VPC_ID]
                     [--vpc-subnet VPC_SUBNET_ID] [--ami AWS_AMI]
                     [--cluster-name CLUSTER_NAME] [--add] --instances COUNT
    
    optional arguments:
      -h, --help            show this help message and exit
      -p KARGO_PATH, --path KARGO_PATH
                            Where the Ansible playbooks are installed
      --config CONFIGFILE   Config file
      -y, --assumeyes       When a yes/no prompt would be presented, assume that
                            the user entered "yes"
      -i INVENTORY_PATH, --inventory INVENTORY_PATH
                            Ansible SSH user (remote user)
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
      --cluster-name CLUSTER_NAME
                            Name of the cluster
      --add                 Add node to an existing cluster
      --instances COUNT     Number of nodes

if the config file is filled with the proper information you just need to run the following command

    kargo aws --instances 3

**GCE** 

    usage: kargo gce [-h] [-p KARGO_PATH] [--config CONFIGFILE] [-y]
                     [-i INVENTORY_PATH] [--pem_file PEM_FILE] [--zone ZONE]
                     [--type MACHINE_TYPE] [--image IMAGE] [--project PROJECT_ID]
                     [--email SERVICE_ACCOUNT_EMAIL] [--cluster-name CLUSTER_NAME]
                     [--add] --instances COUNT
    
    optional arguments:
      -h, --help            show this help message and exit
      -p KARGO_PATH, --path KARGO_PATH
                            Where the Ansible playbooks are installed
      --config CONFIGFILE   Config file
      -y, --assumeyes       When a yes/no prompt would be presented, assume that
                            the user entered "yes"
      -i INVENTORY_PATH, --inventory INVENTORY_PATH
                            Ansible SSH user (remote user)
      --pem_file PEM_FILE   GCE ssh pem file path
      --zone ZONE           GCE zone
      --type MACHINE_TYPE   GCE machine type
      --image IMAGE         GCE image
      --project PROJECT_ID  GCE project ID
      --email SERVICE_ACCOUNT_EMAIL
                            GCE project ID
      --cluster-name CLUSTER_NAME
                            Name of the cluster
      --add                 Add node to an existing cluster
      --instances COUNT     Number of nodes

example:

if the config file is filled with the proper information you just need to run the following command

    kargo gce --instances 3

**Add a node to an existing cluster**
It's possible to add nodes to a running cluster, </br>
these newly added nodes will act as node only (no etcd, no master components)

Add a node

    kargo [aws|gce] --add --instances 1

Then deploy the cluster with the same options as the running cluster.


### Deploy cluster


    usage: kargo deploy [-h] [-p KARGO_PATH] [--config CONFIGFILE] [-y]
                        [-i INVENTORY_PATH] [-k SSH_KEY] [-u ANSIBLE_USER]
                        [-n {flannel,weave,calico}] [--aws] [--gce] [--coreos]
                        [--ansible-opts ANSIBLE_OPTS]
    
    optional arguments:
      -h, --help            show this help message and exit
      -p KARGO_PATH, --path KARGO_PATH
                            Where the Ansible playbooks are installed
      --config CONFIGFILE   Config file
      -y, --assumeyes       When a yes/no prompt would be presented, assume that
                            the user entered "yes"
      -i INVENTORY_PATH, --inventory INVENTORY_PATH
                            Ansible SSH user (remote user)
      -k SSH_KEY, --sshkey SSH_KEY
                            ssh key for authentication on remote servers
      -u ANSIBLE_USER, --user ANSIBLE_USER
                            Ansible SSH user (remote user)
      -n {flannel,weave,calico}, --network-plugin {flannel,weave,calico}
      --aws                 Kubernetes deployment on AWS
      --gce                 Kubernetes deployment on GCE
      --coreos              bootstrap python on CoreOS
      --ansible-opts ANSIBLE_OPTS
                            Ansible options

-   default network plugin : flannel (vxlan) default
-   default kargo\_path : "/home/\<current\_user\>/kargo"
-   inventory path : "\<kargo\_path\>/inventory/inventory.cfg".
-   The option `--inventory` allows to use an existing inventory (file or dynamic)
-   On coreos (--coreos) the directory **/opt/bin** must be writable

- You can use all Ansible's variables with
`--ansible-opts '-e foo=bar -e titi=toto -vvv'`
**Note** : the value must be enclosed by simple quotes

example: Deploy a kubernetes cluster on CoreOS servers located on GCE

    kargo deploy -u core -p /kargo-dc1 --gce --coreos
