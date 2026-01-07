# Server FTP pentru Laborator
# Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

FROM python:3.11-alpine

LABEL maintainer="Revolvix"
LABEL description="Server FTP folosind pyftpdlib"

# Instalează dependențele
RUN apk add --no-cache netcat-openbsd && \
    pip install --no-cache-dir pyftpdlib

# Creează utilizatorul FTP
RUN adduser -D -s /bin/sh labftp

# Creează directorul de date
RUN mkdir -p /home/labftp/upload /home/labftp/download && \
    echo "Fișier de test pentru descărcare FTP" > /home/labftp/download/test.txt && \
    echo "Bine ați venit pe serverul FTP!" > /home/labftp/bun_venit.txt && \
    chown -R labftp:labftp /home/labftp

# Creează directorul aplicației
WORKDIR /app

# Copiază scriptul serverului
COPY ftp_server.py /app/

# Expune porturile
EXPOSE 2121
EXPOSE 30000-30009

# Rulează serverul
CMD ["python", "ftp_server.py"]
