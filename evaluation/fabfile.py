#!/usr/bin/python

from fabric.api import env, roles, run, settings, hide, get
from distbenchr import run_bg

import os
import socket
import glob2
import multiprocessing


kernel_dir = os.environ['KERNEL_DIR']
image_dir =  os.environ['IMAGE_DIR']
repo_root_host = os.environ['REPO_ROOT']

#qemu_cpu_affinity_2sockets_10_cores="10 20 21 22 23 24 25 26 27 30 31 32 33 34 35 36 37 38 39 9"
#(echo "10-19,30-39"; for i in {1..8}; do echo "0-9,20-29"; done; for i in in {1..10}; do echo "10-19,30-39"; done) | tr '\n' ' '
qemu_cpu_affinity_2sockets_10_cores="10-19,30-39 0-9,20-29 0-9,20-29 0-9,20-29 0-9,20-29 0-9,20-29 0-9,20-29 0-9,20-29 0-9,20-29 10-19,30-39 10-19,30-39 10-19,30-39 10-19,30-39 10-19,30-39 10-19,30-39 10-19,30-39 10-19,30-39 10-19,30-39 10-19,30-39 10-19,30-39"
#qemu_cpu_affinity_2sockets_12_cores="12 24 25 26 27 28 29 30 31 36 37 38 39 40 41 42 43 44 45 46"
#(b=12-23,36-47; a=0-11,24-31; echo $b; for i in {1..8}; do echo $a; done; for i in in {1..10}; do echo $b; done) | tr '\n' ' '
qemu_cpu_affinity_2sockets_12_cores="12-23,36-47 0-11,24-31 0-11,24-31 0-11,24-31 0-11,24-31 0-11,24-31 0-11,24-31 0-11,24-31 0-11,24-31 12-23,36-47 12-23,36-47 12-23,36-47 12-23,36-47 12-23,36-47 12-23,36-47 12-23,36-47 12-23,36-47 12-23,36-47 12-23,36-47 12-23,36-47"

def_cmd = ' cd /disk/local/ptemagnet_eval; source source.sh; '
def_server_cmd = ' cd ' + repo_root_host + '; source source.sh; '

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
    cmd = def_cmd + '$REPO_ROOT/atc_measurements/prefault_hostmem/alloc_125GB.sh'
#    cmd = def_cmd + '$REPO_ROOT/atc_measurements/prefault_hostmem/alloc_60GB.sh'
    run(cmd)


@roles('clients')
def copy_result(exp_name, app, kernel, host_result_dir, exp_no):
  guest_result_dir = '/disk/memphis/data/traces/'
  source = guest_result_dir + app + '/' + 'result' 
  target = host_result_dir + '/' + app + '-on-' + kernel + '-kernel/' + 'result_' + str(exp_no)
  get(source, target)


#@roles('clients')
@run_bg('clients')
def shutdown_vm():
  with settings(hide('warnings'), warn_only=True,):
    try:
        run('sudo shutdown -h now')
    except paramiko.ssh_exception.SSHException:
        pass



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#########
# Server
########

@run_bg('servers')
def start_vm(kernel):
  kernel = kernel.replace("\"","") 
  #cmd = 'sudo numactl --membind=0 --cpunodebind=0 qemu-system-x86_64 -kernel ' + kernel_dir + '/linux_' + str(kernel) + '/arch/x86/boot/bzImage -boot c -m 128G -hda ' + image_dir + '/rootfs.img -append "root=/dev/sda rw transparent_hugepage=never" -device e1000,netdev=net0 -netdev user,id=net0,hostfwd=tcp::6666-:22 --enable-kvm -smp 20 -cpu host -nographic'
#  cmd = 'sudo qemu-system-x86_64 -kernel ' + kernel_dir + '/linux_' + str(kernel) + '/arch/x86/boot/bzImage -boot c -m 128G -hda ' + image_dir + '/rootfs.img -append "root=/dev/sda rw transparent_hugepage=never" -device e1000,netdev=net0 -netdev user,id=net0,hostfwd=tcp::6666-:22 --enable-kvm -smp 20 -cpu host -nographic -numa node,nodeid=0 -numa node,nodeid=1 -name test,debug-threads=on'
#  cmd = 'sudo qemu-system-x86_64 -kernel ' + kernel_dir + '/linux_' + str(kernel) + '/arch/x86/boot/bzImage -boot c -m 128G -hda ' + image_dir + '/rootfs.img -append "root=/dev/sda rw transparent_hugepage=never" -device e1000,netdev=net0 -netdev user,id=net0,hostfwd=tcp::6666-:22 --enable-kvm -smp 20 -cpu host -nographic -name test,debug-threads=on'
  cmd = 'sudo qemu-system-x86_64 -kernel ' + kernel_dir + '/linux_' + str(kernel) + '/arch/x86/boot/bzImage -boot c -m 128G -hda ' + image_dir + '/rootfs.img -append "root=/dev/sda rw transparent_hugepage=never" -device e1000,netdev=net0 -netdev user,id=net0,hostfwd=tcp::6666-:22 --enable-kvm -smp 20 -cpu host -nographic -name test,debug-threads=on'
  run(cmd)

@roles('servers')
def pin_qemu_threads():
    cpucount = multiprocessing.cpu_count() 
    if cpucount == 40:
        qemu_cpu_affinity = qemu_cpu_affinity_2sockets_10_cores
    else:
        if cpucount == 48:
            qemu_cpu_affinity = qemu_cpu_affinity_2sockets_12_cores
        else:
            print("This artifact can not be tested on a machine with less than 20 physical CPU cores")
    # this one works on Cloudlab c220g5
    #cmd = def_server_cmd + ' sudo python3 ' + repo_root_host + '/evaluation/qemu_affinity.py -v -k 10 20 21 22 23 24 25 26 27 30 31 32 33 34 35 36 37 38 39 9 -- `ps aux | grep qemu-system-x86 | grep -v sudo | head -n 1 | awk \'{print $2}\'`'
    cmd = def_server_cmd + ' sudo python3 ' + repo_root_host + '/evaluation/qemu_affinity.py -v -k ' + qemu_cpu_affinity + ' -- `ps aux | grep qemu-system-x86 | grep -v sudo | head -n 1 | awk \'{print $2}\'`'
    run(cmd)
