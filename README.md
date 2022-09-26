# cuOpt Resources
NVIDIA cuOpt is an Operations Research optimization API using AI to help developers create complex, real-time fleet routing workflows on NVIDIA GPUs.
This repository contains a collection of resources demonstrating the setup and use of NVIDIA cuOpt via Python and REST based microservice APIs. 


The cuOpt-Resources repository is under [MIT License](LICENSE.md)

Use of NVIDIA cuOpt is subject to the [End User License Agreement](https://docs.nvidia.com/cuopt/NVIDIA_cuOpt_EULA.pdf)



## [NVIDIA cuOpt](https://developer.nvidia.com/cuopt-logistics-optimization)

cuOpt uses highly optimized GPU-accelerated solvers relying on heuristics, metaheuristics, and optimization. In addition to providing dramatically accelerated, world class solutions to some of the most difficult optimization problems, NVIDIA cuOpt prioritizes ease of use through high level Python and REST based microservice APIs

 [cuOpt Docs](https://docs.nvidia.com/cuopt/overview.html)

 cuOpt on NGC container
 - [Collections](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/cuopt/collections/route_optimization)
 - [Containers](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/cuopt/containers/cuopt)
 - [Helm Charts](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/cuopt/helm-charts/cuopt)

## Contents
* NVIDIA cuOpt Python API example notebooks
  * [Routing Optimization](notebooks/routing/python)
<br><br>
* NVIDIA cuOpt REST based microservice example notebooks
  * [Routing Optimization](notebooks/routing/microservice) 
<br><br>
* [Cloud deployments scripts for AWS, Azure, and GCP](cloud-scripts/)


# Setup
Whether deploying locally or in the cloud, an NVIDIA GPU Cloud (NGC) account will be required. NGC hosts a catalog of GPU-optimized software for AI developers. Access is free and it takes just a few minutes to register. For information about creating an NGC account and generating the required API key, see the following documentation:

[Registering and Activating NGC Account](https://docs.nvidia.com/ngc/ngc-overview/index.html#registering-activating-ngc-account)

## Local Environment
### Prerequisites
* NVIDIA GPU and associated driver 450.80.02+
  * Pascal architecture or better
* [CUDA](https://developer.nvidia.com/cuda-downloads) 11.0+
* cuOpt Docker container downloaded from [NGC](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/cuopt/containers/cuopt)

### Instructions
* Clone the cuOpt-Resources repo
* Pull the [cuOpt container from NGC](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/cuopt/containers/cuopt)
* Follow the instructions provided on NGC to run the cuOpt container and mount the example notebooks relevant to your desired API.

## Cloud Environment
### Prerequisites
* AWS, Azure, or GCP account (but see [Alternative "Cloud Local"](#alternative-cloud-local) for another option)
* Permission to provision compute resources
* NVIDIA NGC account credentials

#### Alternative "Cloud Local"

If you don't have an AWS, Azure, or GCP account or you want to run cuOpt with NVIDIA Cloud Native Core on a server that you create yourself, read on and look for the *Cloud Local* section in the [cloud-scripts directory](cloud-scripts/) README.

### Instructions
* Clone the cuOpt-Resources repo
* See detailed instructions provided in the [cloud-scripts directory](cloud-scripts/) README.
