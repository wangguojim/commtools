#!/usr/bin/python
import subprocess
import sys
import logging
import os,signal

gameproc = ["pretrain"]

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
for process in gameproc:
    pids = getPid(process)
    print('kill: %s' % process,pids)
    if pids==-1:
        pass
    else:
        for pid in pids:
            os.kill(np.int(pid),9)
