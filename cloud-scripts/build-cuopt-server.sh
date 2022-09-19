#!/bin/bash
DIR=$(dirname $(realpath "$0"))
if [ "$API_KEY" == "" ]; then
    read -sp 'Enter a NGC api-key to access cuOpt resources: ' API_KEY
fi

TF_VAR_api_key=$API_KEY terraform apply --auto-approve
if [ "$?" -ne 0 ]; then
    exit -1
fi
terraform output --json outputs > values.json
$DIR/utilities/parse.py values.json values.sh
source values.sh

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
echo -e $msg
