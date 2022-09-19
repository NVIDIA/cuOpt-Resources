#!/bin/bash

git clone https://github.com/NVIDIA/cloud-native-core
cd cloud-native-core/playbooks
cat << EOF > hosts
[master]
localhost ansible_connection=local
EOF

sed -i 's,docs.projectcalico.org/v3.23/manifests/calico.yaml,docs.projectcalico.org/manifests/calico.yaml,g' *.yaml
set -x
./setup.sh install
