# Fișa de Comenzi – Săptămâna 5

> Referință rapidă pentru Laborator Rețele de Calculatoare
> ASE, Informatică Economică | realizat de Revolvix

---

## Comenzi Docker

### Verificare Status

```bash
# Verifică dacă Docker e pornit
docker ps

# Verifică toate containerele (inclusiv oprite)
docker ps -a

# Verifică rețelele Docker
docker network ls
```

### Gestiune Containere

```bash
# Pornește containerele laboratorului
cd /mnt/d/RETELE/SAPT5/05roWSL
docker compose up -d

# Oprește containerele
docker compose down

# Repornește un container specific
docker restart week5_python
```

### Execuție în Container

```bash
# Shell interactiv în container
docker exec -it week5_python bash

# Execută o comandă
docker exec week5_python ip addr

# Ping între containere
docker exec week5_python ping -c 3 10.5.0.20
```

### Inspectare Rețea

```bash
# Detalii rețea laborator
docker network inspect week5_labnet

# IP-uri containere
docker network inspect week5_labnet --format '{{range .Containers}}{{.Name}}: {{.IPv4Address}}{{"\n"}}{{end}}'
```

---

## Comenzi Python pentru Exerciții

### Exercițiul 5.01 – Analiză CIDR și FLSM

```bash
# Analiză simplă
python3 src/exercises/ex_5_01_cidr_flsm.py analizeaza 192.168.10.14/26

# Analiză cu detalii binare
python3 src/exercises/ex_5_01_cidr_flsm.py analizeaza 192.168.10.14/26 --detaliat

# Mod învățare cu predicții
python3 src/exercises/ex_5_01_cidr_flsm.py invata 192.168.10.14/26

# Subnetare FLSM în 4 subrețele
python3 src/exercises/ex_5_01_cidr_flsm.py flsm 192.168.100.0/24 4

# Conversie IP la binar
python3 src/exercises/ex_5_01_cidr_flsm.py binar 192.168.1.1

# Export JSON
python3 src/exercises/ex_5_01_cidr_flsm.py analizeaza 192.168.10.14/26 --json
```

### Exercițiul 5.02 – VLSM și IPv6

```bash
# Alocare VLSM
python3 src/exercises/ex_5_02_vlsm_ipv6.py vlsm 172.16.0.0/16 --cerinte 500,120,60,30,2

# Mod învățare VLSM
python3 src/exercises/ex_5_02_vlsm_ipv6.py invata-vlsm 192.168.0.0/24 --cerinte 60,20,10,2

# Comprimare IPv6
python3 src/exercises/ex_5_02_vlsm_ipv6.py ipv6-comprimare "2001:0db8:0000:0000:0000:0000:0000:0001"

# Expandare IPv6
python3 src/exercises/ex_5_02_vlsm_ipv6.py ipv6-expandare "2001:db8::1"

# Generare subrețele IPv6
python3 src/exercises/ex_5_02_vlsm_ipv6.py subretele-ipv6 "2001:db8:cafe::/48" --numar 6

# Calculator prefix
python3 src/exercises/ex_5_02_vlsm_ipv6.py prefix-necesar 100
```

### Exercițiul 5.03 – Quiz

```bash
# Quiz standard (10 întrebări, mediu)
python3 src/exercises/ex_5_03_generator_quiz.py

# Quiz scurt și ușor
python3 src/exercises/ex_5_03_generator_quiz.py --intrebari 5 --dificultate usor

# Quiz pregătire examen
python3 src/exercises/ex_5_03_generator_quiz.py -n 20 -d greu
```

---

## Comenzi Rețea Linux

### Adrese IP

```bash
# Afișează configurația IP
ip addr
ip -4 addr show      # Doar IPv4
ip -6 addr show      # Doar IPv6

# Tabel de rutare
ip route
ip -6 route
```

### Conectivitate

```bash
# Ping IPv4
ping -c 4 10.5.0.20

# Ping IPv6
ping6 -c 4 fe80::1

# Traceroute
traceroute 8.8.8.8

# Verifică port deschis
nc -zv 10.5.0.20 9999
```

### DNS

```bash
# Rezolvare DNS
nslookup google.com
dig google.com A
host google.com
```

---

## Comenzi Wireshark / tshark

### Filtre Captură

| Filtru | Descriere |
|--------|-----------|
| `ip.addr == 10.5.0.0/24` | Trafic din rețeaua laborator |
| `udp.port == 9999` | Server UDP Echo |
| `ip.src == 10.5.0.10` | Sursă specifică |
| `icmp` | Pachete ping |
| `tcp.flags.syn == 1` | Conexiuni noi TCP |

### tshark (CLI)

```bash
# Captură live pe interfață
sudo tshark -i eth0

# Captură cu filtru
sudo tshark -i eth0 -f "udp port 9999"

# Salvare în fișier
sudo tshark -i eth0 -w captura.pcap

# Citire din fișier
tshark -r captura.pcap
```

---

## Formule Calcul Rapid

### Gazde din Prefix

```
Gazde = 2^(32 - prefix) - 2

/24 → 2^8 - 2  = 254
/25 → 2^7 - 2  = 126
/26 → 2^6 - 2  = 62
/27 → 2^5 - 2  = 30
/28 → 2^4 - 2  = 14
/29 → 2^3 - 2  = 6
/30 → 2^2 - 2  = 2
```

### Prefix din Gazde

```
prefix = 32 - ceil(log2(gazde + 2))

10 gazde  → 32 - 4 = /28
50 gazde  → 32 - 6 = /26
100 gazde → 32 - 7 = /25
200 gazde → 32 - 8 = /24
500 gazde → 32 - 9 = /23
```

### Salt între Subrețele

```
Salt = 2^(32 - prefix)

/24: salt = 256
/25: salt = 128
/26: salt = 64
/27: salt = 32
/28: salt = 16
```

---

## Comenzi PowerShell (Windows)

```powershell
# Navigare la laborator
cd D:\RETELE\SAPT5\05roWSL

# Intră în WSL
wsl

# Verifică versiunea WSL
wsl --list --verbose

# Deschide Portainer în browser
Start-Process "http://localhost:9000"
```

---

## Credențiale

| Serviciu | Utilizator | Parolă |
|----------|------------|--------|
| Ubuntu WSL | `stud` | `stud` |
| Portainer | `stud` | `studstudstud` |

---

## Teste Rapide

```bash
# Verifică mediul
python3 setup/verifica_mediu.py

# Verifică calitatea materialelor
python3 scripts/verifica_calitate.py

# Rulează teste exerciții
python3 -m pytest tests/test_exercitii.py -v

# Teste pentru exercițiul 1
python3 tests/test_exercitii.py --exercitiu 1

# Rulează doctest-uri
python3 tests/test_doctest.py
```

---

## Navigare Rapidă

| ← Anterior | Document | Următor → |
|------------|----------|-----------|
| [Rezumat Teoretic](rezumat_teorie.md) | **Fișa de Comenzi** | [Peer Instruction](peer_instruction.md) |

## Documente Înrudite

- [README Principal](../README.md) — Ghid de pornire
- [Glosar](GLOSSARY.md) — Termeni și definiții
- [Rezumat Teoretic](rezumat_teorie.md) — Concepte și formule
- [Depanare](depanare.md) — Soluții probleme
- [Referință API](api_reference.md) — Documentație funcții
- [Exemple Utilizare](exemple_utilizare.md) — Scenarii complete

---

*Laborator Rețele de Calculatoare – ASE București*
