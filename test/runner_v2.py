#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   runner_v2.py    
@Contact :   shu_ke163@163.com
@Author  :   FengFeng zhao
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/12/31 16:09    1.0         None
"""

from loguru import logger
from pathlib import Path
import ansible_runner
from configparser import ConfigParser


# from conf.logger import ansible_logger


class AnsibleRunner():

    def __init__(self, host_pattern='', limit=None):
        self.data_dir = Path.cwd()
        self.inventory_path = '/inventory/hosts'
        self.host_pattern = host_pattern
        self.limit = limit

    def init_hosts(self):
        config = ConfigParser(allow_no_value=True)
        config.read(self.inventory_path)
        print(config.read(self.inventory_path))
        if not config.has_section(self.host_pattern):
            config.add_section(self.host_pattern)
        for host in self.limit.rstrip(',').split(','):
            if not config.has_option(self.host_pattern, host):
                config.set(self.host_pattern, host)

    def run_module(self, module, module_args=None, extravars=None):
        self.init_hosts()
        print(self.limit)
        r = ansible_runner.run(private_data_dir=self.data_dir,
                               host_pattern=self.host_pattern, module=module,
                               module_args=module_args, limit=self.limit, extravars=extravars, quiet=True)
        # print(r.status, r.rc, r.stdout, r.stderr)

        logger.info(f"执行完成！{self.host_pattern}, {module}, {module_args}, {self.limit}")
        result = self.parse_result(r)
        return result

    def parse_result(self, r):
        result = {}
        event_type_list = ['runner_on_ok', 'runner_on_failed',
                           'runner_on_unreachable', 'runner_on_skipped']
        logger.info(f"limit: {self.limit.rstrip(',').split(',')}")
        for host in self.limit.rstrip(',').split(','):
            host_event = list(filter(
                lambda x: x['event'] in event_type_list, r.host_events(host)))
            if host_event:
                result[host] = host_event

        print(result.keys())

        # event_res = host_event[0].get('event_data').get('res')
        # single_host_res = {}
        # if host_event[0].get('event') == 'runner_on_ok':
        #     single_host_res.update({'status': 'ok', 'data': event_res})
        # if host_event[0].get('event') == 'runner_on_failed':
        #     single_host_res.update({'status': 'failed', 'data': event_res})
        # if host_event[0].get('event') == 'runner_on_unreachable':
        #     single_host_res.update(
        #         {'status': 'unreachable', 'msg': '主机不可达'})
        # if host_event[0].get('event') == 'runner_on_skipped':
        #     single_host_res.update({'status': 'skipped', 'msg': '任务被忽略'})
        # result.update({host: single_host_res})
        return result


runner = AnsibleRunner('localhost, 192.168.18.227', limit='localhost, 192.168.18.227')
res = runner.run_module('setup', extravars={})
