#!/usr/bin/python
import subprocess
import sys
import logging
import os,signal
from argparse import ArgumentParser, REMAINDER




def get_parse_args():
    """
    parser support two kinds of arument input:
    1) type of json file
    2) --varname varvalue
    """

    parser = ArgumentParser(
        description="FlashTransformers runner to help launch distributed "
                    "multi-node/multi-gpu training jobs.")



    parser.add_argument("-I",
                        "--input",
                        type=str,
                        default='',
                        help="input for operation"
                             "e.g. 'pretrain' for operation 'kill' means kill all "
                             "processes which contain 'pretrain'" )


    return parser.parse_args()

def getPid(process):
    cmd = "ps aux| grep '%s'|grep -v grep " % process
    logging.info(cmd)
    out = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    infos = out.stdout.read().splitlines()
    pidlist = []
    if len(infos) >= 1:
        for i in infos:
            pid = i.split()[1]
            if pid not in pidlist:
                pidlist.append(pid)
        return pidlist
    else:
        return -1

import numpy as np

args = get_parse_args()


pids = getPid(args.input)
print('kill: %s' % args.input,pids)

if pids==-1:
    pass
else:
    for pid in pids:
        os.kill(np.int(pid),9)
