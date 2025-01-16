# ERROR: failed to create cluster

- ERROR: failed to create cluster: command "docker run --name kind-control-plane --hostname kind-control-plane --label io.x-k8s.kind.role=control-plane --privileged --security-opt seccomp=unconfined --security-opt apparmor=unconfined --tmpfs /tmp --tmpfs /run --volume /var --volume /lib/modules:/lib/modules:ro -e KIND_EXPERIMENTAL_CONTAINERD_SNAPSHOTTER --detach --tty --label io.x-k8s.kind.cluster=kind --net kind --restart=on-failure:1 --init=false --cgroupns=private --publish=0.0.0.0:80:80/TCP --publish=0.0.0.0:443:443/TCP --publish=127.0.0.1:38803:6443/TCP -e KUBECONFIG=/etc/kubernetes/admin.conf kindest/node:v1.31.0@sha256:53df588e04085fd41ae12de0c3fe4c72f7013bba32a20e7325357a1ac94ba865" failed with error: exit status 125
  Command Output: 482e077cbfca9e300e6a8cd7ba1779a5ae4b502d4eb2d98b390af2da7d503366
  docker: Error response from daemon: driver failed programming external connectivity on endpoint kind-control-plane (ea2b72af96a880c2cc1f8e6f07976b106cc7e82f2f6f220edadf8c0d5796f1a6): failed to bind port 0.0.0.0:80/tcp: Error starting userland proxy: listen tcp4 0.0.0.0:80: bind: address already in use.

## debug

The error message indicates that there was an issue creating the kind cluster. This can happen for several reasons, such as Docker not running, insufficient resources, or network issues. Here are some steps to troubleshoot and resolve the issue:

1. Ensure Docker is Running
   Make sure Docker is running on your machine:

￼
sudo systemctl start docker 2. Check Docker Version
Ensure you have a compatible version of Docker installed:

￼
docker --version 3. Check Docker Resources
Ensure Docker has enough resources allocated (CPU, memory, disk space). You can adjust these settings in Docker Desktop or Docker Engine configuration.

4. Clean Up Existing Containers
   Remove any existing kind containers that might be causing conflicts:

￼
docker ps -a | grep kinddocker rm -f $(docker ps -a | grep kind | awk '{print $1}')

5. Create the kind Cluster
   Try creating the kind cluster again:

￼
kind create cluster
If you are using a custom configuration file, ensure it is correctly formatted and try again:

kind create cluster --config kubernetes/kind-config.yaml

6. Check Docker Logs
   If the issue persists, check the Docker logs for more details:

￼
docker logs kind-control-plane

# lite debug kubectl

1. Check Pod Status
   Check the status of the pods to get more details:

```
kubectl get pods
```

1. 1. Check All Namespaces

```
kubectl get pods --all-namespaces
```

2. Describe the Pod
   Describe the pod to get more information about why it is in a Pending state:

```
kubectl describe pod <pod-name>
```

Look for events at the bottom of the output to see if there are any errors or warnings.

2. 1. Check Logs
      Check the logs of the pod to see if there are any errors:

￼kubectl logs <pod-name>

```

￼kubectl logs fastapi-7447b65c7-f8z9m
```

3. Verify Deployment
   Ensure that the fastapi deployment is correctly applied and running:

```

kubectl get deployments
kubectl describe deployment fastapi
```
