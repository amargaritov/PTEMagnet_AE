#!/usr/bin/env python

import os
#from fabric.tasks import execute
from fabric.api import *
from fabfile import *
import distbenchr as dbr
import signal
import time

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--experiment_tag',  help = 'Name of the experiment',             required = True, type=str)
    parser.add_argument('-k', '--kernel',          help = 'Kernel [modified or clean]',         required = True, type=str)
    parser.add_argument('-a', '--app',             help = 'Name of an application to launch',   required = True, type=str)
    parser.add_argument('-n', '--num_experiments', help = 'Number of time run the applicaiton', required = True, type=int)
    parser.add_argument('-r', '--result_dir',     help = 'Full path to dir where results will be placed', required = True, type=str)
    args = parser.parse_args()

    if (args.kernel != "clean") and (args.kernel != "modified"):
      print ("Only clean and modified kernel options are supported. Please select one of them.")
      exit(1)

    exp_name =  args.experiment_tag + '-' + args.kernel + '-' + args.app 

    execution_time = []

    # Asynchronous execution
    for exp_no in range(int(args.num_experiments)):
      mnt = dbr.Monitor()
      # server start a vm
      print(args.kernel)
      mnt.bg_execute(start_vm, str(args.kernel).replace("\"",""), should_wait=False)
      # wait for the vm to start
      time.sleep(40)

      # alloc memory in the guest to prefault memory 
      execute(prefault_hostmem)

      # start an experiment in the vm
      execute(start_experiment, exp_name, args.app, args.kernel)

      # copy the results
      execute(copy_result, exp_name, args.app, args.kernel, args.result_dir, exp_no)
      path_to_results_file_on_host =  args.result_dir+ '/' + args.app + '-on-' + args.kernel + '-kernel/' + 'result_' + str(exp_no)

      # shutdown the vm
      mnt.bg_execute(shutdown_vm)

      # get execution time -- parse the reuslt file on the host
      with open(path_to_results_file_on_host, 'r') as rfile:
        for line in rfile.readlines():
          if ('Test_time:' in line):
            execution_time.append(float(line.strip().split()[1]))
            break

#      mnt.monitor() # wait for the client to finish
      time.sleep(40)
      mnt.killall()

      print("Finished all experiments, execution times are:")
      print(execution_time)
      print("Average execution time of " + args.app + " on " + args.kernel + " kernel is " + str(float(sum(execution_time))/len(execution_time)))

if __name__ == "__main__":
    # FIXME: Terminal is messed up without this
    os.setpgrp() # create new process group, become its leader
    try:
        main()
    except:
        import traceback
        traceback.print_exc()
    finally:
        os.killpg(0, signal.SIGKILL) # kill all processes in my group
