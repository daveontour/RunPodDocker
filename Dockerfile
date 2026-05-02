# Add the base image
FROM ubuntu:22.04

ENV PYTHONUNBUFFERED=1

# Set up the working directory
WORKDIR /

# Consolidated and corrected RUN command
RUN apt-get update --yes --quiet && \
    DEBIAN_FRONTEND=noninteractive apt-get install --yes --quiet --no-install-recommends \
    software-properties-common \
    gpg-agent \
    build-essential \
    apt-utils \
    ca-certificates \
    curl \
    bash && \
    add-apt-repository --yes ppa:deadsnakes/ppa && \
    apt-get update --yes --quiet && \
    DEBIAN_FRONTEND=noninteractive apt-get install --yes --quiet --no-install-recommends \
    python3.11 \
    python3.11-dev \
    python3.11-distutils \
    python3.11-lib2to3 \
    python3.11-gdbm \
    python3.11-tk && \
    ln -sf /usr/bin/python3.11 /usr/bin/python && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /work

# Add my src as /work
ADD ./src /work

# Set default ollama models directory to /runpod-volume where runpod will mount the volume by default
ENV OLLAMA_MODELS="/runpod-volume/models"

# Install runpod and its dependencies
RUN pip install -r requirements.txt && chmod +x /work/start.sh
    
# Set the entrypoint
ENTRYPOINT ["/bin/sh", "-c", "/work/start.sh"]