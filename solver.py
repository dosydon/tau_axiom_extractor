from sas import State
from utils import plan_from_file
import argparse
import subprocess
import os
import re


class FD:
    SCRIPT = "/home/miura/workspace/icaps17ex/fd-inc/fast-downward.py"
    DEVNULL = open(os.devnull,'w')
    def __init__(self):
        self.log = "__FD_.txt"
        self.temp_sas =  "__temp.sas"
        self.temp_plan =  "__temp_plan"

    def solve(self,subsas,sas,config=""):
        with open(self.temp_sas,"w") as f:
            print(subsas, file = f)
#         subprocess.call(self.SCRIPT+" --preprocess {}".format(self.temp_sas),shell=True,stdout=self.DEVNULL)
        with open(self.log,"w") as f:
            subprocess.call(self.SCRIPT+" --plan-file {} {} --search 'astar(blind())'".format(self.temp_plan, self.temp_sas) ,shell=True,stdout=f)
            f.flush()
        propeties = self.get_properties()
        return plan_from_file(sas,self.temp_plan),propeties

    def get_properties(self):
        propeties = {} 
        with open(self.log,"r") as f:
            contents = f.read()
            m = re.search('Peak memory: (\d+) KB',contents)
            if m:
                propeties['peak_memory'] = int(m.group(1))
            m = re.search('Search time: (\d+.\d+)s',contents)
            if m:
                propeties['search_time'] = float(m.group(1))
            else:
                propeties['search_time'] = 0
        for k,v in propeties.items():
            print((k,v))
        return propeties 

