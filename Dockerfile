# Official Python image avoids add-apt-repository / Launchpad API (unreachable in some Docker networks)
FROM python:3.11-bookworm

ENV PYTHONUNBUFFERED=1

RUN apt-get update --yes --quiet && \
    DEBIAN_FRONTEND=noninteractive apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /work

COPY ./src /work

ENV OLLAMA_MODELS="/runpod-volume/models"

RUN pip install --no-cache-dir -r requirements.txt && chmod +x /work/start.sh

ENTRYPOINT ["/bin/sh", "-c", "/work/start.sh"]
