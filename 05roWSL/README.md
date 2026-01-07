# Săptămâna 5: Nivelul Rețea – Adresare IPv4/IPv6, Subrețele și VLSM

> Laborator Rețele de Calculatoare – ASE, Informatică Economică
> 
> realizat de Revolvix

## Prezentare Generală

Această sesiune de laborator explorează **Nivelul Rețea** din modelul TCP/IP, concentrându-se pe mecanismele fundamentale de adresare care permit comunicarea între dispozitive în rețele interconectate. Studenții vor examina atât arhitectura IPv4, cât și IPv6, înțelegând principiile de proiectare, schemele de adresare și tehnicile de subnetare care stau la baza infrastructurii moderne de internet.

Componenta practică pune accent pe calculele de subnetare prin două metodologii distincte: **FLSM** (Fixed-Length Subnet Mask – Mască de subrețea de lungime fixă) și **VLSM** (Variable-Length Subnet Mask – Mască de subrețea de lungime variabilă). Prin exerciții interactive Python și observarea traficului în containere Docker, studenții vor dezvolta competențe în proiectarea schemelor de adresare eficiente care minimizează risipa de adrese IP, respectând în același timp cerințele organizaționale.

Mediul de laborator utilizează Docker pentru a simula mai multe segmente de rețea, permițând studenților să observe comportamentul pachetelor, să analizeze anteturile IP și să verifice configurațiile de adresare folosind instrumente standard de rețea.

## Obiective de Învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Identificați** rolul și funcțiile Nivelului Rețea în arhitecturile OSI și TCP/IP
2. **Explicați** diferențele dintre adresarea IPv4 și IPv6, inclusiv notația și structura
3. **Calculați** adrese de rețea, adrese de broadcast și intervale de gazde utilizabile pentru orice bloc CIDR
4. **Aplicați** tehnicile FLSM și VLSM pentru a divide rețelele în subrețele în funcție de cerințe
5. **Proiectați** scheme de adresare eficiente care minimizează risipa de adrese IP
6. **Evaluați** compromisurile dintre simplitatea FLSM și eficiența VLSM în scenarii din lumea reală

## Cerințe Preliminare

### Cunoștințe Necesare
- Sisteme de numerație binară și hexazecimală
- Concepte de bază ale rețelelor de calculatoare (din săptămânile 1-4)
- Înțelegerea stratificării protocoalelor și încapsulării
- Familiaritate cu operațiile de linie de comandă

### Cerințe Software
- Windows 10/11 cu WSL2 activat
- Docker Desktop (backend WSL2)
- Wireshark (aplicație Windows nativă)
- Python 3.11 sau versiune ulterioară
- Git

### Cerințe Hardware
- Minim 8GB RAM (recomandat 16GB)
- 10GB spațiu liber pe disc
- Conectivitate la rețea

## Pornire Rapidă

### Configurare Inițială (Se execută o singură dată)

```powershell
# Deschideți PowerShell ca Administrator
cd WEEK5_WSLkit_RO

# Verificați cerințele preliminare
python setup/verifica_mediu.py

# Dacă apar probleme, rulați asistentul de instalare
python setup/instaleaza_cerinte.py
```

### Pornirea Laboratorului

```powershell
# Porniți toate serviciile
python scripts/porneste_laborator.py

# Verificați că totul funcționează
python scripts/porneste_laborator.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | https://localhost:9443 | Se setează la prima accesare |
| Container Python | 10.5.0.10 | Acces prin docker exec |
| Server UDP | 10.5.0.20:9999 | Fără autentificare |
| Client UDP | 10.5.0.30 | Acces prin docker exec |

## Exerciții de Laborator

### Exercițiul 1: Analiză CIDR și Subnetare FLSM

**Obiectiv:** Analizați blocuri CIDR pentru a extrage proprietățile rețelei și aplicați FLSM pentru a crea subrețele de dimensiuni egale.

**Durată:** 25-30 minute

**Pași:**

1. Deschideți un terminal în directorul kitului
2. Rulați scriptul de analiză CIDR cu o adresă exemplu:
   ```bash
   python src/exercises/ex_5_01_cidr_flsm.py 192.168.10.14/26
   ```
3. Examinați rezultatul care afișează:
   - Adresa de rețea și adresa de broadcast
   - Intervalul de gazde utilizabile
   - Reprezentarea binară a măștii
   - Clasa de adresă și tipul (public/privat)

4. Testați subnetarea FLSM:
   ```bash
   python src/exercises/ex_5_01_cidr_flsm.py 10.0.0.0/16 --subretele 4
   ```
5. Observați cum rețeaua /16 este divizată în 4 subrețele egale /18

**Verificare:**
```bash
# Comanda pentru verificarea succesului
python tests/test_exercitii.py --exercitiu 1
```

**Rezultat Așteptat:**
- Analiza 192.168.10.14/26 ar trebui să raporteze 62 de gazde utilizabile
- Divizarea FLSM a 10.0.0.0/16 în 4 subrețele produce blocuri /18

---

### Exercițiul 2: Alocare VLSM și Operații IPv6

**Obiectiv:** Implementați alocarea VLSM pentru cerințe variabile de gazde și efectuați operații de adresare IPv6.

**Durată:** 30-35 minute

**Pași:**

1. Rulați alocatorul VLSM cu cerințe multiple de departamente:
   ```bash
   python src/exercises/ex_5_02_vlsm_ipv6.py --vlsm 172.16.0.0/16 --cerinte 500,120,60,30,2
   ```
2. Analizați cum algoritmul:
   - Sortează cerințele descrescător
   - Alocă dimensiunea minimă a blocului pentru fiecare cerință
   - Menține alinierea la granițe de bloc
   - Maximizează utilizarea spațiului de adrese

3. Comparați eficiența VLSM vs FLSM pentru aceleași cerințe

4. Explorați operațiile IPv6:
   ```bash
   python src/exercises/ex_5_02_vlsm_ipv6.py --ipv6-comprimare "2001:0db8:0000:0000:0000:0000:0000:0001"
   python src/exercises/ex_5_02_vlsm_ipv6.py --ipv6-expandare "2001:db8::1"
   ```

5. Generați subrețele IPv6 dintr-o alocare /48:
   ```bash
   python src/exercises/ex_5_02_vlsm_ipv6.py --subretele-ipv6 "2001:db8:abcd::/48" --numar 8
   ```

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 2
```

**Rezultat Așteptat:**
- Alocarea VLSM ar trebui să producă 5 subrețele cu prefixe variate (/23, /25, /26, /27, /30)
- Comprimarea IPv6 ar trebui să producă `2001:db8::1`
- Expandarea ar trebui să restabilească formatul complet pe 32 de caractere hexazecimale

---

### Exercițiul 3: Chestionar Interactiv de Subnetare

**Obiectiv:** Testați-vă cunoștințele de subnetare printr-un quiz interactiv.

**Durată:** 15-20 minute

**Pași:**

1. Lansați generatorul de quiz:
   ```bash
   python src/exercises/ex_5_03_generator_quiz.py
   ```

2. Răspundeți la întrebări despre:
   - Calculul adreselor de rețea
   - Determinarea adreselor de broadcast
   - Identificarea gazdelor utilizabile
   - Selectarea măștii corecte pentru cerințele de gazde

3. Revedeți explicațiile pentru răspunsurile incorecte

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 3
```

---

### Exercițiul 4: Comunicare UDP în Rețea Containerizată

**Obiectiv:** Observați comunicarea UDP între containere și capturați traficul de rețea.

**Durată:** 20-25 minute

**Pași:**

1. Asigurați-vă că mediul de laborator este pornit:
   ```bash
   python scripts/porneste_laborator.py --status
   ```

2. Într-un terminal, porniți captura de trafic:
   ```bash
   python scripts/captureaza_trafic.py --interfata eth0 --iesire pcap/udp_demo.pcap
   ```

3. În alt terminal, rulați demonstrația UDP:
   ```bash
   python scripts/ruleaza_demo.py --demo udp
   ```

4. Opriți captura (Ctrl+C) și deschideți fișierul pcap în Wireshark

5. Analizați:
   - Anteturile IP (adrese sursă și destinație)
   - Anteturile UDP (porturi sursă și destinație)
   - Încărcătura utilă a mesajelor echo

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 4
```

## Demonstrații

### Demo 1: Analiză CIDR Completă

Demonstrație automată a analizei blocurilor CIDR cu reprezentare vizuală.

```powershell
python scripts/ruleaza_demo.py --demo cidr
```

**Ce să observați:**
- Conversia binară a adreselor IP
- Aplicarea măștii pentru derivarea adresei de rețea
- Calculul intervalului de difuzare

### Demo 2: Comparație FLSM vs VLSM

Comparație vizuală a eficienței celor două tehnici de subnetare.

```powershell
python scripts/ruleaza_demo.py --demo vlsm
```

**Ce să observați:**
- Risipa de adrese în FLSM când cerințele variază
- Alocarea optimă în VLSM
- Calcule de eficiență procentuală

### Demo 3: Operații IPv6

Demonstrarea comprimării și expandării adreselor IPv6.

```powershell
python scripts/ruleaza_demo.py --demo ipv6
```

**Ce să observați:**
- Regulile de comprimare (zerouri consecutivi, grupuri de conducere)
- Validarea formatului de adresă
- Generarea subrețelelor /64

### Demo 4: Comunicare UDP

Demonstrarea trimiterii și primirii pachetelor UDP între containere.

```powershell
python scripts/ruleaza_demo.py --demo udp
```

**Ce să observați:**
- Rezoluția adreselor IP între containere
- Structura pachetelor UDP
- Mecanismul de echo pentru verificare

## Captură și Analiză de Pachete

### Capturarea Traficului

```powershell
# Pornirea capturii
python scripts/captureaza_trafic.py --interfata eth0 --iesire pcap/captura_sapt5.pcap

# Sau utilizați Wireshark direct
# Deschideți Wireshark > Selectați interfața corespunzătoare
```

### Filtre Wireshark Sugerate

```
# Trafic IPv4
ip.version == 4

# Trafic IPv6
ipv6

# Trafic UDP pe portul 9999
udp.port == 9999

# Trafic ICMP (ping)
icmp

# Trafic de la/către container specific
ip.addr == 10.5.0.10

# Pachete cu TTL specific
ip.ttl == 64
```

## Oprire și Curățare

### Sfârșitul Sesiunii

```powershell
# Opriți toate containerele (păstrează datele)
python scripts/opreste_laborator.py

# Verificați oprirea
docker ps
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```powershell
# Eliminați toate containerele, rețelele și volumele pentru această săptămână
python scripts/curata.py --complet

# Verificați curățarea
docker system df
```

## Teme pentru Acasă

Consultați directorul `homework/` pentru exercițiile de rezolvat acasă.

### Tema 1: Proiectare Rețea Corporativă

Proiectați o schemă de adresare VLSM pentru o companie cu 5 departamente având cerințe diferite de gazde. Documentați alegerile și justificați eficiența.

### Tema 2: Plan de Migrare IPv6

Elaborați un plan de tranziție de la IPv4 la IPv6 pentru o rețea mică, incluzând:
- Schemă de adresare IPv6
- Mecanisme de coexistență (dual-stack, tunneling)
- Cronologie de implementare

## Depanare

### Probleme Frecvente

#### Problemă: Containerele nu pornesc
**Soluție:** Verificați că Docker Desktop rulează și are backend-ul WSL2 activat. Rulați `docker info` pentru a confirma.

#### Problemă: Nu se poate accesa Portainer
**Soluție:** Verificați că portul 9443 nu este folosit de altă aplicație. Folosiți `netstat -an | findstr 9443` pentru a verifica.

#### Problemă: Scripturile Python nu găsesc modulele
**Soluție:** Asigurați-vă că rulați din directorul rădăcină al kitului și că PYTHONPATH include directorul curent.

#### Problemă: Captura de pachete nu funcționează
**Soluție:** Containerele necesită capabilități NET_ADMIN și NET_RAW. Verificați configurația docker-compose.yml.

Consultați `docs/depanare.md` pentru mai multe soluții.

## Fundamente Teoretice

### Nivelul Rețea în Modelul OSI

Nivelul Rețea (Layer 3) oferă adresare logică și rutare, permițând comunicarea între rețele diferite. Funcțiile principale includ:

- **Adresare logică:** Atribuirea de identificatori unici (adrese IP) dispozitivelor
- **Rutare:** Determinarea căii optime pentru pachete între rețele
- **Fragmentare:** Divizarea pachetelor pentru a se încadra în MTU-ul rețelei
- **Încapsulare:** Adăugarea antetului IP la datele de la nivelurile superioare

### Arhitectura IPv4

Adresele IPv4 constau din 32 de biți, reprezentați în notație zecimală cu punct (ex: 192.168.1.1). Spațiul de adrese este organizat în:

- **Clase tradiționale:** A, B, C, D (multicast), E (experimental)
- **CIDR (Classless Inter-Domain Routing):** Permite prefixe de lungime arbitrară
- **Adrese private:** 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16

### Subnetare FLSM vs VLSM

**FLSM** împarte o rețea în subrețele de dimensiuni egale, simplificând administrarea dar risipind adrese când cerințele diferă.

**VLSM** permite subrețele de dimensiuni diferite, maximizând eficiența prin adaptarea dimensiunii blocului la cerințele reale.

### Arhitectura IPv6

IPv6 utilizează adrese de 128 de biți în notație hexazecimală cu două puncte. Caracteristici cheie:

- **Spațiu de adrese extins:** 2^128 adrese posibile
- **Header simplificat:** Structură fixă de 40 de octeți
- **Autoconfigurare:** SLAAC (Stateless Address Autoconfiguration)
- **Tipuri de adrese:** Unicast, multicast, anycast (fără broadcast)

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- RFC 791 - Internet Protocol (IPv4)
- RFC 8200 - Internet Protocol, Version 6 (IPv6)
- RFC 4632 - Classless Inter-domain Routing (CIDR)

## Diagramă de Arhitectură

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEEK5_WSLkit Environment                     │
│                    Rețea: week5_labnet (10.5.0.0/24)           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  week5_python   │  │ week5_udp-server│  │ week5_udp-client│ │
│  │                 │  │                 │  │                 │ │
│  │  IP: 10.5.0.10  │  │  IP: 10.5.0.20  │  │  IP: 10.5.0.30  │ │
│  │                 │  │  Port: 9999     │  │                 │ │
│  │  • Python 3.11  │  │  • Server Echo  │  │  • Client UDP   │ │
│  │  • Exerciții    │  │  • UDP Socket   │  │  • Testare      │ │
│  │  • Utilitare    │  │                 │  │                 │ │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘ │
│           │                    │                    │          │
│           └────────────────────┼────────────────────┘          │
│                                │                               │
│                    ┌───────────┴───────────┐                   │
│                    │   Docker Bridge Net   │                   │
│                    │    10.5.0.0/24        │                   │
│                    └───────────────────────┘                   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  Portainer: https://localhost:9443                              │
│  Capabilități: NET_ADMIN, NET_RAW (pentru tcpdump)             │
└─────────────────────────────────────────────────────────────────┘
```

---

*Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix*
