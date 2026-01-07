# Dockerfile pentru Laborator Săptămâna 5
# Rețele de Calculatoare – ASE, Informatică Economică
# realizat de Revolvix
#
# Imagine de bază Python cu instrumente de rețea pentru exerciții
# de adresare IPv4/IPv6 și analiză de pachete.

FROM python:3.11-slim

# Metadate
LABEL maintainer="Laborator Rețele - ASE"
LABEL description="Container Python pentru exerciții de adresare IP"
LABEL week="5"

# Variabile de mediu pentru Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalare instrumente de rețea necesare
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Instrumente de rețea de bază
    iputils-ping \
    iproute2 \
    net-tools \
    dnsutils \
    # Captură și analiză pachete
    tcpdump \
    # Client/server TCP/UDP
    netcat-openbsd \
    # Utilitar pentru testare HTTP
    curl \
    # Editor de text simplu
    nano \
    # Curățare cache apt
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Instalare biblioteci Python pentru rețele
RUN pip install --no-cache-dir \
    ipaddress \
    requests \
    scapy

# Crearea directorului de lucru
WORKDIR /app

# Crearea directorului pentru capturi
RUN mkdir -p /app/pcap /app/artifacts

# Setare utilizator non-root pentru securitate
# (comentat pentru a permite captură de pachete)
# RUN useradd -m student
# USER student

# Comandă implicită - menține containerul activ
CMD ["sleep", "infinity"]
