#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   ansible_api.py
@Contact :   shu_ke163@163.com
@Author  :   FengFeng zhao
@Modify Time      @Version    @Desciption
------------      --------    -----------
2024/12/31 09:16    1.0         None
"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import shutil
from loguru import logger
import ansible.constants as C
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.plugins.loader import init_plugin_loader
from ansible.vars.manager import VariableManager
from ansible import context


# Create a callback plugin so we can capture the output
class ResultsCollectorJSONCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in.

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin.
    """

    def __init__(self, *args, **kwargs):
        super(ResultsCollectorJSONCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        host = result._host
        self.host_unreachable[host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        """Print a json representation of the result.

        Also, store the result in an instance attribute for retrieval later
        """
        host = result._host
        self.host_ok[host.get_name()] = result
        # print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_failed(self, result, *args, **kwargs):
        host = result._host
        self.host_failed[host.get_name()] = result

    def v2_runner_on_skipped(self):
        pass


def main():
    init_plugin_loader()
    host_list = ['localhost', "192.168.18.227"]
    # since the API is constructed for CLI it expects certain options to always be set in the context object
    context.CLIARGS = ImmutableDict(
        connection='smart',
        module_path=['/Users/apple/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules'], forks=10,
        become=None,
        become_method=None, become_user=None, check=False, diff=False, verbosity=0)
    # required for
    # https://github.com/ansible/ansible/blob/devel/lib/ansible/inventory/manager.py#L204
    sources = ','.join(host_list)
    if len(host_list) == 1:
        sources += ','

    logger.info(f"sources: {sources}")
    # initialize needed objects
    loader = DataLoader()  # Takes care of finding and reading yaml, json and ini files
    passwords = dict(vault_pass='secret')

    # Instantiate our ResultsCollectorJSONCallback for handling results as they come in. Ansible expects this to be one of its main display outlets
    results_callback = ResultsCollectorJSONCallback()

    # create inventory, use path to host config file as source or hosts in a comma separated string
    inventory = InventoryManager(loader=loader, sources=sources)
    # print(inventory.hosts, inventory.list_hosts(), inventory.list_groups(), inventory.groups, inventory.localhost)

    # variable manager takes care of merging all the different sources to give you a unified view of variables available in each context
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    # instantiate task queue manager, which takes care of forking and setting up all objects to iterate over host list and tasks
    # IMPORTANT: This also adds library dirs paths to the module loader
    # IMPORTANT: and so it must be initialized before calling `Play.load()`.
    tqm = TaskQueueManager(
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        passwords=passwords,
        stdout_callback=results_callback,
        # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
    )

    # create data structure that represents our play, including tasks, this is basically what our YAML loader does internally.
    play_source = dict(
        name="Ansible Play",
        hosts=host_list,
        gather_facts='no',
        tasks=[
            # dict(action=dict(module='ping')),
            dict(action=dict(module='setup')),
        ]
    )

    # Create play object, playbook objects use .load instead of init or new methods,
    # this will also automatically create the task objects from the info provided in play_source
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    # Actually run it
    try:
        result = tqm.run(play)  # most interesting data for a play is actually sent to the callback's methods
    finally:
        # we always need to cleanup child procs and the structures we use to communicate with them
        tqm.cleanup()
        if loader:
            loader.cleanup_all_tmp_files()

    # Remove ansible tmpdir
    shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    for host, result in results_callback.host_ok.items():
        logger.debug(f"host: {host}")
        print('{0} >>> {1}'.format(host, result._result['ansible_facts']))

    for host, result in results_callback.host_failed.items():
        logger.debug(f"host: {host}")
        print('{0} >>> {1}'.format(host, result._result['msg']))
        # print('{0} >>> {1}: {2}'.format(host, result._result['msg'], result._result['exception']))

    for host, result in results_callback.host_unreachable.items():
        logger.debug(f"host: {host}")
        print('{0} >>> {1}'.format(host, result._result['msg']))


if __name__ == '__main__':
    main()
