#!/usr/bin/python

import os
from fabric.tasks import execute
from fabfile import *
import distbenchr as dbr
import signal
import time

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--experiment_tag',  help = 'Name of the experiment',             required = True)
    parser.add_argument('-k', '--kernel',          help = 'Kernel [modified or clean]',         required = True)
    parser.add_argument('-a', '--app',             help = 'Name of an application to launch',   required = True)
    parser.add_argument('-n', '--num_experiments', help = 'Number of time run the applicaiton', required = True)
    parser.add_argument('-r', '--result_dir',     help = 'Full path to dir where results will be placed', required = True)
    args = parser.parse_args()

    if (args.kernel != "clean") and (args.kernel != "modified"):
      print ("Only clean and modified kernel options are supported. Please select one of them.")
      exit(1)

    exp_name =  args.experiment + '-' + args.kernel + '-' args.app 

    execution_time = []

    # Asynchronous execution
    for exp_no in range(int(args.num_experiments)):
      mnt = dbr.Monitor()
      # server start a vm
      mnt.bg_execute(start_vm, args.kernel, should_wait=False)
      # wait for the vm to start
      time.sleep(25)

      # alloc memory in the guest to prefault memory 
      execute(prefault_hostmem)

      # start an experiment in the vm
      execute(start_experiment, exp_name, args.app, args.kernel)

      # copy the results
      path_to_results_file_on_host = execute(copy_result, exp_name, args.app, args.kernel, args.result_dir, exp_no)

      # shutdown the vm
      execute(shutdown_vm)

      # get execution time
      with open(path_to_results_file_on_host, 'r') as rfile:
        line = rfile.readline()
        if ('Test_time:' in line):
          execution_time.append(float(line.strip().split()[1]))
          break

      mnt.monitor() # wait for the client to finish
      time.sleep(30)

      print("Finished all experiments")
      print("Average execution time of ", args.app, " on ", args.kernel, " kernel is ", float(sum(execution_time))/len(execution_time))
      print(execution_time)

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
