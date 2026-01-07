# ==============================================================================
# Dockerfile - Kit Laborator Săptămâna 4
# Mediu de Dezvoltare pentru Protocoale TCP/UDP Personalizate
# ==============================================================================
# Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix
#
# Scop:
# - Oferă un container minimal și reproductibil pentru dezvoltarea protocoalelor
# - Suportă servere pentru protocoale TEXT, BINAR (TCP) și senzor UDP
# - Permite capturarea și analiza pachetelor în interiorul containerului
#
# Utilizare:
#   docker build -t laborator_s4 .
#   docker run -p 5400:5400 -p 5401:5401 -p 5402:5402/udp laborator_s4
# ==============================================================================

FROM python:3.11-slim

# Etichete
LABEL maintainer="ASE CSIE - Rețele de Calculatoare"
LABEL description="Laborator Săptămâna 4 - Dezvoltare Protocoale Personalizate"
LABEL version="1.0.0"

# Setare director de lucru
WORKDIR /app

# Instalare instrumente minimale pentru inspecția rețelei
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       iproute2 \
       iputils-ping \
       netcat-openbsd \
       procps \
       tcpdump \
       tshark \
       curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiere cod aplicație
COPY src/ /app/src/
COPY scripts/ /app/scripts/
COPY tests/ /app/tests/

# Asigurare că scripturile sunt executabile
RUN chmod +x /app/scripts/*.py /app/tests/*.py 2>/dev/null || true

# Creare utilizator non-root pentru securitate
RUN useradd -m -u 1000 -s /bin/bash utilizator_retea \
    && mkdir -p /app/artifacts /app/pcap \
    && chown -R utilizator_retea:utilizator_retea /app

# Permite capturarea pachetelor pentru utilizator non-root
RUN setcap cap_net_raw,cap_net_admin+eip /usr/bin/tcpdump 2>/dev/null || true

# Comutare la utilizator non-root
USER utilizator_retea

# Variabile de mediu
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/home/utilizator_retea/.local/bin:${PATH}"

# Porturi implicite Săptămâna 4
EXPOSE 5400/tcp
EXPOSE 5401/tcp
EXPOSE 5402/udp

# Verificare stare - verifică dacă serverul TEXT răspunde
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import socket; s=socket.socket(); s.settimeout(2); s.connect(('localhost',5400)); s.close()" || exit 1

# Comandă implicită - pornire server protocol TEXT
CMD ["python3", "-u", "src/apps/text_proto_server.py", "--port", "5400"]
