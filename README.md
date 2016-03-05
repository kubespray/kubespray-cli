# Kubespray wrapper

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
kubespray generate --masters=<master1>,<master2> --nodes=<node1>,<node2>
```


On cloud providers create vms and generate the inventory
**AWS** 
```
kubespray aws --masters=2 --nodes=3 --ami=<myami> --type=<aws_instance_type>
```
**GCE**
```
kubespray gce --masters=2 --nodes=3 --ami=<myami> --type=<aws_machine_type> --zone=<gce_zone>
```

### Deploy cluster

```
kubespray deploy [--aws|--gce] [--upgrade]
```

### Infos
```
kubespray cluster-info
```
- binaries version
- latest deployment date
- who deployed the cluster
- network plugin
- etcd cluster health
