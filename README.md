# Kubespray wrapper
This tools helps to deploy a kubernetes cluster with ansible.
It must support all ansible parameters.


## Config file
A config file can be updated (yaml).
This file contains default values for some parameters that doesn't change frequently
```
inventory_path: "/usr/lib/kubespray/ansible/inventory"
logfile: "/var/log/kubespray.log"
loglevel: "info"

aws_access_key: "mykey"
aws_secret_key: "mykey"

gce_sshkey_path: "/home/foo/.ssh/id_rsa"

```
## Basic usage

### Generate inventory
The following options are mandatory

On **baremetal**
```
<<<<<<< HEAD
kubespray generate --masters <master1> <master2> --nodes <node1> <node2>
```


On cloud providers create vms and generate the inventory
**AWS** 
```
kubespray aws --masters 2 --nodes 3 --ami <myami> --type <aws_instance_type> \
[ --aws_access_key <access_key> --aws_secret_key <secret_key> ]
```
**GCE**
```
kubespray gce --masters 2 --nodes 3 --image <gce_image> --type=<aws_machine_type> --zone=<gce_zone> \
[--sshkey <keypath>]
```

### Deploy cluster

```
kubespray deploy [--network-plugin <net_plugin>] [--aws|--gce] [--upgrade] [--ansible_opts]
```
default network plugin : flannel (vxlan)

### Infos
```
kubespray cluster-info
```
- binaries version
- latest deployment date
- who deployed the cluster
- network plugin
- etcd cluster health
