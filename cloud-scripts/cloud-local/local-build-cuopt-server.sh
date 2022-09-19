#!/bin/bash
if [ "$API_KEY" == "" ]; then
    read -sp 'Enter a NGC api-key to access cuOpt resources: ' API_KEY
    echo
fi
SERVER_TYPE="${SERVER_TYPE:-api}"
DIR=$(dirname $(dirname $(realpath "$0")))/scripts

mkdir logs
$DIR/install-cnc.sh 2>&1 | tee logs/install-cnc.log
$DIR/wait-cnc.sh 2>&1 | tee logs/wait-cnc.log
API_KEY=$API_KEY SERVER_TYPE=$SERVER_TYPE $DIR/cuopt-helm.sh 2>&1 | tee logs/cuopt-helm.log
$DIR/wait-cuopt.sh 2>&1 | tee logs/wait-cuopt.log
$DIR/delete-secret.sh 2>&1 | tee logs/delete-secret.log

ip=localhost
nmsg="The address of the cuOpt notebook server is $ip:30001"
amsg="The address of the cuOpt api server is $ip:30000"
case $cuopt_server_type in
  "jupyter")
     msg=$nmsg
     ;;
  "both")
     msg="$amsg\n$nmsg"
     ;;
  *)
     msg=$amsg
     ;;
esac
echo -e $msg 2>&1 | tee local-build-cuopt-server.log
