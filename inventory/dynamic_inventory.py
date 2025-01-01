#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   dynamic_inventory.py
@Contact :   shu_ke163@163.com
@Author  :   fengfeng Zhao
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/12/31 09:16    1.0         None
"""
import json

import sqlite3
from pathlib import Path
from loguru import logger

# docs: https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html
"""
example:
# ansible-inventory -i inventory/hosts.yml --list
{
    "_meta": {
        "hostvars": {
            "192.168.18.227": {
                "ansible_ssh_private_key_file": "~/.ssh/id_rsa.pub"
            },
            "localhost": {
                "ansible_host": "127.0.0.1",
                "ansible_password": "aslongas",
                "ansible_user": "root"
            }
        }
    },
    "all": {
        "children": [
            "ungrouped",
            "dev",
            "prod",
            "test"
        ]
    },
    "dev": {
        "hosts": [
            "localhost",
            "192.168.18.227"
        ]
    },
    "prod": {
        "hosts": [
            "foo.example.com"
        ]
    },
    "test": {
        "hosts": [
            "bar.example.com"
        ]
    }
}
"""

base_path = Path(__file__).parent.parent
logger.info(f"base_path: {base_path}")

struct = {
    "_meta": {
        "hostvars": {
        }
    },
    "all": {
        "children": [
            "ungrouped",
        ]
    },
    "ungrouped": {
        "hosts": []
    }
}

conn = sqlite3.connect(Path(base_path, "db.sqlite3"))
conn.row_factory = sqlite3.Row
c = conn.cursor()
# ret = c.execute(
#     "SELECT id, alias, ansible_host, ansible_password, ansible_user, ansible_ssh_private_key_file  from ansible_inventory").fetchall()

ret = c.execute("SELECT * from ansible_inventory").fetchall()

for row in ret:
    # print(dict(row))
    struct["_meta"]["hostvars"][str(row["alias"])] = dict(row)
    struct["ungrouped"]["hosts"].append(str(row["alias"]))

c.close()
conn.close()

logger.info(json.dumps(struct, indent=4, separators=(',', ':')))
