# Săptămâna 14: Recapitulare Integrată și Evaluare Proiect

> Laborator Rețele de Calculatoare - ASE, Informatică Economică
>
> by Revolvix

## Prezentare Generală

Această sesiune de laborator reprezintă culminarea cursului de Rețele de Calculatoare, integrând concepte și competențe practice dezvoltate pe parcursul semestrului. Mediul de laborator constă într-o arhitectură web cu echilibrare de încărcare ce demonstrează principii fundamentale de rețelistică într-un context containerizat.

## Obiective de Învățare

La finalul acestei sesiuni, veți fi capabili să:

1. **Identificați** componentele unei arhitecturi web cu echilibrare de încărcare
2. **Explicați** funcționarea distribuției round-robin și comunicării reverse proxy
3. **Demonstrați** utilizarea instrumentelor de captură și analiză a pachetelor
4. **Analizați** comportamentul TCP/IP în scenarii client-server
5. **Construiți** scripturi pentru verificarea funcționalității serviciilor de rețea
6. **Evaluați** performanța sistemelor distribuite prin metrici practice

## Cerințe Preliminare

### Software Necesar
- Windows 10/11 cu WSL2 activat
- Docker Desktop (backend WSL2)
- Wireshark (aplicație Windows)
- Python 3.11+

### Hardware Minim
- 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc

## Pornire Rapidă

### 1. Verificare Mediu

```powershell
cd WEEK14_WSLkit_RO
python setup/verifica_mediu.py
```

### 2. Pornire Laborator

```powershell
python scripts/porneste_lab.py
```

### 3. Accesare Servicii

| Serviciu | URL/Port | Descriere |
|----------|----------|-----------|
| Load Balancer | http://localhost:8080 | Punct intrare cereri HTTP |
| Backend App 1 | http://localhost:8001 | Server backend #1 |
| Backend App 2 | http://localhost:8002 | Server backend #2 |
| Server Echo | tcp://localhost:9000 | Server echo pentru teste TCP |
| Portainer | https://localhost:9443 | Management containere |

## Structura Proiectului

```
WEEK14_WSLkit_RO/
├── README.md                    # Acest fișier
├── CHANGELOG.md                 # Istoric modificări
├── LICENSE                      # Licență MIT
├── setup/                       # Configurare mediu
│   ├── verifica_mediu.py        # Verificare cerințe
│   └── requirements.txt         # Dependențe Python
├── docker/                      # Infrastructură Docker
│   ├── docker-compose.yml       # Definiție servicii
│   └── Dockerfile               # Imagine container
├── scripts/                     # Scripturi management
│   ├── porneste_lab.py          # Pornire laborator
│   ├── opreste_lab.py           # Oprire laborator
│   ├── curata.py                # Curățare resurse
│   ├── captura_trafic.py        # Captură pachete
│   ├── ruleaza_demo.py          # Demonstrații
│   └── utils/                   # Utilitare
├── src/                         # Cod sursă
│   ├── apps/                    # Aplicații
│   ├── exercises/               # Exerciții laborator
│   └── utils/                   # Funcții auxiliare
├── tests/                       # Teste
│   └── test_exercitii.py        # Verificare exerciții
├── docs/                        # Documentație
│   ├── rezumat_teoretic.md      # Rezumat concepte
│   └── depanare.md              # Ghid depanare
├── homework/                    # Teme pentru acasă
│   ├── README.md                # Instrucțiuni teme
│   └── exercises/               # Cod starter
├── pcap/                        # Capturi de pachete
└── artifacts/                   # Fișiere generate
```

## Exerciții de Laborator

### Exercițiul 1: Verificarea Mediului
Confirmarea funcționării corecte a infrastructurii.

```powershell
python setup/verifica_mediu.py
python scripts/porneste_lab.py
```

### Exercițiul 2: Analiza Load Balancer-ului
Înțelegerea distribuției round-robin.

```bash
# Trimiteți cereri multiple și observați alternarea
for i in {1..10}; do curl -s http://localhost:8080/; echo; done
```

### Exercițiul 3: Testare Server Echo TCP
Verificarea comunicării TCP.

```bash
echo "Salut Lume" | nc localhost 9000
```

### Exercițiul 4: Captură și Analiză Pachete
Utilizarea Wireshark/tshark.

```powershell
python scripts/captura_trafic.py --durata 30 --lab
```

### Verificare Exerciții

```powershell
python tests/test_exercitii.py --toate
```

## Demonstrații

### Demo Complet
```powershell
python scripts/ruleaza_demo.py --demo complet
```

### Demo Failover
```powershell
python scripts/ruleaza_demo.py --demo failover
```

### Generare Trafic
```powershell
python scripts/ruleaza_demo.py --demo trafic
```

## Captură Pachete

### Pornire Captură
```powershell
python scripts/captura_trafic.py --durata 30 --iesire pcap/demo.pcap
```

### Filtre Wireshark Utile
```
http                               # Trafic HTTP
tcp.port == 8080                   # Trafic load balancer
tcp.port in {8080, 8001, 8002}     # Tot traficul laboratorului
tcp.flags.syn == 1                 # Pachete SYN
```

## Oprire și Curățare

### Oprire Laborator
```powershell
python scripts/opreste_lab.py
```

### Curățare Completă
```powershell
python scripts/curata.py --complet
```

## Teme pentru Acasă

Consultați `homework/README.md` pentru detalii complete.

| Tema | Descriere | Fișier |
|------|-----------|--------|
| 1 | Protocol Echo Îmbunătățit | `tema_14_01_echo_avansat.py` |
| 2 | Load Balancer cu Ponderi | `tema_14_02_lb_ponderat.py` |
| 3 | Analizator PCAP Automat | `tema_14_03_analizator_pcap.py` |

## Depanare

### Docker nu pornește
```powershell
# Verificați Docker Desktop
# Reporniți WSL: wsl --shutdown
```

### Port ocupat
```powershell
netstat -ano | findstr :8080
```

### Container se oprește
```bash
docker logs week14_app1 --tail 50
```

Consultați `docs/depanare.md` pentru mai multe soluții.

## Arhitectură

```
┌─────────────────────────────────────────────┐
│           REȚEA FRONTEND 172.21.0.0/24      │
│                                             │
│    ┌─────────────┐    ┌─────────────┐      │
│    │   CLIENT    │    │     LB      │ ◄──── Port 8080
│    │ 172.21.0.10 │    │ 172.21.0.2  │      │
│    └─────────────┘    └──────┬──────┘      │
└──────────────────────────────┼──────────────┘
                               │
┌──────────────────────────────┼──────────────┐
│           REȚEA BACKEND 172.20.0.0/24       │
│                              │              │
│    ┌─────────────┐    ┌──────▼──────┐      │
│    │    APP1     │◄───┤     LB      │      │
│    │ 172.20.0.10 │    │ 172.20.0.2  │      │
│    └─────────────┘    └──────┬──────┘      │
│                              │              │
│    ┌─────────────┐           │              │
│    │    APP2     │◄──────────┘              │
│    │ 172.20.0.11 │                          │
│    └─────────────┘                          │
│                                             │
│    ┌─────────────┐                          │
│    │    ECHO     │ ◄──────────────── Port 9000
│    │ 172.20.0.20 │                          │
│    └─────────────┘                          │
└─────────────────────────────────────────────┘
```

## Referințe

- Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.)
- Tanenbaum, A. S. & Wetherall, D. J. (2021). *Computer Networks* (6th ed.)
- Stevens, W. R. (2011). *TCP/IP Illustrated, Volume 1: The Protocols* (2nd ed.)
- Documentație Docker: https://docs.docker.com/
- Documentație Wireshark: https://www.wireshark.org/docs/

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
