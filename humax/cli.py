#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import yaml
import os
import sys

from configparser import ConfigParser

from pygments import highlight
from pygments.lexers import JsonLexer, YamlLexer
from pygments.formatters import Terminal256Formatter
from xdg.BaseDirectory import xdg_config_home

from .humax import Humax, ALL_METHODS, Basic, Advanced
from .__version__ import __version__


filename = 'humax.conf'
CONFIG_PATH = os.path.join(xdg_config_home, filename)


def colorprint(json_object, yaml=False, color='auto'):
    if color == 'auto':
        color = sys.stdout.isatty()

    if yaml:
        lexer = YamlLexer()
        str_rep = yaml.dump(json_object)
    else:
        lexer = JsonLexer()
        str_rep = json.dumps(json_object, indent=4, sort_keys=True)

    if not color:
        print(str_rep)
        return

    formatter = Terminal256Formatter(style='monokai')
    print(highlight(str_rep, lexer, formatter))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Program to interact with Humax router")
    parser.add_argument('-V', '--version', action='store_true',
                        help='Display program version.')
    subparsers = parser.add_subparsers(
        dest='action', help='Action to perform')

    parser_post = subparsers.add_parser(
        'post', help="Make a POST request to /api")
    parser_post.add_argument(
        'method', help='Method field of the posted json. Use the '
                       '\'list-methods\' action to list available methods.')

    subparsers.add_parser('list-methods', help="List available methods.")
    subparsers.add_parser('config-path', help="Print config file path.")
    subparsers.add_parser('ip', help="Display WAN IP.")
    subparsers.add_parser('get-port-forwarding',
                          help="Display port forwarding rules.")

    parser.add_argument('-r', '--router', help="Specify the section in config "
                                               "file to use. Defaults to 'DEFAULT'.",
                        default="DEFAULT")

    return parser.parse_args()


def get_config(section="DEFAULT"):
    cfg = ConfigParser()

    try:
        with open(CONFIG_PATH, 'r') as fp:
            cfg.readfp(fp)
        return cfg[section]
    except OSError:
        print(f'Expected credetials file at {CONFIG_PATH} with contents')
        print('[DEFAULT]')
        print("url=http://192.168.0.1")
        print("username=USERNAME")
        print("password=PASSWORD")
        sys.exit(1)


def get_port_forwarding(humax):
    strformat = '''{description}:
    {external_ip}:{external_port} -> {local_ip}:{local_port}
    protocol: {protocol}
    {enabled}
    '''
    output = humax.posttoken(Advanced.getForwarding)

    for rule in output['forwarding']:
        enabled = 'ENABLED' if rule['enable'] else 'DISABLED'

        external_ip = '*' if rule['external_ip'] == '0.0.0.0' else rule['external_ip']

        external_port = str(rule['external_start_port']) + '-' \
            + str(rule['external_end_port'])
        if rule['external_start_port'] == rule['external_end_port']:
            external_port = rule['external_start_port']
        local_port = str(rule['local_start_port']) + '-' \
            + str(rule['local_end_port'])
        if rule['local_start_port'] == rule['local_end_port']:
            local_port = rule['local_start_port']

        rule.update(
            external_ip=external_ip,
            external_port=external_port,
            local_port=local_port,
            enabled=enabled,
        )

        rule_line = strformat.format(**rule)
        print(rule_line)


def main():
    args = parse_arguments()

    if args.version:
        print(__version__)
        sys.exit(0)

    config = get_config(section=args.router)
    url, user, password = config['url'], config['username'], config['password']

    h = Humax(url)
    h.login(user, password)

    if args.action == 'post':
        output = h.posttoken(args.method)
        colorprint(output)
    elif args.action == 'list-methods':
        for method in ALL_METHODS:
            print(method)
    elif args.action == 'get-config-path':
        print(CONFIG_PATH)
    elif args.action == 'ip':
        output = h.posttoken(Basic.getStatus)
        print(output['wan_ip'])
    elif args.action == 'get-port-forwarding':
        get_port_forwarding(h)
    else:
        print('No action specified')
        sys.exit(1)


if __name__ == '__main__':
    main()
