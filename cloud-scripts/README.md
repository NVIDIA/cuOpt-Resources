# cuOpt Cloud Deployment Scripts

A collection of helpful setup scripts to streamline the creation of a cloud based cuOpt development enviroment focused on routing optimization.

NGC credentials will be required as part of the setup process.  See instructions [here](https://docs.nvidia.com/ngc/ngc-overview/index.html#registering-activating-ngc-account) for generating an API key for your NGC account.

## General

The setup scripts for AWS, GCP, and Azure use Terraform to build a new VM in the cloud and run cuOpt.
For the [Cloud Local](#cloud-local) case, you will build the server yourself and then run the setup script manually.

Terminology:

* `cuOpt server` or `server` means the machine that will run cuOpt
* `build host` means the computer where cloud scripts are run to create a cuOpt server
* `cloud shell` means a Linux shell that is available from the console in AWS, GCP, and Azure, and which is integrated with your account

See the additional README files in the [AWS](aws/), [GCP](gcp/), and [Azure](azure) for some cloud-specific details.

### Minimum Server Specs

The Terraform scripts for AWS, GCP, and Azure have sane defaults but allow you to adjust details of the server.
The minimum requirements for a cuOpt server are:

* 64GB root partition
* 4 CPU
* 8GB memory
* Ubuntu 22.04 OS
* NVIDIA GPU Pascal architecture or better
* ports 30000, 30001 open for cuOpt access and port 22 open for ssh access

## Using a Cloud Shell as the Build Host

Open a cloud shell for your chosen cloud: [AWS](https://docs.aws.amazon.com/cloudshell/latest/userguide/working-with-cloudshell.html), [Azure](https://learn.microsoft.com/en-us/azure/cloud-shell/overview), or [GCP](https://cloud.google.com/shell/docs/using-cloud-shell).

The GCP and Azure shells have Terraform pre-installed. For AWS only, the [instructions here](https://learn.hashicorp.com/tutorials/terraform/install-cli) show how to install Terraform in AWS CloudShell. These instructions are included in the [aws-install-terraform.sh](aws/aws-install-terraform.sh) wrapper script.

Clone this repository in the cloud shell, then skip ahead to [Running the cuOpt cloud scripts](#running-the-cuopt-cloud-scripts).

## Using a Linux Machine as the Build Host

[Install Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) on your local machine.

Terraform uses cloud CLIs to communicate with the different clouds. Follow these links to install a CLI:

* [Amazon aws](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
* [GCP gcloud](https://cloud.google.com/sdk/docs/install)
* [Azure az](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)

Authenticate the CLI to the cloud:

* [Amazon aws](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-prereqs.html) prerequisites and [Quickstart](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html)
  
* [GCP gcloud](https://cloud.google.com/sdk/docs/initializing)
  
  Run the following command after setting up gcloud to create credentials for Terraform to use
  ```bash
  $ gcloud auth application-default login
  ```
  
* [Azure az](https://docs.microsoft.com/en-us/cli/azure/get-started-with-azure-cli?source=recommendations#how-to-sign-into-the-azure-cli)

## Running the cuOpt Cloud Scripts

### Ensure ssh Keys Exist

A ssh key pair is required during cuOpt installation. Check to see if you already have a key pair available. (A key pair is usually made up of two files having the same name, one of which has the extension *.pub* and one of which has no extension).

```bash
$ ls ~/.ssh/
id_rsa id_rsa.pub
```

If you do not have a key pair available, you can create one like this

```bash
$ ssh-keygen -t RSA -b 4096
```

### Navigate to the Cloud Subdirectory

The cuOpt cloud scripts will always be run from the subdirectories containing cloud-specific configuration files.

```bash
$ cd cloud-scripts/aws # or gcp, or azure
```

You must initialize Terraform the first time you use it from a particular directory.
```bash
$ terraform init
```

### Set Required Values

Each cloud directory contains two settings files:

* `variables.tf` holds variable definitions
* `terraform.tfvars` is used to set values

Required values are listed in *terraform.tfvars*. If you do not set them, the script will prompt you for them.

### Creating the cuOpt Server

From your chosen cloud subdirectory, run `build-cuopt-server.sh`. You will be prompted for your NGC api-key. When it completes the script will print summary information that you can use to ssh to the server along with the cuOpt url(s).

```bash
$ ../build-cuopt-server.sh
Enter a NGC api-key to access cuOpt resources: 
...
outputs = {
  "cuopt_server_type" = "both"
  "ip" = "34.75.2.43"
  "machine" = "cuopt-merry-cobra"
  "private_key_path" = "~/.ssh/id_rsa"
  "user" = "tmckay"
}

The address of the cuOpt api server is 34.75.2.43:30000
The address of the cuOpt notebook server is 34.75.2.43:30001
```

### Deleting the cuOpt Server

From your chosen cloud subdirectory, run `teardown-cuopt-server.sh`

```bash
$ ../teardown-cuopt-server.sh
```

### Configuration Options

#### Specifying the cuOpt Server Type

By default the cuOpt API service is launched when the server is created. You may launch a Jupyter notebook server instead, or launch both.
Set the `cuopt_server_type` variable in *terraform.tfvars*.
```bash
cuopt_server_type = "both" # may also be api (default), or jupyter
```

#### Setting the NGC api-key Value in $API_KEY

You may set the environment variable `API_KEY` to avoid being prompted for your NGC key

```bash
$ export API_KEY=yourvalidapikey
```
**Tip** You can also put that line in a file and then run `source myfile` to set the value.

### Restricting Network Access 

By default, access is unrestricted to ssh and the cuOpt ports on the server. The following values in the *terraform.tfvars* files can be used to restrict access to those ports. 

* AWS

  * `ssh_cidr_blocks`
  * `cuopt_server_cidr_blocks`

* GCP

  * `additional_ports_source_ranges` (additional_ports includes ssh)
  * `cuopt_ports_source_ranges`

* Azure

  * `ssh_source_address_prefixes`
  * `cuopt_source_address_prefixes`

Each of the variables above takes a list of CIDR blocks as a value (GCP and Azure also allow IP addresses in the list).

#### Allowing ssh Access from the Build Host

Note that if you configure restricted access, you **must** allow ssh access from the build host or installation of cuOpt will fail.

For example, if the IP address of your build host is 20.47.56.12, include that  IP address in the list of addresses granted ssh access in *terraform.tfvars*
```bash
ssh_cidr_blocks = ["20.47.56.12/32", ...] # on AWS

additional_ports_source_ranges = ["20.47.56.12", ...] # on GCP

ssh_source_address_prefixes = ["20.47.56.12", ...] # on Azure
```

#### Allowing ssh Access when the Build Host is a Cloud Shell

A cloud shell's public IP address is not immediately apparent.
To find it, use a service like *ifconfig.co* from the shell
```
$ curl ifconfig.co
34.148.241.75
```

Include the cloud shell's IP address in the ssh CIDR block variable in *terraform.tfvars* as described above.

Note that the same cloud shell may be given a new IP address each time you open it. If you need to re-establish ssh access for a cloud shell after the cuOpt server has been created, you can edit the firewall rules in the cloud console for your server to include the new IP address for the cloud shell (and remove the old one).

#### Allowing ssh Access from Another Host

To allow ssh access from a host other than the build host:

* Before building the cuOpt server, include the IP address of the other host in the ssh CIDR block variable in *terraform.tfvars* as described above

* After the cuOpt server is created, ssh into the server from the build host

* Choose a ssh key pair on the other host, or create a new one. Open the public key file from the pair and copy its contents.

* Edit the `~/.ssh/authorized_keys` file on the server and paste the new public key contents into the file on a new line

### Running more than one cuOpt server on the same cloud

Terraform will track resources that it creates and destroys in the directory where it is run. This means that each directory is tied to at most a single machine. If you would like to run more than one instance of cuOpt on the same cloud, you should copy the `*.tf` and `*.tfvars` files for that cloud to another directory. For example

```bash
$ mkdir aws_two
$ cp aws/*.tf aws/*.tfvars aws_two
$ cd aws_two
```

## Cloud Local

Make sure that the host where you will run cuOpt meets the minimum server specs, and open ports 30000 and 30001 for the cuOpt API and Jupyter services.

Clone this repository and navigate to the cloud-local subdirectory
```bash
$ cd cloud-scripts/cloud-local
```

You will be prompted for your NGC api-key, or you can [set API_KEY](#setting-the-ngc-api-key-value-in-api_key) to prevent the prompt.

Set `SERVER_TYPE` to contorl which cuOpt services are started
```
$ export SERVER_TYPE=both # may also be api (default), or jupyter
```

Run the installation script.
```bash
$ ./local-build-cuopt-server.sh
Enter a NGC api-key to access cuOpt resources:
...
outputs = {
  "cuopt_server_type" = "both"
  "ip" = "34.75.2.43"
  "machine" = "cuopt-merry-cobra"
  "private_key_path" = "~/.ssh/id_rsa"
  "user" = "tmckay"
}
The address of the cuOpt api server is localhost:30000
The address of the cuOpt notebook server is localhost:30001
```

## Managing the cuOpt Server

### Shutting down the cuOpt service(s) temporarily

Login to the server.

To stop the cuOpt service(s)
```bash
$ kubectl scale deployment --all --replicas=0 -n cuopt-server
```

To restart the cuOpt services(s)
```bash
$ kubectl scale deployment --all --replicas=1 -n cuopt-server
```

### Shutting down the cuOpt server

If you are going to shutdown the cuOpt server and restart it at a later date, follow this procedure.

Login to the server.

```bash
kubectl scale deployment --all --replicas=0 -n cuopt-server
Kubectl get pods -n cuopt-server # wait until no pods are reported
```

Now the server may be shutdown.

Login to the server when it is restarted.

```bash
$ scripts/wait-cnc.sh # waits for cloud-native-core to complte restart
$ kubectl scale deployment --all --replicas=1 -n cuopt-server
```

## Troubleshooting

If you cannot connect to the cuOpt services, here are some things to try

### Check the installation logs

Login to the server.

Check the files in the `logs` directory for any reported errors.

In the Cloud Local case, the logs directory will be located in cloud-scripts/cloud-local/logs

### Check localhost connections to cuOpt

Login to the server
```bash
# if you ran the api server
curl -s -o /dev/null -w '%{http_code}\n' localhost:30000/cuopt/docs
200

# if you ran the jupyter server
curl -s -o /dev/null -w '%{http_code}\n' localhost:30001/tree
200
```

If curl returns `200` but you can't connect to the service from another machine, check the firewall rules for the server in the cloud console.

### Check which services were deployed

Login to the build host

The *build-cuopt-server.sh* script will generate a `values.sh` file which includes the server type that was deployed.
```bash
$ cd cloud-scripts/aws # or azure, or gcp
$ more values.sh
cuopt_server_type=api  # This is your server type. 
ip=34.139.78.80
machine=cuopt-fancy-bluebird
private_key_path=~/.ssh/id_rsa
user=tmckay
```

### Check the status of the cuOpt pod

Login to the server

```bash
$ kubectl get pods -n cuopt-server
NAME                                     READY   STATUS    RESTARTS   AGE
cuopt-cuopt-deployment-6887b4769-bbrdm   1/1     Running   0          25m
```

Status should say 'Running'.
If the status is 'ErrImagePull' or 'ImagePullBackoff' then you specified an invalid NGC api-key

There are two ways to repair this:

* Destroy the machine and rerun the build script from the build host with a valid NGC api-key
  ```bash
  $ ../teardown-cuopt-server.sh
  $ ../build-cuopt-server.sh
  ```
  
* Reinstall the cuOpt helm chart locally with a valid NGC api-key
  ```bash
  $ export API_KEY=myvalidapikey
  $ export SERVER_TYPE=both # or jupyter, or api
  $ helm list -n cuopt-server
  NAME              	NAMESPACE   	REVISION	UPDATED                                	STATUS  	CHART        	APP VERSION
  nvidia-cuopt-chart	cuopt-server	1       	2022-09-19 14:11:45.677689124 +0000 UTC	deployed	cuopt-22.08.0	22.08.0
  $ helm uninstall nvidia-cuopt-chart -n cuopt-server
  $ scripts/cuopt-helm.sh
  $ scripts/wait-cuopt.sh
  $ scripts/delete-secret.sh
  ```

### Check the status of cloud-native-core

Login to the server.

```bash
$ kubectl get pods -n kube-system
NAME                                       READY   STATUS    RESTARTS   AGE
calico-kube-controllers-6799f5f4b4-mnt9m   1/1     Running   0          91m
calico-node-fmb8l                          1/1     Running   0          91m
coredns-6d4b75cb6d-56rz2                   1/1     Running   0          90m
coredns-6d4b75cb6d-l6qhl                   1/1     Running   0          90m
etcd-cuopt-local3                          1/1     Running   0          91m
kube-apiserver-cuopt-local3                1/1     Running   0          91m
kube-controller-manager-cuopt-local3       1/1     Running   0          91m
kube-proxy-f445w                           1/1     Running   0          91m
kube-scheduler-cuopt-local3                1/1     Running   0          91m

$ kubectl get pods -n nvidia-gpu-operator
NAME                                                              READY   STATUS      RESTARTS   AGE
gpu-feature-discovery-wjrmw                                       1/1     Running     0          90m
gpu-operator-1663594758-node-feature-discovery-master-6fc72rxrp   1/1     Running     0          91m
gpu-operator-1663594758-node-feature-discovery-worker-x5f5m       1/1     Running     0          90m
gpu-operator-6d7dc7cfc-28r4v                                      1/1     Running     0          91m
nvidia-container-toolkit-daemonset-kmphs                          1/1     Running     0          90m
nvidia-cuda-validator-fv7pb                                       0/1     Completed   0          86m
nvidia-dcgm-exporter-9r7ts                                        1/1     Running     0          90m
nvidia-device-plugin-daemonset-92bxs                              1/1     Running     0          90m
nvidia-device-plugin-validator-sq4p6                              0/1     Completed   0          85m
nvidia-driver-daemonset-bf2sd                                     1/1     Running     0          90m
nvidia-operator-validator-jmbvh                                   1/1     Running     0          90m
```

The output should look similar to the above. If you see pods with error states,
or there appear to be pods missing, cloud-native-core may not have installed properly.

Destroy the machine and rerun the build script from the build host
  ```bash
  $ ../teardown-cuopt-server.sh
  $ ../build-cuopt-server.sh
  ```

For the Cloud Local case, attempt to reinstall.
From the cloud-scripts/cloud-local directory:
```bash
$ cd cloud-native-core/playbooks
$ ./setup.sh uninstall
$ cd ../.. # back to cloud-scripts/cloud-local
$ ./local-build-cuopt-server.sh
```