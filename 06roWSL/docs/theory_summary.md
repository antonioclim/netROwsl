# Săptămâna 6: Sumar concepte teoretice

> Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de ing. dr. Antonio Clim

## Network Address Translation (NAT)

### Problema epuizării IPv4

Creșterea explozivă a Internetului în anii 1990 a revelat o limitare fundamentală: spațiul de adrese IPv4 pe 32 de biți (aproximativ 4,3 miliarde de adrese) nu putea acomoda numărul proiectat de dispozitive. NAT a apărut ca o măsură practică de tranziție care rămâne folosită și astăzi.

### Variante NAT

**NAT Static** stabilește o mapare permanentă unu-la-unu între o adresă internă și una externă. Acesta este folosit când serverele interne necesită accesibilitate externă consistentă.

**NAT Dinamic** menține un pool de adrese externe și le alocă hosturilor interne după necesitate. Când un host inițiază o conexiune, o adresă externă disponibilă este alocată și eliberată când conexiunea se termină.

**PAT (Port Address Translation)**, cunoscut și ca NAT Overload sau NAPT, permite mai multor hosturi interne să partajeze o singură adresă IP externă prin multiplexare prin numere de port. Aceasta este cea mai comună formă de NAT.

### Funcționarea PAT

Când un host intern (192.168.1.10:45678) se conectează la un server extern (8.8.8.8:443):

1. Routerul primește pachetul de ieșire
2. Înregistrează adresa/portul sursă originale în tabela de traducere
3. Rescrie sursa la IP-ul său public cu un port unic (203.0.113.1:50001)
4. Când răspunsul ajunge la 203.0.113.1:50001, routerul consultă tabela
5. Rescrie destinația înapoi la 192.168.1.10:45678 și redirecționează intern

### Limitările NAT

- **Întrerupe conectivitatea end-to-end**: Hosturile externe nu pot iniția conexiuni către hosturi interne fără port forwarding
- **Complicații de protocol**: Protocoalele care încorporează adrese IP în payload necesită Application Layer Gateways
- **Dependența de stare**: Dispozitivul NAT trebuie să mențină starea sesiunii
- **Overhead de performanță**: Procesarea traducerii adaugă latență

---

## Protocoale suport

### ARP (Address Resolution Protocol)

ARP rezolvă adresele IPv4 în adrese MAC într-un segment de rețea local. Când un host trebuie să trimită un cadru dar cunoaște doar IP-ul destinație, transmite broadcast o cerere ARP. Hostul cu IP-ul corespunzător răspunde cu adresa sa MAC.

Concepte cheie:
- **Cache ARP**: Hosturile mențin un cache al rezoluțiilor recente
- **Proxy ARP**: Un router poate răspunde cererilor ARP în numele hosturilor din subrețele diferite
- **Gratuitous ARP**: Un host își anunță propria legătură IP-MAC

### DHCP (Dynamic Host Configuration Protocol)

DHCP automatizează configurația IP. Procesul DORA:

1. **Discover**: Clientul transmite broadcast căutând servere DHCP
2. **Offer**: Serverele răspund cu oferte de configurație
3. **Request**: Clientul solicită o ofertă specifică
4. **Acknowledge**: Serverul confirmă și comite lease-ul

### ICMP (Internet Control Message Protocol)

ICMP facilitează diagnosticarea rețelei și raportarea erorilor. Tipuri cheie:

- **Echo Request/Reply (Tip 8/0)**: Folosit de ping
- **Destination Unreachable (Tip 3)**: Indică eșecuri de rutare
- **Time Exceeded (Tip 11)**: TTL expirat, folosit de traceroute
- **Redirect (Tip 5)**: Sugerează o rută mai bună

### NDP (Neighbor Discovery Protocol)

Înlocuitorul ARP pentru IPv6, furnizând: Router Discovery, Prefix Discovery, Neighbor Discovery și SLAAC.

---

## Software-Defined Networking (SDN)

### Arhitectură

SDN separă fundamental controlul rețelei de redirecționarea datelor:

**Planul de control**: Inteligență centralizată care ia decizii de redirecționare
- Rulează pe servere commodity
- Menține viziunea globală a rețelei
- Implementează algoritmi de rutare și politici

**Planul de date**: Redirecționare distribuită care mută pachetele
- Rulează pe switch-uri/routere
- Execută regulile furnizate de controller
- Operează la viteza liniei

**Interfața Southbound**: Protocol între controller și switch-uri (de obicei OpenFlow)

**Interfața Northbound**: API pentru aplicații pentru a programa comportamentul rețelei

### Protocolul OpenFlow

OpenFlow definește cum comunică controllerele cu switch-urile. Concepte cheie:

**Tabel de fluxuri**: Fiecare switch menține una sau mai multe tabele de fluxuri conținând reguli

**Intrare de flux**: Criterii de potrivire asociate cu acțiuni
- **Câmpuri de potrivire**: IP sursă/destinație, porturi, protocoale, VLAN-uri etc.
- **Acțiuni**: Ieșire pe port, drop, modificare headere, trimitere la controller
- **Prioritate**: Regulile cu prioritate mai mare se potrivesc primele
- **Contoare**: Statistici pachete/octeți

**Table-Miss**: Pachetele care nu se potrivesc cu nicio regulă declanșează acțiunea implicită

### Beneficiile SDN

- **Control centralizat**: Un singur punct de configurare și vizibilitate
- **Programabilitate**: Comportamentul rețelei definit în software
- **Independență de vendor**: Interfețe southbound standardizate
- **Inovație rapidă**: Funcții noi fără upgrade-uri hardware
- **Control fin**: Politici per-flux

### Provocările SDN

- **Scalabilitate**: Controller-ul trebuie să gestioneze toate evenimentele rețelei
- **Consistență**: Asigurarea politicii uniforme pe switch-uri distribuite
- **Latență**: Primele pachete ale fluxurilor implică round-trip la controller
- **Securitate**: Controller-ul devine o țintă critică de atac

---

## Referințe

1. Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (ediția a 7-a). Pearson.
2. RFC 1918 – Alocarea adreselor pentru rețele private
3. RFC 3022 – Translator tradițional de adrese de rețea IP
4. RFC 4861 – Neighbor Discovery pentru IP versiunea 6
5. RFC 2131 – Dynamic Host Configuration Protocol
6. Open Networking Foundation (2015). *OpenFlow Switch Specification* Versiunea 1.3.5

---

*Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de ing. dr. Antonio Clim*
