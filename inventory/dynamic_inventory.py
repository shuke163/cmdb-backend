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

class DynamicInventory:
    """
    dynamic inventory
    """

    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.db_path = Path(self.base_path, "db.sqlite3")
        self.data = self.load_inventory()
        print(self.data)

    def _empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    # dynamic inventory for db.sqlite3
    def load_inventory(self):
        """
        Example of a method for creating an inventory return Json.
        :return: Json with the inventory.
        :rtype: json.
        """
        inventory_struct = dict()
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        ret = c.execute("SELECT * from ansible_inventory").fetchall()

        for row in ret:
            # print(dict(row))
            inventory_struct.setdefault("_meta", {}).setdefault("hostvars", {}).setdefault(str(row["alias"]), dict(row))
            inventory_struct.setdefault(row["group"], {}).setdefault("hosts", []).append(str(row["alias"]))
            inventory_struct.setdefault("all", {}).setdefault("children", []).append(row["group"])

            # if row["group"] == "dev" or row["group"] == "test" or row["group"] == "prod":
            #     inventory_struct[row["group"]]["hosts"].append(str(row["alias"]))

        group = c.execute('SELECT "group" from ansible_inventory').fetchall()
        for row in group:
            inventory_struct["all"]["children"].append(row["group"])

        # tag/去重
        inventory_struct["all"]["children"] = list(set(inventory_struct["all"]["children"]))
        inventory_struct["ungrouped"]["hosts"] = list(set(inventory_struct["ungrouped"]["hosts"]))

        c.close()
        conn.close()

        data = json.dumps(inventory_struct, indent=4, separators=(',', ':'))
        # logger.debug(f"dynamic inventory: {data}")
        return data


if __name__ == '__main__':
    try:
        DynamicInventory()
    except Exception as e:
        print(json.dumps({"_meta": {"hostvars": {}}}))
