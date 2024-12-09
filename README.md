# k8_lab

En första lab med k8

# Dockument

- [Kubeshark](https://www.kubeshark.co/)
- [Container storage](/document/Container_storage.md)
- [Setup dockerhub](/document/Setup_dockerhub.md)
- [Struktur](/document/Struktur.md)
- [Kladd](/document/Kladd_for_code.md)

# Passords hantering

```
echo -n "ditt-lösenord" | base64

echo -n "postgres" | base64
echo -n "password" | base64

```

# Check yaml files

- [Yaml check Linux](https://github.com/mikefarah/yq)

## install on Linux

```
sudo wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /usr/bin/yq &&\
    sudo chmod +x /usr/bin/yq
```

## validate on linux

```
yq -v kubernetes/postgres.yaml

```
