# Săptămâna 6: NAT/PAT, Protocoale de Suport pentru Rețele și Rețele Definite prin Software

> Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | Laborator Rețele de Calculatoare
> 
> de Revolvix

## Prezentare generală

Această sesiune de laborator integrează două domenii complementare ale arhitecturii moderne de rețea: mecanismele de traducere a adreselor care susțin ciclul de viață extins al IPv4, și schimbarea de paradigmă către rețelele definite prin software (SDN) care decuplează logica de control de hardware-ul de redirecționare.

Prima componentă examinează Network Address Translation (NAT) și varianta sa cu multiplexare de porturi (PAT/NAPT), protocoale care au devenit o infrastructură indispensabilă pentru maparea adreselor private la cele publice. Studenții vor configura reguli MASQUERADE bazate pe iptables pe un router Linux, vor observa procesul bidirecțional de traducere și vor analiza modul în care alocarea de porturi efemere permite mai multor hosturi interne să partajeze o singură adresă publică.

A doua componentă introduce arhitectura SDN prin OpenFlow 1.3, demonstrând separarea fundamentală dintre planul de control (luarea deciziilor centralizate) și planul de date (redirecționarea distribuită a pachetelor). Utilizând OS-Ken ca framework de controller și Open vSwitch ca switch programabil, studenții vor implementa și observa politici bazate pe fluxuri care permit sau blochează selectiv traficul pe baza criteriilor de sursă, destinație și protocol.

## Obiective de învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Reamintească** scopul și clasificarea variantelor NAT (static, dinamic, PAT) și rolul protocoalelor auxiliare (ARP, DHCP, ICMP, NDP)
2. **Explice** cum tabelele de traducere PAT mențin starea bidirecțională a sesiunii și de ce acest mecanism creează provocări pentru conexiunile de intrare
3. **Implementeze** reguli NAT/MASQUERADE folosind iptables pe un router Linux multi-homed într-o topologie simulată
4. **Demonstreze** instalarea fluxurilor SDN prin observarea comunicării controller-switch și inspectarea tabelelor de fluxuri cu ovs-ofctl
5. **Analizeze** diferențele comportamentale dintre traficul permis și cel blocat într-o topologie SDN, corelând rezultatele pachetelor cu regulile de flux instalate
6. **Compare** rutarea distribuită tradițională cu controlul SDN centralizat, articulând compromisurile în scalabilitate, flexibilitate și domenii de defecțiune
7. **Proiecteze** politici OpenFlow personalizate care implementează controlul accesului per-host, per-protocol într-o rețea definită prin software

## Cerințe preliminare

### Cerințe de cunoștințe

- Înțelegerea adresării IPv4, subnetting-ului și notației CIDR (Săptămânile 4-5)
- Familiarizare cu conceptele de programare socket TCP/UDP (Săptămânile 2-3)
- Competențe de bază în linia de comandă Linux (navigare fișiere, gestionare procese)
- Înțelegerea conceptuală a modelelor OSI și TCP/IP

### Cerințe software

- Windows 10/11 cu WSL2 activat (Ubuntu 22.04 sau ulterior)
- Docker Desktop cu integrare backend WSL2
- Wireshark (aplicație nativă Windows)
- Python 3.11 sau ulterior
- Git (opțional, pentru controlul versiunilor)

### Cerințe hardware

- Minim 8GB RAM (16GB recomandat pentru execuție paralelă de containere)
- 10GB spațiu liber pe disc
- Conectivitate de rețea (pentru instalarea inițială a pachetelor)

## Pornire rapidă

### Configurare inițială (Se rulează o singură dată)

```powershell
# Deschide PowerShell ca Administrator
cd WEEK6_WSLkit

# Verifică dacă cerințele preliminare sunt instalate
python setup/verify_environment.py

# Dacă vreo verificare eșuează, rulează helper-ul de instalare
python setup/install_prerequisites.py

# Configurează Docker pentru operațiuni privilegiate
python setup/configure_docker.py
```

### Pornirea laboratorului

```powershell
# Pornește toate serviciile (containere Docker, configurare rețea)
python scripts/start_lab.py

# Verifică dacă serviciile rulează
python scripts/start_lab.py --status

# Pentru reconstruirea containerelor după modificări
python scripts/start_lab.py --rebuild
```

### Accesarea serviciilor

| Serviciu | URL/Port | Scop |
|----------|----------|------|
| Portainer | https://localhost:9443 | Panou de administrare containere |
| Controller SDN | localhost:6633 | Endpoint controller OpenFlow |
| Router NAT (rnat) | 203.0.113.1 | Gateway NAT cu interfață publică |
| Observator NAT | Port 5000 | Demonstrație traducere PAT |
| Echo TCP | Port 9090 | Testare conectivitate SDN |
| Echo UDP | Port 9091 | Testare politici specifice protocolului |

## Topologia rețelei

### Planul de adrese IP Săptămâna 6

| Resursă | Adresă | Scop |
|---------|--------|------|
| Subrețea SDN | 10.0.6.0/24 | Rețea internă topologie SDN |
| h1 | 10.0.6.11 | Host SDN (acces complet la h2) |
| h2 | 10.0.6.12 | Host SDN (server) |
| h3 | 10.0.6.13 | Host SDN (acces restricționat) |
| Subrețea privată | 192.168.1.0/24 | Rețea internă topologie NAT |
| NAT privat | 192.168.1.1 | Interfața routerului (partea privată) |
| NAT public | 203.0.113.1 | Interfața routerului (partea publică, TEST-NET-3) |
| h3 (NAT) | 203.0.113.2 | Server public în topologia NAT |

### Planul de porturi

| Port | Protocol | Utilizare |
|------|----------|-----------|
| 9090 | TCP | Aplicație server/client echo |
| 9091 | UDP | Aplicație server/client echo |
| 6633 | TCP | Controller OpenFlow (legacy) |
| 6653 | TCP | Controller OpenFlow (standard) |
| 5000 | TCP | Aplicație observator NAT |
| 5600-5699 | - | Interval porturi personalizate Săptămâna 6 |

## Exerciții de laborator

### Exercițiul 1: Configurarea și observarea NAT/PAT

**Obiectiv:** Configurarea NAT MASQUERADE pe un router Linux și observarea traducerii adreselor de port în acțiune.

**Durată:** 40 minute

**Context:** Când hosturile private (adrese RFC 1918) comunică cu serverele publice, NAT rescrie adresele sursă la adresa IP publică a routerului. PAT extinde acest lucru traducând și porturile sursă, permițând mai multor hosturi interne să partajeze o singură adresă publică.

**Pași:**

1. Pornește topologia NAT:
   ```powershell
   python scripts/run_demo.py --demo nat
   ```

2. În CLI-ul Mininet, verifică configurația interfețelor:
   ```bash
   rnat ifconfig
   rnat iptables -t nat -L -n -v
   ```

3. Pornește observatorul NAT pe serverul public (h3):
   ```bash
   h3 python3 src/apps/nat_observer.py server --bind 203.0.113.2 --port 5000
   ```

4. De pe hosturile private, inițiază conexiuni:
   ```bash
   h1 python3 src/apps/nat_observer.py client --host 203.0.113.2 --port 5000 --msg "Salut de la h1"
   h2 python3 src/apps/nat_observer.py client --host 203.0.113.2 --port 5000 --msg "Salut de la h2"
   ```

5. Observă output-ul serverului - notează că ambele conexiuni par să provină de la 203.0.113.1 (IP-ul public NAT) cu porturi sursă diferite.

6. Verifică traducerile NAT:
   ```bash
   rnat conntrack -L 2>/dev/null || rnat cat /proc/net/nf_conntrack
   ```

**Observații așteptate:**
- Adresele private (192.168.1.x) nu sunt niciodată vizibile pe partea publică
- Fiecare conexiune de la hosturi interne diferite folosește un port tradus unic
- Tabela NAT menține starea bidirecțională pentru traficul de retur

**Verificare:**
```powershell
python tests/test_exercises.py --exercise 1
```

### Exercițiul 2: Topologie SDN și observarea fluxurilor

**Obiectiv:** Implementarea unei topologii SDN cu un controller OpenFlow și observarea redirecționării pachetelor bazate pe fluxuri.

**Durată:** 35 minute

**Context:** SDN separă planul de control (unde se iau deciziile de redirecționare) de planul de date (unde pachetele sunt efectiv redirecționate). Controller-ul instalează reguli de flux în switch-uri care definesc perechi match-action.

**Pași:**

1. Pornește topologia SDN cu reguli de flux:
   ```powershell
   python scripts/run_demo.py --demo sdn
   ```

2. În CLI-ul Mininet, verifică conectivitatea:
   ```bash
   # Ar trebui să funcționeze (h1 ↔ h2 PERMITE)
   h1 ping -c 3 h2
   
   # Ar trebui să eșueze (h1 → h3 BLOCHEAZĂ)
   h1 ping -c 3 h3
   
   # Ar trebui să funcționeze (h2 → h3 PERMITE)
   h2 ping -c 3 h3
   ```

3. Inspectează tabelele de fluxuri instalate:
   ```bash
   ovs-ofctl -O OpenFlow13 dump-flows s1
   ```

4. Pornește serverele de testare pe h2 și h3:
   ```bash
   h2 python3 src/apps/tcp_echo.py server &
   h3 python3 src/apps/tcp_echo.py server &
   ```

5. Testează politicile la nivel de protocol:
   ```bash
   # TCP de la h1 la h2 (ar trebui să funcționeze)
   h1 python3 src/apps/tcp_echo.py client --host 10.0.6.12
   
   # TCP de la h1 la h3 (ar trebui să eșueze)
   h1 python3 src/apps/tcp_echo.py client --host 10.0.6.13
   ```

**Observații așteptate:**
- Tabelele de fluxuri conțin reguli match-action
- Traficul permis primește răspunsuri
- Traficul blocat timeout-ează sau este rejectat
- Numărul de potriviri în fluxuri crește cu traficul

**Verificare:**
```powershell
python tests/test_exercises.py --exercise 2
```

### Exercițiul 3: Modificarea politicilor SDN

**Obiectiv:** Modificarea politicilor controller-ului pentru a schimba comportamentul de acces la nivel de protocol.

**Durată:** 30 minute

**Pași:**

1. Examinează codul controller-ului:
   ```powershell
   # Deschide controller-ul de politici în editorul tău
   code src/apps/sdn_policy_controller.py
   ```

2. Localizează secțiunea de definire a politicilor și modifică pentru a permite UDP pe portul 9091 la h3

3. Repornește controller-ul și testează noua politică:
   ```bash
   # În Mininet
   h3 python3 src/apps/udp_echo.py server &
   h1 python3 src/apps/udp_echo.py client --host 10.0.6.13
   ```

4. Verifică noile reguli de flux:
   ```bash
   ovs-ofctl -O OpenFlow13 dump-flows s1 | grep udp
   ```

**Criterii de succes:**
- Traficul UDP la h3 funcționează conform noii politici
- Regulile de flux reflectă filtrul specific protocolului
- Alte politici rămân neafectate

## Oprirea laboratorului

### Oprire standard
```powershell
python scripts/stop_lab.py
```

### Curățare completă (resetare totală)
```powershell
python scripts/cleanup.py --full --prune
```

## Teme pentru acasă

Consultă directorul `homework/` pentru exercițiile de lucru individual.

### Tema 1: Analiză extinsă NAT

Documentează procesul de traducere NAT pentru următorul scenariu:
- Trei hosturi interne conectându-se simultan la același server extern
- Fiecare host face două conexiuni (HTTP și HTTPS)
- Capturează și analizează starea tabelei NAT

**Livrabil:** `homework/exercises/hw_6_01_analiza_nat.md`

### Tema 2: Implementare politici SDN personalizate

Proiectează și implementează o politică SDN care:
- Permite HTTP (port 80) și HTTPS (port 443) de la toate hosturile la h3
- Blochează tot ICMP către h3 cu excepția celui de la h2
- Permite SSH (port 22) doar de la h1 la h2

**Livrabil:** `homework/exercises/hw_6_02_politica_sdn.py`

## Depanare

### Probleme frecvente

#### Problemă: Erori la curățarea Mininet ("File exists")
**Soluție:** Rulează curățarea cu flag-ul force:
```powershell
python scripts/cleanup.py --force
# Sau manual în WSL:
sudo mn -c
```

#### Problemă: Switch-ul OVS nu se conectează la controller
**Soluție:** Verifică dacă controller-ul rulează și portul este accesibil:
```bash
ss -ltn | grep 6633
ovs-vsctl show
```

#### Problemă: Containerele Docker nu pornesc în modul privilegiat
**Soluție:** Asigură-te că Docker Desktop este configurat pentru integrarea WSL2:
1. Deschide Docker Desktop Settings
2. Navighează la Resources > WSL Integration
3. Activează integrarea cu distribuția ta Ubuntu

#### Problemă: NAT nu traduce pachetele
**Soluție:** Verifică dacă IP forwarding-ul este activat:
```bash
sysctl net.ipv4.ip_forward
# Ar trebui să fie 1; dacă nu:
sudo sysctl -w net.ipv4.ip_forward=1
```

#### Problemă: Ping-urile în topologia SDN sunt lente sau expiră
**Soluție:** Verifică dacă regulile de flux sunt instalate:
```bash
ovs-ofctl -O OpenFlow13 dump-flows s1
```
Dacă este gol sau există doar regula table-miss, controller-ul poate să nu funcționeze corect.

Consultă `docs/troubleshooting.md` pentru soluții suplimentare.

## Fundamente teoretice

### NAT și PAT

Network Address Translation a apărut ca răspuns la epuizarea adreselor IPv4, permițând organizațiilor să utilizeze intervale de adrese private (RFC 1918: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) intern, în timp ce partajează adrese publice limitate extern. Port Address Translation extinde acest lucru prin multiplexarea conexiunilor prin numere de port, permițând mii de hosturi interne să partajeze un singur IP public.

Procesul de traducere implică:
1. **Ieșire:** Rescrierea IP-ului sursă (și portului în PAT) la adresa publică a dispozitivului NAT
2. **Urmărirea stării:** Menținerea unei tabele de traducere care mapează tuplurile interne la cele externe
3. **Intrare:** Traducerea inversă folosind starea stocată

### Rețele definite prin software

SDN reprezintă o schimbare arhitecturală fundamentală de la controlul distribuit la controlul centralizat al rețelei. Principiile cheie includ:
1. **Separarea responsabilităților:** Logica de control (controller) distinctă de redirecționare (switch-uri)
2. **Programabilitate:** Comportamentul rețelei definit prin API-uri software
3. **Viziune centralizată:** Controller-ul menține starea globală a rețelei
4. **Redirecționare bazată pe fluxuri:** Pachetele sunt potrivite cu reguli și se aplică acțiuni

OpenFlow oferă interfața southbound între controller și switch-uri, definind modul în care tabelele de fluxuri sunt populate și interogate.

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (ediția a 7-a). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- RFC 1918 – Alocarea adreselor pentru rețele private
- RFC 5737 – Blocuri de adrese IPv4 rezervate pentru documentație
- RFC 4861 – Neighbor Discovery pentru IP versiunea 6 (IPv6)
- Open Networking Foundation (2015). *OpenFlow Switch Specification* Versiunea 1.3.5

## Diagrame de arhitectură

### Topologia NAT
```
    ┌─────────────────────────────────────────────────────────────┐
    │                    Rețea privată                            │
    │                    192.168.1.0/24                           │
    │                                                             │
    │   ┌───────────┐              ┌───────────┐                  │
    │   │    h1     │              │    h2     │                  │
    │   │.10        │              │.20        │                  │
    │   └─────┬─────┘              └─────┬─────┘                  │
    │         │                          │                        │
    │         └──────────┬───────────────┘                        │
    │                    │                                        │
    │              ┌─────┴─────┐                                   │
    │              │    s1     │                                   │
    │              └─────┬─────┘                                   │
    └────────────────────┼────────────────────────────────────────┘
                         │ eth0: 192.168.1.1
                   ┌─────┴─────┐
                   │   rnat    │  ← NAT/MASQUERADE
                   │  (router) │
                   └─────┬─────┘
                         │ eth1: 203.0.113.1
    ┌────────────────────┼────────────────────────────────────────┐
    │                    │                                        │
    │              ┌─────┴─────┐                                   │
    │              │    s2     │                                   │
    │              └─────┬─────┘                                   │
    │                    │                                        │
    │              ┌─────┴─────┐                                   │
    │              │    h3     │                                   │
    │              │.2         │                                   │
    │              └───────────┘                                   │
    │                                                             │
    │                    Rețea publică                            │
    │                    203.0.113.0/24 (TEST-NET-3)              │
    └─────────────────────────────────────────────────────────────┘
```

### Topologia SDN
```
                          ┌─────────────────────────────┐
                          │      Controller SDN         │
                          │       (OS-Ken)              │
                          │                             │
                          │  ┌──────────────────────┐   │
                          │  │  Motor de politici   │   │
                          │  │  • h1↔h2: PERMITE    │   │
                          │  │  • *→h3: BLOCHEAZĂ   │   │
                          │  │  • UDP→h3: CONFIG    │   │
                          │  └──────────────────────┘   │
                          └─────────────┬───────────────┘
                                        │ OpenFlow 1.3
                                        │ (port 6633)
    ┌───────────────────────────────────┼───────────────────────────────────┐
    │                                   │                                   │
    │                           ┌───────┴───────┐                           │
    │                           │      s1       │                           │
    │                           │   (OVS)       │                           │
    │                           │               │                           │
    │                           │ ┌───────────┐ │                           │
    │                           │ │Tabel flux │ │                           │
    │                           │ └───────────┘ │                           │
    │                           └───┬───┬───┬───┘                           │
    │                               │   │   │                               │
    │                    ┌──────────┘   │   └──────────┐                    │
    │                    │              │              │                    │
    │              ┌─────┴─────┐  ┌─────┴─────┐  ┌─────┴─────┐              │
    │              │    h1     │  │    h2     │  │    h3     │              │
    │              │10.0.6.11  │  │10.0.6.12  │  │10.0.6.13  │              │
    │              │           │  │           │  │           │              │
    │              │ [✓ ACCES  │  │  [SERVER] │  │  [ACCES   │              │
    │              │  COMPLET] │  │           │  │RESTRICȚ.] │              │
    │              └───────────┘  └───────────┘  └───────────┘              │
    │                                                                       │
    │                        Rețea SDN: 10.0.6.0/24                         │
    └───────────────────────────────────────────────────────────────────────┘
```

---

*Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
