# Dockerfile pentru Laboratorul Săptămânii 3
# Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix
#
# Imagine de bază pentru containerele de laborator cu instrumente de rețea.

FROM ubuntu:22.04

# Previne prompturile interactive în timpul instalării
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Actualizează sistemul și instalează dependențele
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Python și pip
    python3 \
    python3-pip \
    python3-dev \
    # Instrumente de rețea esențiale
    iputils-ping \
    iproute2 \
    net-tools \
    netcat-openbsd \
    curl \
    wget \
    dnsutils \
    traceroute \
    # Instrumente de captură și analiză
    tcpdump \
    tshark \
    # Instrumente de testare performanță
    iperf3 \
    hping3 \
    # Utilitare generale
    vim \
    nano \
    less \
    procps \
    # Dependențe pentru compilare (dacă este necesar)
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalează pachetele Python necesare
RUN pip3 install --no-cache-dir \
    scapy \
    requests \
    pyyaml

# Creează directorul de lucru
WORKDIR /app

# Creează utilizator non-root (opțional, pentru securitate)
# RUN useradd -m -s /bin/bash student && chown -R student:student /app
# USER student

# Expune porturile utilizate frecvent
EXPOSE 5007/udp 5008/udp 8080 9090

# Comandă implicită - poate fi suprascrisă în docker-compose
CMD ["bash"]
