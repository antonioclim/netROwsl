# Dockerfile pentru Laboratorul Săptămânii 12
# Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix
#
# Imagine de bază pentru serverele SMTP, JSON-RPC, XML-RPC și gRPC

FROM python:3.12-slim

# Metadate
LABEL maintainer="Revolvix"
LABEL description="Container de laborator pentru protocoale email și RPC"
LABEL week="12"
LABEL course="Rețele de Calculatoare - ASE"

# Setare variabile de mediu
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Instalare instrumente de sistem
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Instrumente de rețea
    curl \
    netcat-openbsd \
    tcpdump \
    tshark \
    dnsutils \
    iputils-ping \
    iproute2 \
    # Utilitare generale
    vim-tiny \
    less \
    procps \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Creare utilizator non-root pentru securitate
RUN useradd -m -s /bin/bash labuser

# Instalare dependențe Python
COPY setup/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Creare structură directoare
WORKDIR /app
RUN mkdir -p /app/src /app/spool /app/pcap /app/logs \
    && chown -R labuser:labuser /app

# Expunere porturi
# 1025 - SMTP
# 6200 - JSON-RPC
# 6201 - XML-RPC
# 6251 - gRPC
EXPOSE 1025 6200 6201 6251

# Director de lucru
WORKDIR /app/src

# Comandă implicită (suprascrisă de docker-compose)
CMD ["bash"]
