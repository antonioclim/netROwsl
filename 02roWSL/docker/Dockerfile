# Dockerfile pentru Laboratorul Săptămânii 2
# Laborator Rețele de Calculatoare - ASE, Informatică Economică
# by Revolvix
#
# Imagine bazată pe Python 3.11 cu instrumente de rețea

# Imagine de bază: Python 3.11 slim pe Debian Bookworm
FROM python:3.11-slim-bookworm

# Metadate imagine
LABEL maintainer="Revolvix"
LABEL description="Container pentru laboratorul de programare socket TCP/UDP"
LABEL version="1.0"

# Variabile de mediu
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=Europe/Bucharest

# Setare fus orar
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Instalare instrumente de rețea și utilități
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Instrumente de captură pachete
    tcpdump \
    tshark \
    # Utilități de rețea
    netcat-openbsd \
    iproute2 \
    iputils-ping \
    dnsutils \
    net-tools \
    curl \
    wget \
    # Instrumente de diagnostic
    procps \
    lsof \
    # Curățare cache apt
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Creare utilizator non-root pentru securitate
RUN groupadd -r student && useradd -r -g student -d /home/student -s /bin/bash -m student

# Creare directoare de lucru
RUN mkdir -p /app/exercises /app/pcap /app/artifacts \
    && chown -R student:student /app

# Setare director de lucru
WORKDIR /app

# Comutare la utilizatorul non-root
# Notă: Comentat pentru a permite tcpdump (necesită root sau capabilități)
# USER student

# Expunere porturi
# 9090 - Server TCP
# 9091 - Server UDP
EXPOSE 9090 9091/udp

# Comandă implicită: shell interactiv
CMD ["/bin/bash"]

# Alternativ: pornire directă a unui server
# CMD ["python", "/app/exercises/ex_2_01_tcp.py", "server"]
