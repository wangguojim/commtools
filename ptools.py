# !/usr/bin/env python
# coding=utf-8

# import os
# import sys
import json
import json5
from argparse import ArgumentParser, REMAINDER
import subprocess
import collections
import socket
import os
import datetime
import sys


def get_parse_args():
    """
    parser support two kinds of arument input:
    1) type of json file
    2) --varname varvalue
    """

    parser = ArgumentParser(
        description="FlashTransformers runner to help launch distributed "
                    "multi-node/multi-gpu training jobs.")

    parser.add_argument("-o",
                        "--operation",
                        default='kill',
                        choices=['kill','ls'],
                        type=str,
                        help="(optional) choose launcher backend for multi-node "
                             "training.")

    parser.add_argument("-H",
                        "--hostfile",
                        type=str,
                        default='./hostfile',
                        help="Hostfile path (in MPI style) that defines the"
                             "resource pool available to the job (e.g.,host1 slots=4),"
                             "one can leave it unset if only one node is used")

    parser.add_argument("-I",
                        "--input",
                        type=str,
                        default='',
                        help="input for operation"
                             "e.g. 'pretrain' for operation 'kill' means kill all "
                             "processes which contain 'pretrain'" )


    parser.add_argument("-e",
                        "--executable",
                        default='/opt/conda/bin/python',
                        type=str,
                        help="The path of executable python, e.g. /opt/conda/bin/python")


    return parser.parse_args()


def fetch_hosts(args):
    resource_pool = collections.OrderedDict()
    if not os.path.isfile(args.hostfile):
        print("Unable to find hostfile and no hostnames are set, will proceed with training "
              "with local resources only.")
        return resource_pool

    else:
        if os.path.isfile(args.hostfile):
            with open(args.hostfile, 'r') as fd:
                for line in fd.readlines():
                    line = line.strip()
                    if line == '':
                        # skip empty lines
                        continue
                    try:
                        hostname, slots = line.split()
                        _, slot_count = slots.split("=")
                        slot_count = int(slot_count)
                    except ValueError as err:
                        raise err
                    if hostname in resource_pool:
                        raise ValueError(f"host {hostname} is already defined")

                    resource_pool[hostname] = slot_count
    return resource_pool


def main():
    args = get_parse_args()
    resource_pool = fetch_hosts(args)
    print('hosts:',list(resource_pool.keys()))


    cmd = "which python"
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read().splitlines()
    python_path =str(out[0], encoding='utf-8')
    for host, slots in resource_pool.items():
        cmd_launch = ['pdsh',
                      '-f', '1024',
                      '-w']
        cmd_launch.append('ssh:' + host)

        if args.operation=='kill':
            cmd_launch.append('"')
            cmd_launch.append(python_path)
            cmd_launch.append('/data/ptools/src/kill_process.py')
            cmd_launch.append('--input')
            cmd_launch.append(args.input)
            cmd_launch.append('"')
        elif args.operation=='ls':
            cmd_launch.append('"')
            cmd_launch.append('ls')
            cmd_launch.append(args.input)
            cmd_launch.append('"')
        else:
            pass


        run_cmd = ' '.join(cmd_launch)
        print(run_cmd)
        subprocess.Popen(run_cmd, shell=True)

if __name__ == '__main__':
    main()



