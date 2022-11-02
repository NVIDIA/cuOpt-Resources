#!/bin/bash

# SPDX-FileCopyrightText: Copyright (c) 2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: MIT

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

detached=False
detached_log=
jupyterserver=True
requirements=
image=nvcr.io/nvidia/cuopt/cuopt:22.10.01
localdir=
have_realpath=$(command -v realpath)

function help {
    echo "This script runs a Jupyter notebook server or Python program within the cuOpt environment in a container"
    echo "using the specified image. The image should be a NVIDIA cuOpt image or based"
    echo "on a NVIDIA cuOpt image."
    echo
    echo "usage: run_cuopt [-h] [-d [-o DETACHED_LOGFILE]] [-r REQUIREMENTS_FILE] [-l LOCAL_DIR] [-i IMAGE_PULL_SPEC] [PYTHON_FILE]"
    echo
    echo "options:"
    echo "  -d                    Run the container in detached mode (container runs disconnected from the terminal)."
    echo "                        This is useful for launching cuOpt and then closing the terminal or logging out."
    echo "  -o DETACHED_LOGFILE   Logifle for detached mode. If this option is set, stderr and stdout from the container"
    echo "                        will be written to the specified file in detached mode."
    echo "  -r REQUIREMENTS_FILE  Specifies a conda requirements file to install before"
    echo "                        running the specified program. The path may be relative if realpath is installed."
    echo "  -l LOCAL_DIR          Specifies a local directory to mount on the container."
    echo "                        This directory can be used to store results, load or save local notebooks,"
    echo "                        or hold resources. The location of this directory in the container"
    echo "                        can be read from the environment variable CUOPT_LOCAL_DIR."
    echo "  -i IMAGE_PULL_SPEC    Specifies the image to use to run cuOpt (default $image)"
    echo
    echo "arguments:"
    echo "  PYTHON_FILE           Optional path of a Python file to run in the cuOpt environment."
    echo "                        If this argument is not specified, the notebook server is started."
    echo "                        The path may be relative if realpath is installed."
    echo "                        The directory containing the Python file will be mounted on the container."
    echo "                        The location of this directory in the container can be read from the"
    echo "                        environment variable CUOPT_PROG_DIR."
}

function resolvepath {
    local path=$1
    if ! [[ "$path" == /* ]]; then
        if [ -n "$have_realpath" ]; then
            path=$(realpath $path)
	else
	    echo "Relative paths are not supported unless realpath is installed"
	    exit -1
        fi
    fi
    if ! [[ -e $path ]]; then
	echo Path $path does not exist
	exit -1
    fi
    echo $path
}

while getopts "hr:i:l:do:" option; do
   case $option in
      h) # display Help
         help
         exit;;
      d)
	  detached=True;;
      o)
	  detached_log=$OPTARG;;
      r)
         requirements=$OPTARG;;
      i)
         image=$OPTARG;;
      l)
	 localdir=$OPTARG;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

shift "$(( OPTIND - 1 ))"
if [ "$#" -gt 0 ]; then
    jupyterserver=False
    if ! [ -f "$1" ]; then
        echo "PYTHON_FILE must be a file, not a directory"
        exit
    fi
fi

if [ -n "$detached_log" ]; then
    if [ "$detached" == "False" ]; then
	echo "WARNING: -o option ignored since -d not set"
    fi
fi

# Set up volume argument for requirements.txt
req_volume=
req_install=
if [ -n "$requirements" ]; then
    requirements=$(resolvepath $requirements) || { echo $requirements ; exit ; }
    req_volume="-v $requirements:$requirements"
    req_install="conda install --file $requirements -y"
fi

# Resolve path for localdir
localdir_volume=
localdir_env=
py_dir_env=
if [ -n "$localdir" ]; then
    localdir=$(resolvepath $localdir) || { echo $localdir ; exit ; }
fi

if [ "$jupyterserver" == "True" ]; then
    if [ -n "$localdir" ]; then
        localdir_volume="-v $localdir:/home/cuopt_user/notebooks/cuopt-local"
        localdir_env="-eCUOPT_LOCAL_DIR=/home/cuopt_user/notebooks/cuopt-local"
    fi
    command="jupyter-notebook --allow-root --no-browser --ip=0.0.0.0 --notebook-dir 'notebooks'"
else
    python_path=$(resolvepath $1) || { echo $requirements ; exit ; }
    python_dir=$(dirname $python_path)
    py_dir_env="-eCUOPT_PROG_DIR=$python_dir"

    # Set up volume argument for Python executable
    volume="-v $python_dir:$python_dir"

    if [ -n "$localdir" ]; then
        localdir_volume="-v $localdir:/cuopt-local"
        localdir_env="-eCUOPT_LOCAL_DIR=/cuopt-local"
    fi

    command="python $python_path"
fi

# There are issues with "conda install" argument reading and chaining commands together,
# so we write a script file and mount if for execution instead
tmpfile=$(mktemp)
echo $req_install > $tmpfile
echo $command >> $tmpfile
chmod a+rx $tmpfile

if [ "$detached" == "True" ]; then
    a=$(docker run --rm --gpus=all -d --network=host $volume $req_volume $localdir_volume -v $tmpfile:$tmpfile $py_dir_env $localdir_env $image $tmpfile)
    echo Running cuOpt in detached mode.
    echo To halt cuOpt run the following command:
    echo
    echo -e "\tdocker stop $a"
    echo
    echo To view logs run the following command:
    echo
    echo -e "\tdocker logs $a"
    if [ -n "$detached_log" ]; then
        echo
        echo Also saving logs to \""$detached_log"\"
        docker logs -f $a > "$detached_log" 2>&1 &
    fi
    if [ "$jupyterserver" == "True" ]; then
        echo
        echo "NOTE: since you are running the Jupyter server, you must view the logs to find the Jupyter URL"
    fi
else
  echo Press ctrl-C to halt
  docker run --rm --gpus=all --network=host -it $volume $req_volume $localdir_volume -v $tmpfile:$tmpfile $py_dir_env $localdir_env $image $tmpfile
fi
rm $tmpfile
