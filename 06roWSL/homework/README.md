# Teme pentru acasă Săptămâna 6

> Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de ing. dr. Antonio Clim

## Prezentare generală

Aceste exerciții extind conceptele explorate în timpul sesiunii de laborator despre NAT/PAT și Rețele Definite prin Software.

---

## Tema 1: Analiză extinsă NAT

**Nivel Bloom:** APPLY + ANALYSE  
**Durată estimată:** 2 ore  
**Punctaj:** 15%

### Obiectiv

Analizează comportamentul traducerilor NAT sub diverse modele de trafic.

### Sarcini

1. Modifică `topo_nat.py` pentru a adăuga un al patrulea host (h4) în rețeaua privată
2. Generează conexiuni TCP simultane de la h1, h2 și h4 către h3
3. Capturează traficul pe rnat-eth1 folosind tcpdump
4. Documentează intrările din tabela de traducere PAT

### Livrabile

- Fișierul de topologie modificat
- Captura de pachete (PCAP)
- Analiză scrisă (300-500 cuvinte)

---

## Tema 2: Implementare politici SDN personalizate

**Nivel Bloom:** APPLY + ANALYSE  
**Durată estimată:** 2-3 ore  
**Punctaj:** 15%

### Obiectiv

Proiectează și implementează politici OpenFlow personalizate.

### Sarcini

1. Extinde topologia SDN pentru a include un al patrulea host (h4: 10.0.6.14/24)
2. Implementează regulile:
   - h1 ↔ h2: PERMITE tot traficul
   - h1 ↔ h3: PERMITE doar ICMP
   - h1 → h4: PERMITE doar TCP portul 80
   - h4 → h1: BLOCHEAZĂ tot traficul
3. Testează fiecare politică

### Livrabile

- Fișierul de topologie modificat
- Controller actualizat
- Script de test
- Documentație

---

## Tema 3: Analiză comparativă

**Nivel Bloom:** ANALYSE  
**Durată estimată:** 3 ore  
**Punctaj:** 15%

### Obiectiv

Compară NAT tradițional cu abordările bazate pe SDN.

### Sarcini

1. Cercetează cel puțin trei alternative bazate pe SDN la NAT tradițional
2. Implementează un exemplu simplu folosind Mininet/OS-Ken
3. Compară metricile de performanță și complexitate

### Livrabile

- Document de cercetare (800-1000 cuvinte)
- Implementare funcțională
- Tabel comparativ

---

## Tema 4: Evaluare Critică NAT vs SDN-NAT

**Nivel Bloom:** EVALUATE  
**Durată estimată:** 2-3 ore  
**Punctaj:** 15%

### Context

O companie mică (50 angajați) trebuie să aleagă între:
- **Opțiunea A:** Router Linux cu iptables NAT
- **Opțiunea B:** Switch OpenFlow cu controller SDN care implementează NAT

### Sarcini

**1. Completează tabelul de evaluare (40%)**

| Criteriu | NAT Tradițional | SDN-NAT | Câștigător |
|----------|-----------------|---------|------------|
| Cost hardware inițial | | | |
| Complexitate configurare | | | |
| Scalabilitate (50→500 users) | | | |
| Vizibilitate trafic | | | |
| Flexibilitate politici | | | |
| Single point of failure | | | |
| Latență per-pachet | | | |
| Expertiză necesară | | | |

**2. Scrie recomandarea (35%)**

200-300 cuvinte cu cel puțin 3 argumente tehnice.

**3. Scenariu alternativ (25%)**

50-100 cuvinte despre când alegerea opusă ar fi mai bună.

### Livrabil

`homework/exercises/hw_6_04_evaluare_nat_sdn.md`

---

## Tema 5: Proiectare Topologie Campus Hibridă

**Nivel Bloom:** CREATE  
**Durată estimată:** 4-5 ore  
**Punctaj:** 20%

### Context

Proiectează arhitectura de rețea pentru un campus universitar cu:
- 3 clădiri cu câte 100 utilizatori fiecare
- 1 datacenter central
- Acces internet printr-un singur punct de ieșire
- Izolare între departamente

### Cerințe funcționale

1. Izolare inter-departamente
2. Acces la datacenter pentru toate departamentele
3. Acces extern la serverele web
4. NAT pentru ieșire

### Livrabile

**1. Diagrama topologiei (20%)**

**2. Fișier topologie Mininet (35%)**
- Minim 3 switch-uri OpenFlow
- 1 router NAT
- Comentarii explicative

**3. Controller SDN (30%)**
- Politici de izolare
- Logging pentru pachetele blocate

**4. Documentație (15%)**
- 300-500 cuvinte
- Justificarea deciziilor arhitecturale
- Cum s-ar scala soluția

### Bonus (până la +10%)

- Implementare failover
- Dashboard de monitorizare
- Teste automate

---

## Ghid de trimitere

- Trimite toate fișierele ca o singură arhivă ZIP: `tema6_<id_student>.zip`
- Include un `README.txt` cu numele și ID-ul de student
- Asigură-te că fișierele Python au sintaxă validă
- Include capturile în format PCAP

**Termen limită:** Consultă calendarul cursului

---

*Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de ing. dr. Antonio Clim*
