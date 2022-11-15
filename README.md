# Detect Nvidia GPUs in a Container

[![Version](https://img.shields.io/docker/v/fnndsc/dbg-nvidia-smi?sort=semver)](https://hub.docker.com/r/fnndsc/dbg-nvidia-smi)
[![MIT License](https://img.shields.io/github/license/fnndsc/dbg-nvidia-smi)](https://github.com/FNNDSC/dbg-nvidia-smi/blob/main/LICENSE)
[![Build](https://github.com/FNNDSC/dbg-nvidia-smi/actions/workflows/build.yml/badge.svg)](https://github.com/FNNDSC/dbg-nvidia-smi/actions)

`dbg-nvidia-smi` is a _ChRIS_ fs plugin wrapper around the command `nvidia-smi`, thus it requires an output positional directory argument. The plugin is useful to probe/test for available GPU(s) on a given host or ChRIS compute environment.

## Usage

```shell

# To get detailed usage/man page instruction, pass a
# --man argument to the 'nvidia-smi-wrapper' in the
# examples below.

# Apptainer
singularity exec --nv docker://ghcr.io/fnndsc/dbg-nvidia-smi:lite \
    sh -c 'nvidia-smi-wrapper /tmp --cat'

# Typical Docker
docker run --rm --gpus all ghcr.io/fnndsc/dbg-nvidia-smi:lite \
    sh -c 'nvidia-smi-wrapper /tmp --cat'

# RHEL with SELinux
# Note: cannot use :lite image, must use :cuda image
podman run --rm --security-opt=no-new-privileges --cap-drop=ALL \
    --security-opt label=type:nvidia_container_t \
    ghcr.io/fnndsc/dbg-nvidia-smi:cuda \
    sh -c 'nvidia-smi-wrapper /tmp --cat'
```
