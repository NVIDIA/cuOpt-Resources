# utilities

This directory contains convenience scripts and examples for running the cuOpt server, or running a Jupyter cuOpt notebook or local cuOpt program in a Docker container using the direct Python API.

The included Dockerfile can be used to create a derived image with additional conda dependencies added to the cuOpt environment.

## Overview

The cuOpt image includes a conda environment with cuOpt and its dependencies installed.

The *run_cuopt.sh* script uses docker facilities to:

* optionally mount a local program and the enclosing directory on the container
* optionally mount a requirements file on the container and install those requirements in the conda environment
* optionally mount a local directory on the container where results or local notebooks can be written
* execute the specified program or start a Jupyter notebook server within the cuOpt environment

This can be done directly from the command line, but the script makes it simpler.

The *run_server.sh* script is a convenience script for launching the cuOpt API server.

## Using run_cuopt.sh to launch a Jupyter notebook server

By default *run_cuopt.sh* will launch a Jupyter server with example cuOpt notebooks.

```
./run_cuopt.sh
```

Jupyter urls will be displayed on the console. To access Jupyter from a remote machine, copy the
url with the local address *127.0.0.1* and replace the local address with the external IP address of the host.

## Using run_cuopt.sh to execute a local program

The *cuopt-api/cuopt-api.py* program uses the Python API to solve a CVRPTW problem. It has a local dependency *helper_function* in the same directory. This command will mount the *cuopt-api* directory on the container and execute *cuopt-api.py*. The path of the directory in the container can be read from the CUOPT_PROG_DIR environment variable:

```
./run_cuopt.sh cuopt-api/cuopt-api.py
```

## Common options for *run_cuopt.sh*

To run cuOpt in detached mode, use the -d option. Include -o *filename* to specify a logfile

```
./run_cuopt.sh -do mylogfile
```

If a program requires additional dependencies that are not in the same directory as the executable, they can be listed in a conda requirements file and specified with the **-r** option.

```
./run_cuopt.sh -r requirements.txt
```

To override the default cuOpt container image, use the **-i** option.

```
./run_cuopt.sh -i my_derived_cuopt_image:latest
```

The **-l** option specifies a local directory to mount on the container. This directory can be used to store results, or load or save local notebooks or hold resources. The path of this directory in the container can be read from the CUOPT_LOCAL_DIR environment variable.

```
./run_cuopt.sh -l my-local-notebooks
```

## Running the cuOpt server with *./run_server.sh*

This command will run the cuOpt server. The server will listen on 127.0.0.1:5000.

```
./run_server.sh

# check that the server is running
curl 127.0.0.1:5000/cuopt/health
```

The cuopt_api/post-cuopt.py file will send a problem to the server:

```
cd cuopt-api
./post-cuopt.py
```

To run the server in detached mode, use the -d option. Include -o *filename* to specify a logfile

```
./run_server.sh -do mylogfile
```

## Deriving a new cuOpt image with additional dependencies

If your application has additional dependencies, it may be convenient to create a new cuOpt image which has those dependencies pre-installed. The included Dockerfile makes this simple.

Add your conda dependencies to *requirements.txt* and then build the new image

```
docker build . -t my_derived_cuopt_image:latest
```
