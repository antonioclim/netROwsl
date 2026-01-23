# 📚 Proiecte Rețele de Calculatoare

> **Disciplina:** Rețele de Calculatoare  
> **Program:** Informatică Economică, Anul 3, Semestrul 2  
> **Instituție:** Academia de Studii Economice București - CSIE  
> **Semestru:** 2025-2026

---

## 📋 Cuprins

Acest repository conține **20 de proiecte** pentru disciplina Rețele de Calculatoare, organizate în două categorii:

### 🎯 [PROIECTE/](PROIECTE/) — Proiecte principale (P01-P15)

Proiecte complete pentru echipe de 1-3 studenți.

| Nr. | Proiect | Tehnologii |
|-----|---------|------------|
| P01 | [Firewall SDN Mininet](PROIECTE/P01_Firewall_SDN_Mininet.md) | Mininet, OpenFlow, POX/Ryu |
| P02 | [Rețea Hibridă Mininet Docker](PROIECTE/P02_Retea_Hibrida_Mininet_Docker.md) | Mininet, Docker, Python |
| P03 | [IDS Monitorizare Trafic](PROIECTE/P03_IDS_Monitorizare_Trafic_Python.md) | Python, Scapy, Threading |
| P04 | [Mesagerie Securizată](PROIECTE/P04_Mesagerie_Securizata_Client_Server.md) | Python, AES/RSA, Sockets |
| P05 | [Protocol Rutare Personalizat](PROIECTE/P05_Protocol_Rutare_Personalizat.md) | Python, Distance Vector/Link State |
| P06 | [SDN Controller OpenFlow](PROIECTE/P06_SDN_Mininet_Controller_OpenFlow.md) | Mininet, OpenFlow, Python |
| P07 | [Firewall IDS Software](PROIECTE/P07_Firewall_IDS_Monitorizare_Trafic.md) | Python, iptables, Logging |
| P08 | [Server Web Proxy Invers](PROIECTE/P08_Server_Web_Proxy_Invers.md) | Python, HTTP, Nginx |
| P09 | [Server FTP Multi-Client](PROIECTE/P09_Server_FTP_Multi_Client.md) | Python, FTP, Docker |
| P10 | [Orchestrare DNS SSH FTP](PROIECTE/P10_Orchestrare_DNS_SSH_FTP_Docker.md) | Docker Compose, BIND, vsftpd |
| P11 | [SDN Avansat OpenFlow](PROIECTE/P11_SDN_Avansat_Mininet_OpenFlow.md) | Mininet, OpenFlow, QoS |
| P12 | [Microservicii Load Balancing](PROIECTE/P12_Microservicii_Docker_Load_Balancing.md) | Docker, Nginx, HAProxy |
| P13 | [Aplicație Distribuită RPC](PROIECTE/P13_Aplicatie_Distribuita_RPC.md) | gRPC/JSON-RPC, Docker |
| P14 | [Securitate IDS IPS](PROIECTE/P14_Securitate_IDS_IPS_Simulare.md) | Snort/Suricata, Python |
| P15 | [IoT Edge Computing MQTT](PROIECTE/P15_IoT_Edge_Computing_MQTT.md) | MQTT, Mosquitto, Docker |

### 📦 [REZERVA_individual/](REZERVA_individual/) — Proiecte rezervă (P16-P20)

Proiecte mai simple, pentru lucru individual sau cazuri speciale.

| Nr. | Proiect | Tehnologii |
|-----|---------|------------|
| P16 | [Analiza HTTP Wireshark](REZERVA_individual/P16_Analiza_HTTP_Wireshark.md) | Wireshark, HTTP |
| P17 | [Rețea LAN NAT DHCP](REZERVA_individual/P17_Retea_LAN_NAT_DHCP.md) | Cisco Packet Tracer |
| P18 | [Chat TCP Client Server](REZERVA_individual/P18_Chat_TCP_Client_Server.md) | Python, Sockets TCP |
| P19 | [Scanner Porturi Securitate](REZERVA_individual/P19_Scanner_Porturi_Securitate.md) | Python, Sockets |
| P20 | [IoT Casă Inteligentă](REZERVA_individual/P20_IoT_Casa_Inteligenta_Securitate.md) | Packet Tracer, IoT |

---

## ⚠️ IMPORTANT: Reguli de evaluare

### 1. Prezența fizică obligatorie

**Evaluarea proiectului se face EXCLUSIV la facultate!**

- Prezentarea finală (Etapa 4) necesită prezență fizică
- Fiecare membru al echipei trebuie să demonstreze că înțelege codul
- Întrebări din implementare și teorie sunt posibile
- **Lipsa de la prezentare = nepromovare proiect**

### 2. GitHub obligatoriu

Fiecare proiect trebuie publicat pe GitHub:

```
https://github.com/[username]/retele-proiect-XX
```

Structura repository-ului și ce se postează la fiecare etapă sunt detaliate în fișierul fiecărui proiect.

### 3. Calendarul etapelor

| Etapa | Săptămâna | Ce livrezi | Punctaj |
|-------|-----------|------------|---------|
| **E1** - Design | Săpt. 5 | Specificații + Diagrame | 20% |
| **E2** - Prototip | Săpt. 9 | Implementare parțială | 25% |
| **E3** - Final | Săpt. 13 | Versiune completă | 35% |
| **E4** - Prezentare | Săpt. 14 | Demo live | 20% |

---

## 🛠️ Mediul de lucru

### Configurația standard

```
Windows 11 → WSL2 → Ubuntu 22.04 → Docker Engine → Portainer CE
```

### Credențiale implicite

| Serviciu | Utilizator | Parolă |
|----------|------------|--------|
| Ubuntu WSL | `stud` | `stud` |
| Portainer | `stud` | `studstudstud` |

### Puncte de acces

| Serviciu | URL |
|----------|-----|
| Portainer | http://localhost:9000 |
| Servicii laborator | Variază (8080, 8081, etc.) |

---

## 📖 Cum să începi

1. **Alege un proiect** din lista de mai sus
2. **Citește fișierul** proiectului ales pentru cerințe detaliate
3. **Creează repository** pe GitHub conform structurii indicate
4. **Urmează calendarul** etapelor și postează progresul
5. **Pregătește prezentarea** pentru evaluarea finală

---

## 📚 Resurse adiționale

- **Materialele de laborator:** Folderele `{NN}roWSL` din repository-ul cursului
- **Documentația Docker:** https://docs.docker.com
- **Documentația Mininet:** http://mininet.org
- **Tutoriale Wireshark:** https://www.wireshark.org/docs/

---

## 📝 Convenția de denumire arhive

**Format:** `NUME_Prenume_GGGG_PXX_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Nume familie (MAJUSCULE) | POPESCU |
| Prenume | Prenume (prima literă mare) | Ion |
| GGGG | Număr grupă | 1098 |
| PXX | Număr proiect | P05 |
| TT | Etapă (E1-E4) sau săptămână (S07) | E2 |

**Exemplu:** `POPESCU_Ion_1098_P05_E2.zip`

---

*Rețele de Calculatoare — ASE București — Semestrul 2, 2025-2026*  
*Ultima actualizare: Ianuarie 2026*
