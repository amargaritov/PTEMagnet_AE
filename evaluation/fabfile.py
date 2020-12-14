#!/usr/bin/python

from fabric.api import env, roles, run, settings, hide, get
from distbenchr import run_bg

import os
import socket
import glob2


def_cmd = ' cd /disk/local/ptemagnet_eval; source source.sh; '
kernel_dir = os.environ['KERNEL_DIR']
image_dir =  os.environ['IMAGE_DIR']

env.roledefs = {
        'servers': [socket.gethostname()],
        'clients': ['user@localhost:6666'],
        }


@roles('servers', 'clients')
def get_info():
  run('hostname')


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#########
# Client
########


@roles('clients')
def start_experiment(exp_name, app, kernel):
  if kernel == "clean":
    kernel_mode = "0"
  else:
    kernel_mode = "1"
  cmd = def_cmd + ' cd $REPO_ROOT/atc_measurements/' + app + '; ./record-mlperf.sh 1 2 0 ' + kernel_mode
  run(cmd)

@roles('clients')
def prefault_hostmem():
  with settings(hide('warnings'), warn_only=True,):
    cmd = def_cmd + '$REPO_ROOT/atc_measurements/prefault_hostmem/alloc_60GB.sh'
    run(cmd)


@roles('clients')
def copy_result(exp_name, app, kernel, host_result_dir, exp_no):
  guest_result_dir = '/disk/memphis/data/traces/'
  source = guest_result_dir + app + '/' + 'result' 
  target = host_result_dir + '/' + app + '-on-' + kernel + '-kernel/' + 'result_' + str(exp_no)
  get(source, target)


@roles('clients')
def shutdown_vm():
  with settings(hide('warnings'), warn_only=True,):
    run('sudo shutdown -h now')



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#########
# Server
########

@run_bg('servers')
def start_vm(kernel):
  kernel = kernel.replace("\"","") 
  #cmd = 'sudo numactl --membind=0 --cpunodebind=0 qemu-system-x86_64 -kernel ' + kernel_dir + '/linux_' + str(kernel) + '/arch/x86/boot/bzImage -boot c -m 64G -hda ' + image_dir + '/rootfs.img -append "root=/dev/sda rw transparent_hugepage=never" -device e1000,netdev=net0 -netdev user,id=net0,hostfwd=tcp::6666-:22 --enable-kvm -smp 20 -cpu host -nographic'
  cmd = 'sudo qemu-system-x86_64 -kernel ' + kernel_dir + '/linux_' + str(kernel) + '/arch/x86/boot/bzImage -boot c -m 64G -hda ' + image_dir + '/rootfs.img -append "root=/dev/sda rw transparent_hugepage=never" -device e1000,netdev=net0 -netdev user,id=net0,hostfwd=tcp::6666-:22 --enable-kvm -smp 20 -cpu host -nographic'
  run(cmd)
