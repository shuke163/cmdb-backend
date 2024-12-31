#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   test.py
@Contact :   shu_ke163@163.com
@Author  :   FengFeng zhao
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/12/30 17:12    1.0         None
"""

import json
from loguru import logger

import ansible_runner

# get ansible inventory information
out, err = ansible_runner.get_inventory(
    action='list',
    inventories=['/Users/apple/work/cmdb/inventory/hosts', ],
    response_format='json',
    process_isolation=False,
    # container_image='network-ee'
)
logger.info("inventory: {}".format(out))
# logger.info("err: {}".format(err))

# r = ansible_runner.run(private_data_dir='/Users/apple/work/cmdb', playbook='test.yml')
# print("{}: {}".format(r.status, r.rc))
# # successful: 0
# for each_host_event in r.events:
#     print(each_host_event['event'])
# print("Final status:")
# print(r.stats)

# print(dir(ansible_runner))
#
# print(r.get_fact_cache("localhost"))

hosts = "localhost"
r = ansible_runner.run(private_data_dir='/', host_pattern=hosts, module='ping')
# print("{}: {}".format(r.status, r.rc))
#
# for each_host_event in r.events:
#     print(each_host_event['event'])
# print("Final status:")
# print(r.stats)

if r.status == "successful" and r.rc == 0:
    data = json.dumps(r.get_fact_cache(hosts), indent=4)
    logger.info(f"{hosts}: {data}")
