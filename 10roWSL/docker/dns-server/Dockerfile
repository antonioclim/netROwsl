# Dockerfile pentru Serverul DNS
# Laborator Rețele de Calculatoare - ASE | by Revolvix
#
# Server DNS personalizat folosind biblioteca dnslib din Python

FROM python:3.11-alpine

# Metadate imagine
LABEL maintainer="Laborator Retele - ASE"
LABEL description="Server DNS personalizat pentru laborator"

# Instalează dnslib
RUN pip install --no-cache-dir dnslib

# Directorul de lucru
WORKDIR /app

# Copiază scriptul serverului DNS
COPY server_dns.py /app/

# Expune portul DNS (UDP)
EXPOSE 5353/udp

# Pornește serverul
CMD ["python", "-u", "server_dns.py"]
