# A simple example of a MLOps pipeline

## Setup

Install the conda environment with:
```
conda env create -f etc/environment.yml
```
Then activate the environment with:
```
conda activate imdb
```

## Execution


### Configure DVC

```
dvc init
```

### Model training

```python
python src/prepare_data.py
```
Then:
```
dvc add <path_to_data>
```
Then
```
python src/train_model.py
```

## Kubernetes integration

### Description

* Minikube enables running Kubernetes locally for development, testing, and learning purposes.
* It sets up a single-node Kubernetes cluster on the local system.
* Useful for developers who want to test applications in a Kubernetes environment without a full-scale cluster.
* Minikube creates a virtual machine using platforms like VirtualBox, VMware, or Hyper-V.
* Within the virtual machine, it installs a lightweight Linux distribution like Boot2Docker or LinuxKit.
* Minikube deploys and configures Kubernetes components such as the API server, controller manager, scheduler, and etcd inside the virtual environment.


The following installation is taken from https://minikube.sigs.k8s.io/docs/start/

### Minikube installation

```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
```
Then:
```
sudo dpkg -i minikube_latest_amd64.deb
```
If this is not already the case, add your user to the docker group with:
```
sudo usermod -aG docker $USER && newgrp docker
```
Finally:
```
minikube start
```


If kubectl is not installed, please follow the next step. First:
```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```
Then:
```
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```
Check the version with:
```
kubectl version --client --output=yaml
```

Now, you can explore the cluster with:
```
kubectl get po -A
```

To monitor and explore the cluster, you can use the dashboard with:
```
minikube dashboard
```


Minikube has its own Docker daemon running inside the VM. To make the Docker image available to Minikube, we need to run:
```
eval $(minikube docker-env)
```


Build the docker image
```
docker build -t imdb-image -f Dockerfile.api .
```