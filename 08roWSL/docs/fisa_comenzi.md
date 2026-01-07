# Fișă de Comenzi Rapide

> Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

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

# Executare comandă în container
docker exec -it <nume_container> bash
docker exec -it <nume_container> sh
```

### Docker Compose

```bash
# Pornire servicii
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
docker exec week8-backend1-1 ping week8-nginx-1
```

## Testare HTTP cu curl

### Cereri de Bază

```bash
# Cerere GET simplă
curl http://localhost:8080/

# Afișare antete răspuns
curl -i http://localhost:8080/

# Doar antetele (HEAD)
curl -I http://localhost:8080/

# Afișare detalii verbose
curl -v http://localhost:8080/
```

### Testare Echilibrare

```bash
# Testare round-robin (6 cereri)
for i in {1..6}; do 
    curl -s http://localhost:8080/ | grep -o 'Backend [0-9]'
done

# Cu afișare antet backend
for i in {1..6}; do
    curl -sI http://localhost:8080/ | grep X-Backend
done

# Testare weighted
for i in {1..18}; do
    curl -sI http://localhost:8080/weighted/ | grep X-Backend-ID
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

## Captură Trafic

### tcpdump

```bash
# Captură pe interfața loopback
sudo tcpdump -i lo port 8080

# Salvare în fișier
sudo tcpdump -i lo port 8080 -w captura.pcap

# Doar primele 100 pachete
sudo tcpdump -i lo port 8080 -c 100

# Afișare conținut pachet
sudo tcpdump -i lo port 8080 -A

# Afișare în hex și ASCII
sudo tcpdump -i lo port 8080 -X
```

### Filtre Wireshark

```
# Trafic HTTP
http

# Port specific
tcp.port == 8080

# Cereri HTTP
http.request

# Răspunsuri HTTP
http.response

# Handshake TCP
tcp.flags.syn == 1

# Backend specific
ip.addr == 172.28.8.21

# Urmărire flux TCP
tcp.stream eq 0

# Metoda GET
http.request.method == "GET"

# Cod stare 200
http.response.code == 200
```

## Instrumente Python HTTP

```python
# Server HTTP simplu
python -m http.server 8888

# Server HTTP în director specific
python -m http.server 8888 --directory www/

# Legare la interfață specifică
python -m http.server 8888 --bind 127.0.0.1
```

## Diagnosticare Rețea

### Conectivitate

```bash
# Verificare port deschis
nc -zv localhost 8080

# Scanare porturi
nmap localhost -p 8080-8090

# Testare DNS
nslookup localhost
dig localhost
```

### Analiza Jurnale

```bash
# Jurnale nginx
docker logs week8-nginx-1

# Jurnale cu timestamp
docker logs -t week8-nginx-1

# Ultimele 50 linii
docker logs --tail 50 week8-nginx-1

# Doar erori
docker logs week8-nginx-1 2>&1 | grep -i error
```

## Tabel Referință Rapidă

| Acțiune | Comandă |
|---------|---------|
| Pornire laborator | `python scripts/porneste_laborator.py` |
| Oprire laborator | `python scripts/opreste_laborator.py` |
| Curățare completă | `python scripts/curatare.py --complet` |
| Test rapid | `python tests/test_rapid.py` |
| Demo round-robin | `python scripts/ruleaza_demo.py --demo docker-nginx` |
| Verificare mediu | `python setup/verifica_mediu.py` |
| Jurnale nginx | `docker logs week8-nginx-1` |
| Stare containere | `docker compose ps` |
| Captură trafic | `python scripts/captureaza_trafic.py --wireshark` |

---

*Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
