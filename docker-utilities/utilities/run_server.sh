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

image=nvcr.io/nvidia/cuopt/cuopt:22.12
detached=False
detached_log=

function help {
    echo "This script runs a cuOpt server in a container. The server will be accessible at 127.0.0.1:5000."
    echo "The image should be a NVIDIA cuOpt server image or based on a NVIDIA cuOpt server image."
    echo
    echo "usage: run_server.sh [-h] [-d [-o DETACHED_LOGFILE]] [-i IMAGE_PULL_SPEC]"
    echo
    echo "options:"
    echo "  -d                    Run the container in detached mode (container runs disconnected from the terminal)."
    echo "                        This is useful for launching cuOpt and then closing the terminal or logging out."
    echo "  -o DETACHED_LOGFILE   Logifle for detached mode. If this option is set, stderr and stdout from the container"
    echo "                        will be written to the specified file in detached mode."    
    echo "  -i IMAGE_PULL_SPEC    Specifies the image to use to run cuOpt (default $image)"
    echo
}

while getopts "hi:do:" option; do
    case $option in
      d)
	 detached=True;;
      o)
	 detached_log=$OPTARG;;	
      h) # display Help
         help
         exit;;
      i)
         image=$OPTARG;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

shift "$(( OPTIND - 1 ))"

if [ -n "$detached_log" ]; then
    if [ "$detached" == "False" ]; then
	echo "WARNING: -o option ignored since -d not set"
    fi
fi
echo \(There may be little or no output from the cuOpt server. This is expected\)
if [ "$detached" == "True" ]; then
    a=$(docker run --rm -d --gpus=all --network=host $image)
    echo Running cuOpt server in detached mode.
    echo
    echo To halt the server run the following command:
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
else
    echo Press ctrl-C to halt
    docker run --rm -it --gpus=all --network=host $image
fi
