# Comenzi Rapide - Săptămâna 7

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

## Managementul Laboratorului

### Pornire și Oprire

```powershell
# Pornire mediu de laborator
python scripts/porneste_lab.py

# Verificare status
python scripts/porneste_lab.py --status

# Pornire cu serviciul proxy
python scripts/porneste_lab.py --proxy

# Oprire mediu
python scripts/opreste_lab.py

# Curățare completă
python scripts/curata.py --complet
```

### Verificări

```powershell
# Verificare mediu
python setup/verifica_mediu.py

# Test rapid
python tests/test_rapid.py

# Teste exerciții
python tests/test_exercitii.py
python tests/test_exercitii.py --exercitiu 1
```

---

## Comenzi Docker

### Containere

```powershell
# Listare containere active
docker ps

# Listare toate containerele (inclusiv oprite)
docker ps -a

# Loguri container
docker logs week7_server_tcp
docker logs week7_receptor_udp
docker logs -f week7_server_tcp  # urmărire în timp real

# Intrare în container
docker exec -it week7_server_tcp /bin/bash

# Restart container
docker restart week7_server_tcp
```

### Docker Compose

```powershell
# Navigare la directorul docker
cd docker

# Pornire servicii
docker compose up -d

# Pornire cu profil proxy
docker compose --profile proxy up -d

# Oprire servicii
docker compose down

# Reconstruire imagini
docker compose build
docker compose up -d --build
```

### Rețele

```powershell
# Listare rețele
docker network ls

# Inspectare rețea
docker network inspect week7net

# Creare rețea manuală
docker network create --subnet=10.0.7.0/24 week7net
```

---

## Comenzi de Rețea (Testare)

### TCP

```powershell
# Client TCP simplu (PowerShell)
Test-NetConnection localhost -Port 9090

# Cu Python
python src/apps/client_tcp.py --host localhost --port 9090 --mesaj "test"

# Cu netcat (dacă este instalat)
echo "test" | nc localhost 9090
```

### UDP

```powershell
# Expeditor UDP
python src/apps/expeditor_udp.py --host localhost --port 9091 --mesaj "test"

# Cu netcat
echo "test" | nc -u localhost 9091
```

### Sondare Porturi

```powershell
# Sondare interval de porturi
python src/apps/sonda_porturi.py --tinta localhost --interval 9080-9100

# Sondare port unic
python src/apps/sonda_porturi.py --tinta localhost --port 9090
```

---

## Wireshark și Captură

### Filtre de Afișare

```
# Trafic TCP pe portul echo
tcp.port == 9090

# Trafic UDP pe portul receptor
udp.port == 9091

# Combinație
tcp.port == 9090 or udp.port == 9091

# Doar pachete SYN
tcp.flags.syn == 1 && tcp.flags.ack == 0

# Pachete RST (conexiuni refuzate)
tcp.flags.reset == 1

# Mesaje ICMP de eroare
icmp.type == 3

# Trafic de la/către IP specific
ip.addr == 10.0.7.100

# Analiza handshake complet
tcp.port == 9090 && (tcp.flags.syn == 1 || tcp.flags.fin == 1)
```

### Capturare din Linia de Comandă

```powershell
# Cu scriptul din kit
python scripts/capteaza_trafic.py --interfata eth0 --durata 60

# Cu tcpdump (în container sau WSL)
tcpdump -i eth0 -w captura.pcap tcp port 9090

# Cu tshark
tshark -i eth0 -w captura.pcap -a duration:60
```

---

## Profile Firewall

### Folosind scriptul firewallctl

```powershell
# Listare profile disponibile
python src/apps/firewallctl.py listeaza

# Aplicare profil (mod simulare)
python src/apps/firewallctl.py aplica referinta --simulare

# Aplicare profil real (necesită privilegii)
python src/apps/firewallctl.py aplica blocare_tcp_9090

# Resetare reguli
python src/apps/firewallctl.py reseteaza

# Afișare reguli curente
python src/apps/firewallctl.py arata
```

### Profile Disponibile

| Profil | Descriere |
|--------|-----------|
| `referinta` | Fără filtrare |
| `blocare_tcp_9090` | REJECT TCP pe 9090 |
| `blocare_udp_9091` | DROP UDP pe 9091 |
| `filtrare_mixta` | REJECT + DROP |
| `blocare_tcp_drop` | DROP TCP pe 9090 |

---

## Demonstrații

```powershell
# Demonstrație completă (interactiv)
python scripts/ruleaza_demo.py --demo complet

# Demo-uri individuale
python scripts/ruleaza_demo.py --demo referinta
python scripts/ruleaza_demo.py --demo tcp
python scripts/ruleaza_demo.py --demo udp
python scripts/ruleaza_demo.py --demo sondare
python scripts/ruleaza_demo.py --demo reject_vs_drop

# Listare demo-uri
python scripts/ruleaza_demo.py --listeaza
```

---

## Structura Directoarelor

```
WEEK7_WSLkit_RO/
├── setup/           # Scripturi de configurare
├── docker/          # Configurație Docker
├── scripts/         # Scripturi de management
├── src/             # Cod sursă
│   ├── apps/        # Aplicații de rețea
│   └── exercises/   # Exerciții
├── tests/           # Teste
├── docs/            # Documentație
├── homework/        # Teme pentru acasă
├── pcap/            # Capturi de pachete
└── artifacts/       # Fișiere generate
```

---

## Exerciții - Comenzi Rapide

```powershell
# Exercițiul 1: Captură de referință
python src/exercises/ex_7_01_captura_referinta.py

# Verificare exerciții
python tests/test_exercitii.py --exercitiu 1
python tests/test_exercitii.py --exercitiu 2
# ... etc.
```

---

## Depanare Rapidă

```powershell
# Docker nu pornește
wsl --update
wsl --set-default-version 2

# Port ocupat
netstat -ano | findstr :9090

# Container nu pornește
docker logs week7_server_tcp

# Verificare rețea Docker
docker network inspect week7net

# Reconstruire de la zero
python scripts/curata.py --complet
python scripts/porneste_lab.py
```

---

## 📝 Verifică-ți Cunoștințele

### Nivel REMEMBER (Reamintire)

Completează fără să te uiți în documentație:

1. Care este portul implicit pentru Portainer? `____`
2. Ce flag TCP marchează începutul unei conexiuni? `____`
3. Cum se numește acțiunea iptables care elimină silențios pachetele? `____`
4. Care este subnetul rețelei Docker week7net? `____/____`
5. Ce extensie au fișierele de captură Wireshark? `.____`

<details>
<summary>Răspunsuri</summary>

1. 9000
2. SYN
3. DROP
4. 10.0.7.0/24
5. .pcap sau .pcapng

</details>

### Nivel UNDERSTAND (Înțelegere)

Explică în propriile tale cuvinte (2-3 propoziții fiecare):

1. Care este diferența fundamentală dintre REJECT și DROP?
2. De ce handshake-ul TCP are exact 3 pași, nu 2 sau 4?
3. Ce înseamnă că un port este în starea FILTRAT la sondare?

### Nivel ANALYZE (Analiză)

Analizează următoarea captură Wireshark și răspunde:

```
Timp       Sursă          Dest           Protocol  Info
0.000000   192.168.1.10   10.0.7.100     TCP       SYN
0.000500   192.168.1.10   10.0.7.100     TCP       [TCP Retransmission] SYN
3.000000   192.168.1.10   10.0.7.100     TCP       [TCP Retransmission] SYN
9.000000   192.168.1.10   10.0.7.100     TCP       [TCP Retransmission] SYN
```

1. Ce tip de blocare este activă pe portul destinație? Justifică.
2. Cum ar arăta diferit captura dacă ar fi REJECT în loc de DROP?
3. Ce informație obține un atacator din acest comportament?

### Nivel EVALUATE (Evaluare)

Ești administrator de securitate. Alege și justifică:

1. Pentru un server web public, ai folosi DROP sau REJECT pentru porturile ne-HTTP? De ce?
2. Pentru un serviciu intern de backup, ai folosi DROP sau REJECT? De ce?
3. Când ar fi mai potrivită filtrarea la nivel aplicație (WAF) în locul iptables?

### Nivel CREATE (Creare)

Proiectează un profil de firewall pentru următorul scenariu:

**Scenariu:** Un server cu:
- SSH (port 22) - acces doar din rețeaua internă (192.168.0.0/16)
- HTTP (port 80) - acces public
- Bază de date (port 5432) - acces doar localhost
- Toate celelalte porturi blocate

Scrie regulile iptables și justifică alegerea ACCEPT/DROP/REJECT pentru fiecare.

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
