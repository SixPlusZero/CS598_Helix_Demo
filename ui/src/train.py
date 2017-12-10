from __future__ import absolute_import, unicode_literals
import os
import sys
import time

def save_code(mlcode):
    workflow_name = "CensusExample"
    with open("/Users/sixpluszero/work/gestalt/src/main/scala/com/smiley/datamodel/workflows/client/CensusExample.scala", "w") as fp:
        fp.write(mlcode)
    return workflow_name

def compile_code():
    os.system("cd /Users/sixpluszero/work/gestalt; sbt/sbt compile")
    return 0

def run_code():
    cmd = "java -Xmx60000m -cp target/scala-2.11/smiley-assembly-0.1.jar com.smiley.datamodel.workflows.client.CensusExample > ./runningout.txt"
    ts_start = time.time()
    os.system("cd /Users/sixpluszero/work/gestalt; %s" % (cmd))
    ts_end = time.time()
    print("run time is %f" % (ts_end - ts_start))
    return 0

