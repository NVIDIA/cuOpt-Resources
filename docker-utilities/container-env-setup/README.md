# Setting up a new Ubuntu machine to run cuOpt

These instructions show how to set up an Ubuntu machine to run cuOpt, beginning with a freshly installed OS (baremetal or VM).
If the host already has Docker or NVIDIA components installed, the *install.sh* script may not work.

## General requirements

+ OS: Ubuntu 18.04, 20.04, 22.04

+ Disk space: at least 64GB in the root partition
    
## Additional requirements for VMs on cloud platforms

+ Instance type must include an NVIDIA GPU

    + AWS instance type - G4dn (tested on g4dn.xlarge)

    + Azure instance type - NC-series (tested on Standard_NC6s_v2)

    + GCP instance type - N1 series with added GPU (n1-standard-2 with T4 GPU)

+ SSH access:

    A security group should be used that opens port 22.

## Clone this repository and run the *install.sh* script

```bash
$ cd ~
$ git clone https://github.com/nvidia/cuopt-resources
$ cd cuopt-resources/docker-utilities/container-env-setup
$ ./install.sh
```

## Testing the Installation

Log out of the host and then log back in. If installation was successful you will be
able to run the following docker image without sudo and display information about the GPU.

```bash
$ docker run --gpus all nvcr.io/nvidia/cuda:11.1.1-base-ubi8 nvidia-smi
```

Log in to nvcr.io using your NGC api key for the password
```
$ docker login nvcr.io -u \$oauthtoken
```

Use the optional *run_cuopt.sh* script to run the cuOpt Jupyter server.
See the *README.md* in the utilities directory for more information.

```
$ cd ~/cuopt-resources/docker-utilities/utilities
$ ./run_cuopt.sh
```
