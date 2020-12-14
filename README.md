# PTEMagnet_artifact_evaluation

This repository includes an artifact for PTEMagnet (#111 ASPLOS'21 paper). The artifact reproduces the results of Figure 6 in the paper. This repo also includes the PTEMagnet path for Linux Kernel, making it publically available. The artifact consists of:
* a patch implementing PTEMagnet in Linux Kernel v4.19 with scripts for building clean and modified versions of the kernel 
* a disk image for QEMU containing Ubuntu 16 LTS with selected SPEC'17, GPOP, and MLPerf ObjDetect benchmarks with their reference datasets; the disk image also contains scripts for running SPEC'17 and GPOP benchmarks colocated with MLPerf ObjDetect 
* a python scripts for launching and measuring the execution time of SPEC'17 and GPOP benchmarks when running colocated with MLPerf ObjDetect within a virtual machine with and without PTEMagnet

## Installation
On Ubuntu 18 LTS, 
```bash
./install/install_all.sh <PATH_TO_DIR_WITH_AT_LEAST_150GB_FREE_SPACE> 
```
This script  
* installs all relevant 
* builds the _clean_ kernel and the _modified_ kernel with PTEMagnet
* downloads the disk image for a VM (if run outside of Cloudlab)
* sets relevant shell and python environment for scripts automating launching and measuring execution time of benchmarks
* disables THP on the host machine

**Note that we can provide access to a preconfigured Cloudlab profile (and servers) on which this code was tested. Using the Cloudlab profile accelerates installation and simplifies troubleshooting. If you are intersted in running the artifact evaluation on Cloudlab, please email to Artemiy <artemiy.margaritov@ed.ac.uk>.**

## Evaluation 
```bash
cd ./evaluation/; 
mkdir -p results;
./lauch_exp.py --experiment_tag asplos21_ae --kernel [ clean | modified] --app [ bfs | cc | nibble | pr | gcc | mcf | omnetpp | xz ] --num_experiments <int>  --result_dir <PATH_TO_STORE_RESULT_FILES> 
```
This script runs the benchmark specified under by the `app` parameter in colocation with MLPerf ObjDetect in a virtual machine under the selected kernel type `num_experiments` number of times. The script outputs (prints) the average execution time of the benchmark in such environment at the end of its execution. 
For example, the following command will print average execution time for mcf run 10 times on a kernel with PTEMagnet (in colocaiton with MLPerf ObjDetect):
```bash
cd ./evaluation/; mkdir -p results; ./lauch_exp.py --experiment_tag asplos21_ae --kernel modified --app mcf --num_experiments 10 --result_dir ./results
```
To get the results of Figure 6, one needs to run the script for each benchmark two times: with clean and modified kernel and compare the execution times. 

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

