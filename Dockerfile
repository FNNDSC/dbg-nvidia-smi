# Modern nvidia-container-toolkit does not need CUDA inside the container
# image, however the legacy nvidia-docker needs it.
#
# To build w/o CUDA, run
#
#     docker build --build-arg BASE=python:3.10.2-slim .
#
ARG BASE=docker.io/fnndsc/conda:cuda-fallback
FROM ${BASE}

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="dbg-nvidia-smi" \
      org.opencontainers.image.description="A ChRIS fs plugin wrapper around nvidia-smi"

WORKDIR /usr/local/src/app

COPY . .
RUN pip install --use-feature=in-tree-build .

CMD ["nvidia-smi-wrapper", "--help"]
