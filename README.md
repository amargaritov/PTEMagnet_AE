# PTEMagnet Artifact Evaluation Pack

This repository includes an artifact evaluation pack for PTEMagnet (#111 ASPLOS'21 paper). The artifact reproduces the results of Figure 6 in the paper. This repo also includes the PTEMagnet path for Linux Kernel, making it publically available. The artifact consists of:
* a patch implementing PTEMagnet in Linux Kernel v4.19 together with scripts for building clean and modified versions of the kernel 
* a disk image for QEMU containing Ubuntu 16.04 LTS with selected SPEC'17, GPOP, and MLPerf ObjDetect benchmarks with their reference datasets; the disk image also contains scripts for running SPEC'17 and GPOP benchmarks colocated with MLPerf ObjDetect 
* a python scripts for launching and measuring the execution time of SPEC'17 and GPOP benchmarks when running colocated with MLPerf ObjDetect within a virtual machine with and without PTEMagnet
* scripts for installing relevant tools and setting the environment

## Installation
### Part 1: packages and environment
On Ubuntu 18.04 LTS, 
```bash
./install/install_all.sh <PATH_TO_DIR_WITH_AT_LEAST_150GB_FREE_SPACE> 
```
This script  
* installs all relevant 
* builds the _clean_ kernel and the _modified_ kernel with PTEMagnet
* downloads the disk image for a VM (if run outside of Cloudlab)
* sets relevant shell and python environment for scripts automating launching and measuring the execution time of benchmarks
* disables THP on the host machine

**Note that we can provide access to a preconfigured Cloudlab profile (and servers) on which this code was tested. Using the Cloudlab profile accelerates installation and simplifies troubleshooting. If you are interested in running the artifact evaluation on Cloudlab, please email Artemiy <artemiy.margaritov@ed.ac.uk>.**

### Part 2: setting ssh keys for passwordless login to a machine 
Evaluation scripts should be able to passwordlessly ssh to 1) a virtual machine where the benchmarks would run and 2) to the host. In our opinion, the simplest way to achieve passwordless ssh is using ssh keys. To upload an ssh key to the virtual machine
* Generate ssh key with 
```bash
ssh-keygen -t rsa
```
* Boot a virtual machine with the provided disk image
```bash
KERNEL=clean; sudo qemu-system-x86_64 -kernel /disk/local/linux/linux_$KERNEL/arch/x86/boot/bzImage -boot c -m 64G -hda /disk/local/rootfs.img -append "root=/dev/sda rw" -device e1000,netdev=net0 -netdev user,id=net0,hostfwd=tcp::6666-:22 --enable-kvm -smp 20 -cpu host -nographic
```
* Wait for machine to boot (login prompt should appear)
* Start a new shell on the host, upload the generated ssh key to a virtual machine 
```bash 
ssh-copy-id -p 6666 user@localhost
```
when asked for password, type `user`
* To allow passwordless login from the host to the host itself upload the ssh key to it
```bash
# This does not work on Cloudlab!
ssh-copy-id $USER@localhost
```
If using Cloudlab, you would need to copy your cloudlab ssh key to the host 
```bash
# on machine you ssh to Cloudlab to
scp -P 22 ~/.ssh/<YOUR_CLOUDLAB_KEY> <CLOUDLAB_USERNAME@CLOUDLAB_MACHINE>:~/.ssh/ 
# on Cloudlab machine
chmod 400 ~/.ssh/<YOUR_COPIED_CLOUDLAB_KEY>
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/<YOUR_COPIED_CLOUDLAB_KEY>
```
* Shutdown the virtual machine
```bash 
ssh -p 6666 user@localhost 'sudo shutdown -h now' 
```


## Evaluation 
```bash
cd ./evaluation/; 
mkdir -p results;
./lauch_exp.py --experiment_tag asplos21_ae --kernel [ clean | modified] --app [ bfs | cc | nibble | pr | gcc | mcf | omnetpp | xz ] --num_experiments <int>  --result_dir <PATH_TO_STORE_RESULT_FILES> 
```
This script runs the benchmark specified under the `app` parameter in colocation with MLPerf ObjDetect in a virtual machine under the selected kernel type `num_experiments` number of times. The script outputs (prints) the average execution time of the benchmark in such an environment at the end of its execution. 
For example, the following command will print average execution time for mcf run 10 times on a kernel with PTEMagnet (in colocaiton with MLPerf ObjDetect):
```bash
cd ./evaluation/; mkdir -p results; ./lauch_exp.py --experiment_tag asplos21_ae --kernel modified --app mcf --num_experiments 10 --result_dir ./results
```
To reproduce the results of Figure 6, one needs to run the script for each benchmark two times: with clean and modified kernel and compare the execution times. 

## Miscellaneous

### Building Linux kernel 
Note that both clean and modified Linux kernels were already built by the installation script. You need to run it only if you want to rebuild them. 
```bash
./install/build_kernels.sh <PATH_TO_WHERE_PUT_KERNELS> 
```
Note that both clean and modified Linux kernels were already built by the installation script. You need to run it only if you want to rebuild them. 

### Downloading the VM image
Note that the VM image is already downloaded by the installation script. You don't need to run it.
```bash
./install/download_vm_disk_image.sh <PATH_TO_WHERE_PUT_IMAGE>
```
### Running a virtual machine manually
If you want to boot a virtual machine with the VM image manually you can run the following command:
```bash 
KERNEL=clean; sudo qemu-system-x86_64 -kernel /disk/local/linux/linux_$KERNEL/arch/x86/boot/bzImage -boot c -m 64G -hda /disk/local/rootfs.img -append "root=/dev/sda rw" -device e1000,netdev=net0 -netdev user,id=net0,hostfwd=tcp::6666-:22 --enable-kvm -smp 20 -cpu host -nographic
```
This command boot a machine with 20 cores and 64GB memory. 
After launching the virtual machine you can ssh into it with
```bash 
ssh -p 6666 user@localhost
```
password is `user`
