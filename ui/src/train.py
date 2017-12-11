from __future__ import absolute_import, unicode_literals
import os
import sys
import time
BASE_PATH = "/Users/sixpluszero/work/"
GESTALT_PATH = BASE_PATH + "gestalt/"


def save_code(mlcode):
    CODE_PATH = "src/main/scala/com/smiley/datamodel/workflows/client/"
    WORKFLOW = "CensusExample"
    with open("%s%s%s.scala" % (GESTALT_PATH, CODE_PATH, WORKFLOW), "w") as fp:
        fp.write(mlcode)
    return WORKFLOW

def compile_code():
    os.system("cd %s; sbt/sbt compile" % (GESTALT_PATH))
    return 0

def run_code(workflow, logfile):
    cmd = "java -Xmx60000m -cp target/scala-2.11/smiley-assembly-0.1.jar com.smiley.datamodel.workflows.client.%s > ./%s" % (workflow, logfile)
    ts_start = time.time()
    os.system("cd %s; %s" % (GESTALT_PATH, cmd))
    ts_end = time.time()
    print("run time is %f" % (ts_end - ts_start))
    return 0

def extract_runtime(logfile):
    with open("%s%s" % (GESTALT_PATH, logfile), "r") as fp:
        for line in fp:
            if line.find("Execution time: [") != -1:
                ans = line[17:line.find("]")]
                return float(ans)
    return 0.0
    
def extract_accuracy(logfile):
    with open("%s%s" % (GESTALT_PATH, logfile), "r") as fp:
        for line in fp:
            if line.find("Accuracy ") != -1:
                ans = line.strip("\n")[9:]
                return float(ans)
    return -1.0
