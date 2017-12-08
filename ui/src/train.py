from __future__ import absolute_import, unicode_literals
import os
import sys

def save_code(mlcode):
    with open("/Users/sixpluszero/sandbox/workflow.scala", "w") as fp:
        fp.write(mlcode)
