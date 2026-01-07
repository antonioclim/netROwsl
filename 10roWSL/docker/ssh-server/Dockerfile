# Server SSH pentru Laborator
# Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

FROM alpine:3.19

LABEL maintainer="Revolvix"
LABEL description="Server SSH pentru demonstrații de laborator"

# Instalează OpenSSH și utilitare
RUN apk add --no-cache \
    openssh \
    bash \
    netcat-openbsd

# Creează utilizatorul de laborator
RUN adduser -D -s /bin/bash labuser && \
    echo "labuser:labpass" | chpasswd

# Configurează SSH
RUN ssh-keygen -A && \
    sed -i 's/#PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config

# Creează directorul pentru date
RUN mkdir -p /home/labuser && \
    chown -R labuser:labuser /home/labuser

# Creează fișiere demo pentru utilizator
RUN echo "Bine ați venit pe serverul SSH de laborator!" > /home/labuser/bun_venit.txt && \
    echo "Acest fișier poate fi citit prin SSH." > /home/labuser/exemplu.txt && \
    chown labuser:labuser /home/labuser/*.txt

# Expune portul SSH
EXPOSE 22

# Pornește serverul SSH
CMD ["/usr/sbin/sshd", "-D", "-e"]
