### ansible dynamic inventory

### ansible-config

```shell
# example ansible.cfg 
$ ansible-config init --disabled > ansible.cfg
#include all plugin
$ ansible-config init --disabled -t all > ansible.cfg
# check ansible.cfg changed
ansible-config dump --only-changed -t all
```

### ansible-inventory

```shell
ansible-inventory  --list
ansible-inventory  --graph
ansible-inventory -i inventory/dynamic_inventory.py --list
```

### test

```shell
python /Users/apple/work/cmdb/inventory/dynamic_inventory.py
```