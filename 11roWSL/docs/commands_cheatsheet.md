# Fișă de Comenzi Rapide

> Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

> 📚 **Documente înrudite:**
> - [Depanare](./troubleshooting.md) — Soluții probleme comune
> - [Rezumat Teorie](./theory_summary.md) — Concepte fundamentale
> - [Analogii Concepte](./analogii_concepte.md) — Explicații vizuale
> - [Glosar](./glosar.md) — Termeni și definiții

---

## Docker

### Gestionare Containere

```powershell
# Pornește serviciile
docker compose up -d

# Oprește serviciile
docker compose down

# Oprește și elimină volumele
docker compose down -v

# Repornește un serviciu specific
docker compose restart nginx

# Reconstruiește imaginile
docker compose build --no-cache

# Vizualizează containerele active
docker ps

# Vizualizează toate containerele
docker ps -a

# Oprește toate containerele
docker stop $(docker ps -q)
```

### Jurnale și Depanare

```powershell
# Vizualizează jurnalele tuturor serviciilor
docker compose logs

# Jurnale în timp real
docker compose logs -f

# Jurnale pentru un serviciu specific
docker compose logs nginx

# Ultimele 100 linii
docker compose logs --tail=100

# Execută comandă într-un container
docker exec -it s11_nginx_lb /bin/sh

# Inspectează un container
docker inspect s11_nginx_lb
```

### Curățare

```powershell
# Elimină containere oprite
docker container prune

# Elimină imagini nefolosite
docker image prune

# Elimină tot ce nu e folosit
docker system prune -a

# Verifică spațiul folosit
docker system df
```

---

## Rețelistică

### curl

```powershell
# Cerere GET simplă
curl http://localhost:8080/

# Afișează header-ele
curl -i http://localhost:8080/

# Doar header-ele
curl -I http://localhost:8080/

# Afișare verbosă (debug)
curl -v http://localhost:8080/

# Timeout personalizat
curl --connect-timeout 5 http://localhost:8080/

# Multiple cereri
for /L %i in (1,1,10) do @curl -s http://localhost:8080/

# Salvează răspunsul
curl -o raspuns.txt http://localhost:8080/

# Cerere POST cu date JSON
curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' http://localhost:8080/
```

### netstat / ss

```powershell
# Windows - porturi în ascultare
netstat -ano | findstr LISTENING

# Windows - găsește ce folosește un port
netstat -ano | findstr :8080

# Linux - porturi în ascultare
ss -tuln

# Linux - conexiuni stabilite
ss -tn
```

### tcpdump (Linux/WSL)

```bash
# Captură pe o interfață
sudo tcpdump -i eth0

# Captură doar port specific
sudo tcpdump -i eth0 port 8080

# Salvează în fișier
sudo tcpdump -i eth0 -w captura.pcap

# Afișează conținut pachete
sudo tcpdump -i eth0 -A port 8080

# Limitează numărul de pachete
sudo tcpdump -i eth0 -c 100 port 8080
```

### tshark (Wireshark CLI)

```powershell
# Listează interfețele
tshark -D

# Captură pe interfață
tshark -i "Ethernet"

# Captură cu filtru
tshark -i "Ethernet" -f "tcp port 8080"

# Salvează captură
tshark -i "Ethernet" -w captura.pcap

# Analizează fișier existent
tshark -r captura.pcap

# Statistici I/O
tshark -r captura.pcap -q -z io,stat,1
```

---

## DNS

### dig

```bash
# Interogare A record
dig google.com

# Interogare tip specific
dig google.com MX
dig google.com NS
dig google.com AAAA

# Server DNS specific
dig @8.8.8.8 google.com

# Afișare scurtă
dig +short google.com

# Trace complet (iterativ)
dig +trace google.com

# Interogare inversă
dig -x 8.8.8.8
```

### nslookup

```powershell
# Interogare simplă
nslookup google.com

# Server DNS specific
nslookup google.com 8.8.8.8

# Interogare MX
nslookup -type=mx google.com

# Mod interactiv
nslookup
> set type=NS
> google.com
> exit
```

---

## Python

### Scripturi Kit

```powershell
# Verifică mediul
python setup/verify_environment.py

# Pornește laboratorul
python scripts/start_lab.py

# Oprește laboratorul
python scripts/stop_lab.py

# Curățare completă
python scripts/cleanup.py --full

# Rulează demonstrația
python scripts/run_demo.py --all

# Captură trafic
python scripts/capture_traffic.py -i eth0 -d 60

# Teste mediu
python tests/test_environment.py

# Teste exerciții
python tests/test_exercises.py --exercise 1
```

### Exerciții

```powershell
# Backend-uri
python src/exercises/ex_11_01_backend.py --id 1 --port 8081 -v
python src/exercises/ex_11_01_backend.py --id 2 --port 8082 -v
python src/exercises/ex_11_01_backend.py --id 3 --port 8083 -v

# Echilibror - Round Robin
python src/exercises/ex_11_02_loadbalancer.py --backends localhost:8081,localhost:8082,localhost:8083 --algo rr

# Echilibror - IP Hash
python src/exercises/ex_11_02_loadbalancer.py --backends localhost:8081,localhost:8082,localhost:8083 --algo ip_hash

# Generator sarcină
python src/exercises/ex_11_02_loadbalancer.py loadgen --url http://localhost:8080/ --n 100 --c 10

# Client DNS
python src/exercises/ex_11_03_dns_client.py google.com A --verbose
python src/exercises/ex_11_03_dns_client.py google.com MX
```

---

## Wireshark - Filtre de Afișare

### HTTP

```
# Tot traficul HTTP
http

# Doar cereri
http.request

# Doar răspunsuri
http.response

# Metode specifice
http.request.method == "GET"
http.request.method == "POST"

# Cod status
http.response.code == 200
http.response.code >= 400

# URI specific
http.request.uri contains "health"

# Host specific
http.host == "localhost"
```

### DNS

```
# Tot traficul DNS
dns

# Doar interogări
dns.flags.response == 0

# Doar răspunsuri
dns.flags.response == 1

# Tip înregistrare
dns.qry.type == 1    # A
dns.qry.type == 28   # AAAA
dns.qry.type == 15   # MX

# Nume specific
dns.qry.name contains "google"
```

### TCP

```
# Port specific
tcp.port == 8080

# Port sursă sau destinație
tcp.srcport == 8080
tcp.dstport == 80

# Flags TCP
tcp.flags.syn == 1
tcp.flags.fin == 1
tcp.flags.rst == 1

# Conversație specifică
tcp.stream eq 5
```

### Generale

```
# Adresă IP
ip.addr == 192.168.1.1
ip.src == 192.168.1.1
ip.dst == 192.168.1.1

# Exclude trafic
!(ip.addr == 192.168.1.1)
not arp

# Combinații
http and ip.addr == 192.168.1.1
tcp.port == 8080 && http.request
```

---

## Scurtături Utile

### PowerShell

```powershell
# Oprește procesul pe un port
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8080).OwningProcess -Force

# Găsește procesul pe un port
Get-Process -Id (Get-NetTCPConnection -LocalPort 8080).OwningProcess
```

### Linux/WSL

```bash
# Oprește procesul pe un port
kill $(lsof -t -i:8080)

# Găsește procesul pe un port
lsof -i :8080
```

---

## Navigare Rapidă

- [← Înapoi la README](../README.md)
- [Depanare →](./troubleshooting.md)
- [Rezumat Teorie →](./theory_summary.md)
- [Glosar →](./glosar.md)

---

*Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix*
