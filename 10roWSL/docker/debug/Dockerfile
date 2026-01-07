# Container Debug pentru Laborator
# Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

FROM alpine:3.19

LABEL maintainer="Revolvix"
LABEL description="Container utilitar cu instrumente de rețea"

# Instalează instrumente de rețea
RUN apk add --no-cache \
    bash \
    curl \
    wget \
    bind-tools \
    tcpdump \
    nmap \
    nmap-scripts \
    netcat-openbsd \
    lftp \
    openssh-client \
    iputils \
    iproute2 \
    net-tools \
    busybox-extras \
    jq \
    vim

# Creează directorul de lucru
WORKDIR /home

# Creează fișier cu instrucțiuni
RUN echo "=== Container Debug pentru Laborator ===" > /home/CITESTE.txt && \
    echo "" >> /home/CITESTE.txt && \
    echo "Instrumente disponibile:" >> /home/CITESTE.txt && \
    echo "  - curl: client HTTP/HTTPS" >> /home/CITESTE.txt && \
    echo "  - wget: descărcător de fișiere" >> /home/CITESTE.txt && \
    echo "  - dig: interogări DNS" >> /home/CITESTE.txt && \
    echo "  - nslookup: rezoluție DNS" >> /home/CITESTE.txt && \
    echo "  - tcpdump: captură pachete" >> /home/CITESTE.txt && \
    echo "  - nmap: scanner de porturi" >> /home/CITESTE.txt && \
    echo "  - nc: netcat pentru conexiuni" >> /home/CITESTE.txt && \
    echo "  - lftp: client FTP avansat" >> /home/CITESTE.txt && \
    echo "  - ssh: client SSH" >> /home/CITESTE.txt && \
    echo "  - ping: test conectivitate" >> /home/CITESTE.txt && \
    echo "" >> /home/CITESTE.txt && \
    echo "Exemple:" >> /home/CITESTE.txt && \
    echo "  curl http://web:8000/" >> /home/CITESTE.txt && \
    echo "  dig @dns-server -p 5353 web.lab.local" >> /home/CITESTE.txt && \
    echo "  ssh labuser@ssh-server" >> /home/CITESTE.txt && \
    echo "  lftp -u labftp,labftp ftp-server:2121" >> /home/CITESTE.txt

# Comandă implicită - shell interactiv
CMD ["/bin/bash"]
