# Fișă de Comenzi – Săptămâna 5

> Laborator Rețele de Calculatoare – ASE, Informatică Economică
> realizat de Revolvix

## Comenzi de Laborator

### Pornire și Oprire

```powershell
# Verifică mediul
python setup/verifica_mediu.py

# Pornește laboratorul
python scripts/porneste_laborator.py

# Verifică starea
python scripts/porneste_laborator.py --status

# Oprește laboratorul
python scripts/opreste_laborator.py

# Curățare completă
python scripts/curata.py --complet
```

### Exerciții

```powershell
# Exercițiul 1: Analiză CIDR
python src/exercises/ex_5_01_cidr_flsm.py analizeaza 192.168.10.14/26
python src/exercises/ex_5_01_cidr_flsm.py analizeaza 192.168.10.14/26 --detaliat
python src/exercises/ex_5_01_cidr_flsm.py flsm 10.0.0.0/24 4
python src/exercises/ex_5_01_cidr_flsm.py binar 192.168.1.1

# Exercițiul 2: VLSM și IPv6
python src/exercises/ex_5_02_vlsm_ipv6.py vlsm 172.16.0.0/16 --cerinte 500,120,60,30,2
python src/exercises/ex_5_02_vlsm_ipv6.py ipv6-comprimare "2001:0db8:0000:0000:0000:0000:0000:0001"
python src/exercises/ex_5_02_vlsm_ipv6.py ipv6-expandare "2001:db8::1"
python src/exercises/ex_5_02_vlsm_ipv6.py comparatie 192.168.0.0/24 --cerinte 60,30,10,2

# Exercițiul 3: Quiz
python src/exercises/ex_5_03_generator_quiz.py
```

### Demonstrații

```powershell
# Demonstrație CIDR
python scripts/ruleaza_demo.py --demo cidr

# Comparație VLSM
python scripts/ruleaza_demo.py --demo vlsm

# Operații IPv6
python scripts/ruleaza_demo.py --demo ipv6

# Comunicare UDP
python scripts/ruleaza_demo.py --demo udp

# Toate demonstrațiile
python scripts/ruleaza_demo.py --demo toate
```

### Captură de Trafic

```powershell
# Pornește captură UDP
python scripts/captureaza_trafic.py --filtru udp

# Captură ICMP
python scripts/captureaza_trafic.py --filtru icmp

# Deschide Wireshark
python scripts/captureaza_trafic.py --wireshark
```

### Teste

```powershell
# Test rapid
python tests/test_smoke.py

# Toate testele
python tests/test_exercitii.py

# Teste pentru un exercițiu specific
python tests/test_exercitii.py --exercitiu 1
```

## Comenzi Docker

### Gestionare Containere

```powershell
# Listează containerele active
docker ps

# Listează toate containerele (inclusiv oprite)
docker ps -a

# Oprește un container
docker stop week5_python

# Pornește un container
docker start week5_python

# Repornește un container
docker restart week5_python

# Elimină un container
docker rm week5_python
```

### Acces la Containere

```powershell
# Shell interactiv
docker exec -it week5_python bash

# Execută o comandă
docker exec week5_python ip addr

# Verifică configurația rețelei
docker exec week5_python cat /etc/hosts
```

### Jurnale și Depanare

```powershell
# Jurnale unui container
docker logs week5_python

# Urmărește jurnalele în timp real
docker logs -f week5_python

# Inspectare container
docker inspect week5_python
```

### Rețele Docker

```powershell
# Listează rețelele
docker network ls

# Inspectare rețea
docker network inspect week5_labnet

# Listează containerele dintr-o rețea
docker network inspect week5_labnet --format '{{json .Containers}}'
```

## Comenzi Linux în Container

### Configurare Rețea

```bash
# Afișează interfețele
ip addr show

# Afișează tabela de rutare
ip route show

# Verifică conectivitate
ping -c 4 10.5.0.20

# Rezoluție DNS
nslookup google.com
```

### Utilitare Rețea

```bash
# Captură pachete
tcpdump -i eth0 -c 10

# Captură cu filtru
tcpdump -i eth0 port 9999

# Client UDP
echo "test" | nc -u 10.5.0.20 9999

# Ascultă pe un port UDP
nc -u -l 9999
```

## Filtre Wireshark

### Filtre de Captură (BPF)

```
# Trafic UDP pe portul 9999
udp port 9999

# Trafic către/de la o adresă
host 10.5.0.10

# Doar trafic ICMP
icmp

# Trafic pe o subrețea
net 10.5.0.0/24
```

### Filtre de Afișare

```
# Trafic IPv4
ip

# Trafic IPv6
ipv6

# Pachete UDP
udp

# Port specific
udp.port == 9999

# Adresă specifică
ip.addr == 10.5.0.10

# TTL specific
ip.ttl == 64
```

## Calcule Rapide

### Prefixe și Gazde

| Prefix | Gazde | Mască ultimul octet |
|--------|-------|---------------------|
| /24 | 254 | .0 |
| /25 | 126 | .128 |
| /26 | 62 | .192 |
| /27 | 30 | .224 |
| /28 | 14 | .240 |
| /29 | 6 | .248 |
| /30 | 2 | .252 |

### Formule

```
Gazde = 2^(32-prefix) - 2
Subrețele = 2^(biți împrumutați)
Prefix pentru N gazde = 32 - ⌈log₂(N+2)⌉
```

---

*Material didactic pentru Laborator Rețele de Calculatoare – ASE Bucuresti*
