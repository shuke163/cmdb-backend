#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   runner_api.py
@Contact :   shu_ke163@163.com
@Author  :   FengFeng zhao
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/12/30 17:12    1.0         None
"""

import json
from pathlib import Path
from loguru import logger

import ansible_runner

# print(dir(ansible_runner))

# get ansible inventory information
# out, err = ansible_runner.get_inventory(
#     action='list',
#     inventories=['/Users/apple/work/cmdb/inventory/hosts.yml', ],
#     response_format='json',
#     process_isolation=False,
#     # container_image='network-ee'
# )
# logger.info("inventory: {}".format(out))
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

hosts = "192.168.0.107"

# r = ansible_runner.run(private_data_dir=Path.cwd(), host_pattern="/Users/apple/work/cmdb/inventory/hosts.yml")

for host in hosts.split(","):
    print("host={}".format(str(host).strip()))
    r = ansible_runner.run(private_data_dir=Path.cwd(),
                           host_pattern=str(host).strip(),
                           limit=",".join(["localhost", "127.0.0.1", "mac", "192.168.0.107"]),
                           module='setup', quiet=True, json_mode=True)
    #
    for each_host_event in r.events:
        print(each_host_event['event'])

    print("Final status:")
    print(r.stats)

    if r.status == "successful" and r.rc == 0:
        if r.stats.get("ok"):
            data = json.dumps(r.get_fact_cache(str(host).strip()), indent=4)
            logger.info(f"{host}: {data}")

# print(dir(r))

# print("stdout: ", r.stdout.readlines())
# print(r.stderr.readlines())
# print(r.get_fact_cache("192.168.0.109"))


# print(dir(r))
# print(dir(r.config))
# print(r.config.fact_cache)
# print(r.config.host_pattern)
# print(r.config.limit)
