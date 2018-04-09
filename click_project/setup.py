#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import print_function, absolute_import

from click_project.flow import setup as setup_flow
from click_project.triggers import setup as setup_triggers
from click_project.overloads import CoreCommandResolver, MainCommand, entry_point
from click_project.scriptcommands import ScriptCommandResolver
from click_project.externalcommands import ExternalCommandResolver
from click_project.alias import DottedAliasResolver, AliasCommandResolver, AliasToGroupResolver
from click_project.hook import HookCommandResolver, setup as setup_hook
from click_project.overloads import Group, GroupCommandResolver
from click_project.completion import init as completion_init
from click_project.config import setup_config_class, Config
from click_project.log import get_logger, basic_config
from click_project import lib
from click_project.core import main  # NOQA: F401

LOGGER = get_logger(__name__)


def classic_setup(main_module=None, config_cls=Config, extra_command_packages=[]):
    lib.main_module = main_module
    completion_init()
    setup_config_class(config_cls)
    setup_triggers()
    setup_flow()
    setup_hook()
    for package in extra_command_packages:
        basic_config(package)
    CoreCommandResolver.commands_packages = extra_command_packages + ["click_project.commands"]
    Group.commandresolvers = [
        ScriptCommandResolver(),
        ExternalCommandResolver(),
        AliasCommandResolver(),
        HookCommandResolver(),
        GroupCommandResolver(),
        DottedAliasResolver(),
        AliasToGroupResolver(),
    ]
    MainCommand.commandresolvers = [
        ScriptCommandResolver(),
        ExternalCommandResolver(),
        AliasCommandResolver(),
        HookCommandResolver(),
        CoreCommandResolver(),
        DottedAliasResolver(),
    ]

    def decorator(command):
        config_cls.main_command = command
        return command
    return decorator


def basic_entry_point(main_module, extra_command_packages=[]):
    def decorator(f):
        return classic_setup(main_module, extra_command_packages=extra_command_packages)(entry_point()(f))
    return decorator