# Modern nvidia-container-toolkit does not need CUDA inside the container
# image, however the legacy nvidia-docker needs it.
#
# To build w/o CUDA, run
#
#     docker build --build-arg BASE=python:3.10.2-slim .
#
ARG BASE=docker.io/fnndsc/conda:python3.10.5-cuda11.6.0
FROM ${BASE}

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="dbg-nvidia-smi" \
      org.opencontainers.image.description="A ChRIS fs plugin wrapper around nvidia-smi"

WORKDIR /usr/local/src/dbg-nvidia-smi

COPY . .
RUN pip install .

CMD ["nvidia-smi-wrapper", "--man", "/tmp"]
