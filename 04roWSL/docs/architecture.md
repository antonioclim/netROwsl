# Arhitectură: Kit Laborator Săptămâna 4

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

---

## Diagrama de Ansamblu

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           WINDOWS 11 HOST                                   │
│                                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   VS Code    │  │  Wireshark   │  │  PowerShell  │  │   Browser    │   │
│  │   (Editor)   │  │  (Captură)   │  │  (Comenzi)   │  │  (Portainer) │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
│         │                 │                 │                  │           │
│         │    vEthernet (WSL) - Interfață virtuală             │           │
│         │                 │                 │                  │           │
│ ════════╪═════════════════╪═════════════════╪══════════════════╪═══════════│
│         │                 │                 │                  │           │
│  ┌──────┴─────────────────┴─────────────────┴──────────────────┴─────────┐ │
│  │                         WSL2 (Ubuntu 22.04)                           │ │
│  │                                                                       │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │                      DOCKER ENGINE                              │ │ │
│  │  │                                                                 │ │ │
│  │  │  ┌─────────────────────────────────────────────────────────┐   │ │ │
│  │  │  │              retea_saptamana4 (bridge)                  │   │ │ │
│  │  │  │                                                         │   │ │ │
│  │  │  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐   │   │ │ │
│  │  │  │  │   TEXT      │ │   BINAR     │ │   UDP SENSOR    │   │   │ │ │
│  │  │  │  │ saptamana4- │ │ saptamana4- │ │  saptamana4-    │   │   │ │ │
│  │  │  │  │    text     │ │    binar    │ │     senzor      │   │   │ │ │
│  │  │  │  │             │ │             │ │                 │   │   │ │ │
│  │  │  │  │  TCP:5400   │ │  TCP:5401   │ │   UDP:5402      │   │   │ │ │
│  │  │  │  └──────┬──────┘ └──────┬──────┘ └────────┬────────┘   │   │ │ │
│  │  │  │         │               │                 │            │   │ │ │
│  │  │  └─────────┼───────────────┼─────────────────┼────────────┘   │ │ │
│  │  │            │               │                 │                │ │ │
│  │  │  ┌─────────┴───────────────┴─────────────────┴────────────┐   │ │ │
│  │  │  │                    PORT MAPPING                        │   │ │ │
│  │  │  │    localhost:5400 ←→ container:5400                    │   │ │ │
│  │  │  │    localhost:5401 ←→ container:5401                    │   │ │ │
│  │  │  │    localhost:5402 ←→ container:5402/udp                │   │ │ │
│  │  │  └────────────────────────────────────────────────────────┘   │ │ │
│  │  │                                                               │ │ │
│  │  │  ┌────────────────────────────────────────────────────────┐  │ │ │
│  │  │  │              PORTAINER (global)                        │  │ │ │
│  │  │  │              localhost:9000                            │  │ │ │
│  │  │  │              stud / studstudstud                       │  │ │ │
│  │  │  └────────────────────────────────────────────────────────┘  │ │ │
│  │  │                                                               │ │ │
│  │  └───────────────────────────────────────────────────────────────┘ │ │
│  │                                                                     │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Fluxul de Date

### Conexiune Client-Server (TCP)

```
   Client Python                    Docker Engine                  Server Container
        │                               │                               │
        │                               │                               │
   ┌────┴────┐                          │                          ┌────┴────┐
   │ socket()│                          │                          │ listen()│
   └────┬────┘                          │                          └────┬────┘
        │                               │                               │
        │ ─── connect(localhost:5400) ──┼───── port forward ──────────► │
        │                               │                               │
        │ ◄──────────────────────────── │ ◄─────── accept() ─────────── │
        │         [TCP 3-way handshake: SYN, SYN-ACK, ACK]              │
        │                               │                               │
   ┌────┴────┐                          │                               │
   │ send()  │ ─── "4 PING" ────────────┼─────────────────────────────► │
   └────┬────┘                          │                          ┌────┴────┐
        │                               │                          │ recv()  │
        │                               │                          │ process │
        │                               │                          │ send()  │
   ┌────┴────┐                          │                          └────┬────┘
   │ recv()  │ ◄── "4 PONG" ────────────┼─────────────────────────────── │
   └────┬────┘                          │                               │
        │                               │                               │
   ┌────┴────┐                          │                               │
   │ close() │ ─── FIN ─────────────────┼─────────────────────────────► │
   └─────────┘                          │                          ┌────┴────┐
        │ ◄──────────────────────────── │ ◄─────── FIN-ACK ─────── │ close() │
        │                               │                          └─────────┘
```

### Comunicare UDP (Senzor)

```
   Client Senzor                    Docker Engine                  Server UDP
        │                               │                               │
   ┌────┴────┐                          │                          ┌────┴────┐
   │ socket()│                          │                          │ bind()  │
   │ DGRAM   │                          │                          │ recvfrom│
   └────┬────┘                          │                          └────┬────┘
        │                               │                               │
        │ ─── sendto(datagrama 23B) ────┼─────────────────────────────► │
        │     [fire-and-forget]         │                               │
        │                               │                          ┌────┴────┐
        │     [fără răspuns]            │                          │ process │
        │                               │                          │ log     │
        │                               │                          └─────────┘
        │                               │                               
   ┌────┴────┐                          │                               
   │ sendto()│ ─── altă datagramă ──────┼─────────────────────────────► 
   └─────────┘                          │                               
```

---

## Structura Protocolului BINAR

### Antet (14 octeți)

```
Octet:   0    1    2    3    4    5    6    7    8    9   10   11   12   13
       ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
       │ 'N'│ 'P'│Vers│Tip │  Lungime  │      Secvență       │     CRC32     │
       │    │    │    │    │  (2B BE)  │      (4B BE)        │    (4B BE)    │
       └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘
       │◄─ Magic ─►│    │    │◄────────►│◄────────────────────►│◄────────────►│
           2B      1B  1B      2 bytes        4 bytes              4 bytes
       
       BE = Big-Endian (Network Byte Order)
```

### Mesaj Complet

```
       ┌───────────────────────────────────────────────────────────────────────┐
       │                        MESAJ COMPLET                                  │
       ├───────────────────────────────────────────────────────────────────────┤
       │  ANTET (14 bytes fix)              │  PAYLOAD (lungime variabilă)    │
       │                                    │                                  │
       │  [NP][V][T][LL][SSSS][CCCC]        │  [date utile...]                │
       │                                    │                                  │
       └────────────────────────────────────┴──────────────────────────────────┘
       
       Calcul CRC32:
       ┌─────────────────────────────────────────────────────────────────────┐
       │  CRC = crc32( ANTET[0:10] + PAYLOAD )                               │
       │                                                                      │
       │  Adică: Magic + Versiune + Tip + Lungime + Secvență + Payload       │
       │  NU include câmpul CRC în sine (evident)                            │
       └─────────────────────────────────────────────────────────────────────┘
```

### Tipuri de Mesaje

```
       ┌──────────┬────────┬─────────────────────────────────────────────────┐
       │   Cod    │  Nume  │  Descriere                                      │
       ├──────────┼────────┼─────────────────────────────────────────────────┤
       │   0x01   │  PING  │  Verificare conexiune (fără payload)            │
       │   0x02   │  PONG  │  Răspuns la PING (fără payload)                 │
       │   0x03   │  SET   │  Setare valoare (payload: cheie\0valoare)       │
       │   0x04   │  GET   │  Citire valoare (payload: cheie)                │
       │   0x05   │ DELETE │  Ștergere cheie (payload: cheie)                │
       │   0x06   │RESPONSE│  Răspuns cu date (payload: valoare)             │
       │   0xFF   │ ERROR  │  Eroare (payload: mesaj eroare)                 │
       └──────────┴────────┴─────────────────────────────────────────────────┘
```

---

## Structura Datagramei Senzor UDP

```
Octet:   0    1    2    3    4    5    6    7    8    9   ...  16   17  ...  20   21   22
       ┌────┬─────────┬───────────────────┬────────────────────┬─────────────┬───────────┐
       │Vers│ ID Senz │    Temperatură    │      Locație       │    CRC32    │ Rezervat  │
       │ 1B │  2B BE  │     4B float BE   │    10B ASCII+pad   │    4B BE    │    2B     │
       └────┴─────────┴───────────────────┴────────────────────┴─────────────┴───────────┘
       
       Total: 23 octeți (dimensiune fixă)
       
       Locație: String ASCII, padding cu \x00 până la 10 bytes
       Exemplu: "Lab1" → [L][a][b][1][\0][\0][\0][\0][\0][\0]
```

---

## Structura Directorului

```
04roWSL/
├── README.md                    # Ghid principal
├── CHANGELOG.md                 # Istoric modificări
│
├── docker/
│   ├── docker-compose.yml       # Orchestrare containere
│   └── Dockerfile               # Imagine personalizată (dacă e cazul)
│
├── docs/
│   ├── theory_summary.md        # Fundamente teoretice
│   ├── commands_cheatsheet.md   # Referință rapidă comenzi
│   ├── troubleshooting.md       # Ghid depanare
│   ├── further_reading.md       # Resurse suplimentare
│   ├── architecture.md          # ACEST FIȘIER
│   ├── debugging_guide.md       # Ghid debugging pas-cu-pas
│   ├── faq.md                   # Întrebări frecvente
│   └── peer_instruction.md      # Întrebări PI (instructor)
│
├── scripts/
│   ├── start_lab.py             # Pornire mediu
│   ├── stop_lab.py              # Oprire mediu
│   └── utils/
│       └── docker_utils.py      # Utilitare Docker
│
├── src/
│   ├── apps/
│   │   ├── text_proto_server.py    # Server protocol TEXT
│   │   ├── text_proto_client.py    # Client protocol TEXT
│   │   ├── binary_proto_server.py  # Server protocol BINAR
│   │   ├── binary_proto_client.py  # Client protocol BINAR
│   │   ├── udp_sensor_server.py    # Server senzor UDP
│   │   └── udp_sensor_client.py    # Client senzor UDP
│   │
│   ├── exercises/
│   │   ├── ex1_text_client.py      # Exercițiu 1: Client TEXT
│   │   ├── ex2_binary_client.py    # Exercițiu 2: Client BINAR
│   │   ├── ex3_udp_sensor.py       # Exercițiu 3: Senzor UDP
│   │   ├── ex4_crc_detection.py    # Exercițiu 4: Detectare CRC
│   │   ├── ex5_pair_debugging.py   # Exercițiu 5: Debugging perechi
│   │   └── ex6_wireshark_trace.md  # Exercițiu 6: Analiză Wireshark
│   │
│   └── utils/
│       └── protocol_utils.py       # Funcții utilitare protocoale
│
├── homework/
│   └── exercises/
│       ├── tema_4_01.py            # Temă: Client BINAR complet
│       └── tema_4_02.py            # Temă: Simulator senzori
│
├── tests/
│   ├── test_protocols.py           # Teste protocoale
│   └── test_protocol_utils.py      # Teste unitare utilitare
│
├── pcap/
│   └── (capturi Wireshark)
│
└── artifacts/
    └── (fișiere generate)
```

---

## Secvență de Pornire

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SECVENȚĂ PORNIRE LABORATOR                          │
└─────────────────────────────────────────────────────────────────────────────┘

     Utilizator                    Script                      Docker
         │                           │                            │
         │ ── python start_lab.py ──►│                            │
         │                           │                            │
         │                           │ ── verifică docker ───────►│
         │                           │ ◄─── docker activ ─────────│
         │                           │                            │
         │                           │ ── docker compose up ─────►│
         │                           │                            │
         │                           │      ┌────────────────────────────┐
         │                           │      │ Creare rețea               │
         │                           │      │ retea_saptamana4           │
         │                           │      ├────────────────────────────┤
         │                           │      │ Start saptamana4-text      │
         │                           │      │ Start saptamana4-binar     │
         │                           │      │ Start saptamana4-senzor    │
         │                           │      └────────────────────────────┘
         │                           │                            │
         │                           │ ◄─── containere pornite ───│
         │                           │                            │
         │                           │ ── verifică port 5400 ────►│
         │                           │ ◄─── port activ ───────────│
         │                           │                            │
         │                           │ ── verifică port 5401 ────►│
         │                           │ ◄─── port activ ───────────│
         │                           │                            │
         │                           │ ── verifică port 5402 ────►│
         │                           │ ◄─── port activ ───────────│
         │                           │                            │
         │ ◄── "Mediul e pregătit!" ─│                            │
         │                           │                            │
```

---

## Referințe

- [README principal](../README.md)
- [Ghid Debugging](debugging_guide.md)
- [Troubleshooting](troubleshooting.md)

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
