# Client SSH cu Paramiko pentru Laborator
# Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

FROM python:3.11-alpine

LABEL maintainer="Revolvix"
LABEL description="Client SSH cu Paramiko pentru demonstrații"

# Instalează dependențele de sistem
RUN apk add --no-cache \
    openssh-client \
    bash

# Instalează Paramiko
RUN pip install --no-cache-dir paramiko

# Creează directorul aplicației
WORKDIR /app

# Copiază scriptul clientului
COPY paramiko_client.py /app/

# Comandă implicită
CMD ["python", "paramiko_client.py"]
