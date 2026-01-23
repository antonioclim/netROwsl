# Fișă de Comenzi Rapide — Săptămâna 8

> Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix
>
> **Vezi și:** [README principal](../README.md) | [Rezumat teoretic](rezumat_teoretic.md) | [Depanare](depanare.md)

---

## ⚡ Comenzi Esențiale (Top 10)

| # | Acțiune | Comandă |
|---|---------|---------|
| 1 | Pornire Docker | `sudo service docker start` |
| 2 | Pornire laborator | `python3 scripts/porneste_laborator.py` |
| 3 | Verificare containere | `docker ps` |
| 4 | Test HTTP | `curl -i http://localhost:8080/` |
| 5 | Test round-robin | `for i in {1..6}; do curl -s http://localhost:8080/ \| grep Backend; done` |
| 6 | Jurnale nginx | `docker logs week8-nginx-proxy` |
| 7 | Oprire laborator | `python3 scripts/opreste_laborator.py` |
| 8 | Acces Portainer | http://localhost:9000 (stud/studstudstud) |
| 9 | Wireshark filtre | `http` sau `tcp.port == 8080` |
| 10 | Curățare | `python3 scripts/curatare.py --complet` |

---

## Comenzi Docker

### Gestionare Containere

```bash
# Listare containere active
docker ps

# Listare toate containerele (inclusiv oprite)
docker ps -a

# Oprire container
docker stop <nume_container>

# Pornire container
docker start <nume_container>

# Repornire container
docker restart <nume_container>

# Vizualizare jurnale
docker logs <nume_container>
docker logs -f <nume_container>  # Urmărire în timp real
docker logs --tail 50 <nume_container>  # Ultimele 50 linii

# Executare comandă în container
docker exec -it <nume_container> bash
docker exec -it <nume_container> sh
```

### Docker Compose

```bash
# Pornire servicii (în background)
docker compose up -d

# Oprire servicii
docker compose down

# Oprire și eliminare volume
docker compose down -v

# Reconstruire imagini
docker compose build --no-cache

# Vizualizare stare servicii
docker compose ps

# Vizualizare jurnale toate serviciile
docker compose logs

# Vizualizare jurnale serviciu specific
docker compose logs nginx
docker compose logs backend1
```

### Rețele Docker

```bash
# Listare rețele
docker network ls

# Inspectare rețea
docker network inspect week8-laboratory-network

# Testare conectivitate între containere
docker exec week8-nginx-proxy ping backend1
```

---

## Testare HTTP cu curl

### Cereri de Bază

```bash
# Cerere GET simplă
curl http://localhost:8080/

# Afișare antete răspuns (-i = include headers)
curl -i http://localhost:8080/

# Doar antetele (HEAD)
curl -I http://localhost:8080/

# Afișare detalii verbose
curl -v http://localhost:8080/
```

### 🔮 Predicții pentru Testare

**Înainte de a rula:** Ce cod HTTP aștepți? Ce antete vor fi prezente?

### Testare Echilibrare

```bash
# Testare round-robin (6 cereri)
for i in {1..6}; do 
    echo "Cerere $i:"
    curl -s http://localhost:8080/ | grep -o 'Backend-[A-Za-z]*'
done

# Cu afișare antet backend
for i in {1..6}; do
    curl -sI http://localhost:8080/ | grep X-Backend
done

# Testare weighted (numărare distribuție)
for i in {1..18}; do
    curl -sI http://localhost:8080/ | grep X-Backend-ID
done | sort | uniq -c
```

### Testare Endpoint-uri

```bash
# Verificare sănătate nginx
curl http://localhost:8080/nginx-health

# Verificare sănătate backend
curl http://localhost:8080/health

# API status JSON
curl http://localhost:8080/api/status.json

# Cu formatare JSON (necesită jq)
curl -s http://localhost:8080/api/status.json | jq .
```

---

## Captură Trafic

### tcpdump (în WSL)

```bash
# Captură pe interfața eth0
sudo tcpdump -i eth0 port 8080

# Salvare în fișier
sudo tcpdump -i eth0 port 8080 -w pcap/captura.pcap

# Doar primele 100 pachete
sudo tcpdump -i eth0 port 8080 -c 100

# Afișare conținut pachet (ASCII)
sudo tcpdump -i eth0 port 8080 -A

# Afișare în hex și ASCII
sudo tcpdump -i eth0 port 8080 -X
```

### Filtre Wireshark (Referință Rapidă)

| Filtru | Scop |
|--------|------|
| `http` | Tot traficul HTTP |
| `tcp.port == 8080` | Port specific |
| `http.request` | Doar cereri HTTP |
| `http.response` | Doar răspunsuri HTTP |
| `tcp.flags.syn == 1` | Pachete SYN (handshake) |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | Doar SYN inițial |
| `tcp.flags.syn == 1 && tcp.flags.ack == 1` | SYN-ACK |
| `ip.addr == 172.28.8.21` | Backend specific |
| `http.request.method == "GET"` | Metoda GET |
| `http.response.code == 200` | Cod stare 200 |
| `http.response.code >= 400` | Erori HTTP |

### Combinare Filtre

```
# ȘI logic
http && tcp.port == 8080

# SAU logic  
tcp.port == 8080 || tcp.port == 8443

# NEGARE
!arp && !dns

# Urmărire flux TCP specific
tcp.stream eq 0
```

---

## Instrumente Python HTTP

```bash
# Server HTTP simplu
python3 -m http.server 8888

# Server HTTP în director specific
python3 -m http.server 8888 --directory www/

# Legare la interfață specifică
python3 -m http.server 8888 --bind 127.0.0.1
```

---

## Diagnosticare Rețea

### Conectivitate

```bash
# Verificare port deschis
nc -zv localhost 8080

# Verificare ce proces folosește un port
sudo ss -tlnp | grep 8080

# Testare DNS în container
docker exec week8-nginx-proxy nslookup backend1
```

### Analiza Jurnale

```bash
# Jurnale nginx
docker logs week8-nginx-proxy

# Jurnale cu timestamp
docker logs -t week8-nginx-proxy

# Ultimele 50 linii
docker logs --tail 50 week8-nginx-proxy

# Doar erori
docker logs week8-nginx-proxy 2>&1 | grep -i error

# Urmărire în timp real
docker logs -f week8-nginx-proxy
```

---

## Tabel Referință Rapidă Scripturi

| Acțiune | Comandă |
|---------|---------|
| Pornire laborator | `python3 scripts/porneste_laborator.py` |
| Oprire laborator | `python3 scripts/opreste_laborator.py` |
| Curățare completă | `python3 scripts/curatare.py --complet` |
| Test rapid | `python3 tests/test_rapid.py` |
| Demo round-robin | `python3 scripts/ruleaza_demo.py --demo docker-nginx` |
| Demo echilibrare | `python3 scripts/ruleaza_demo.py --demo echilibrare` |
| Demo handshake | `python3 scripts/ruleaza_demo.py --demo handshake` |
| Verificare mediu | `python3 setup/verifica_mediu.py` |
| Captură trafic | `python3 scripts/captureaza_trafic.py` |
| Stare servicii | `python3 scripts/porneste_laborator.py --status` |

---

## Credențiale Standard

| Serviciu | Utilizator | Parolă |
|----------|------------|--------|
| Ubuntu WSL | `stud` | `stud` |
| Portainer | `stud` | `studstudstud` |

## Porturi Standard

| Port | Serviciu |
|------|----------|
| 8080 | nginx HTTP |
| 8443 | nginx HTTPS |
| 9000 | Portainer (⚠️ REZERVAT) |
| 8888 | Server exercițiu 1 |
| 8001-8003 | Backend-uri exercițiu 2 |

---

*Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
