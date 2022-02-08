# Detect Nvidia GPUs in a Container

[![Version](https://img.shields.io/docker/v/fnndsc/dbg-nvidia-smi?sort=semver)](https://hub.docker.com/r/fnndsc/dbg-nvidia-smi)
[![MIT License](https://img.shields.io/github/license/fnndsc/dbg-nvidia-smi)](https://github.com/FNNDSC/dbg-nvidia-smi/blob/main/LICENSE)
[![Build](https://github.com/FNNDSC/dbg-nvidia-smi/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/dbg-nvidia-smi/actions)

`dbg-nvidia-smi` is a _ChRIS_ fs plugin wrapper around the command `nvidia-smi`.

## Usage

```shell
# Apptainer
singularity exec --nv docker://ghcr.io/fnndsc/dbg-nvidia-smi:lite \
    sh -c 'nvidia-smi-wrapper /tmp && cat /tmp/gpus.csv'

# Typical Docker
docker run --rm --gpus all ghcr.io/fnndsc/dbg-nvidia-smi:lite \
    sh -c 'nvidia-smi-wrapper /tmp && cat /tmp/gpus.csv'

# RHEL with SELinux
# Note: cannot use :lite image, must use :cuda image
podman run --rm --security-opt=no-new-privileges --cap-drop=ALL \
    --security-opt label=type:nvidia_container_t \
    ghcr.io/fnndsc/dbg-nvidia-smi:cuda \
    sh -c 'nvidia-smi-wrapper /tmp && cat /tmp/gpus.csv'
```
