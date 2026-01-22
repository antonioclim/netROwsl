# Glosar de Termeni – Săptămâna 5

> Referință rapidă pentru termeni tehnici
> Laborator Rețele de Calculatoare – ASE, Informatică Economică

---

## Adresare IP

| Termen | Definiție | Exemplu |
|--------|-----------|---------|
| **CIDR** | Classless Inter-Domain Routing — notație prefix/lungime | `192.168.1.0/24` |
| **Prefix** | Numărul de biți din partea de rețea | `/24` = 24 biți rețea |
| **Mască de rețea** | Adresă care separă biții rețea de cei gazdă | `255.255.255.0` |
| **Mască wildcard** | Inversul măștii de rețea (folosită în ACL, OSPF) | `0.0.0.255` |
| **Adresa de rețea** | Prima adresă din bloc (biți gazdă = 0) | `192.168.1.0` |
| **Broadcast** | Ultima adresă din bloc (biți gazdă = 1) | `192.168.1.255` |
| **Gazde utilizabile** | Total adrese minus 2 (rețea + broadcast) | 254 pentru /24 |
| **Octet** | Grup de 8 biți (0-255 în zecimal) | `192` = `11000000` |

---

## Subnetare

| Termen | Definiție |
|--------|-----------|
| **FLSM** | Fixed Length Subnet Mask — împarte rețeaua în subrețele de dimensiune egală |
| **VLSM** | Variable Length Subnet Mask — permite subrețele de dimensiuni diferite |
| **Biți împrumutați** | Biți "furați" din partea de gazdă pentru a crea subrețele |
| **Salt (Increment)** | Diferența între adresele de rețea ale subrețelelor consecutive |
| **Supernet** | Agregarea mai multor rețele într-un singur prefix mai mare |

### Formule Cheie

```
Total adrese       = 2^(32 - prefix)
Gazde utilizabile  = 2^(32 - prefix) - 2
Salt între rețele  = 2^(32 - prefix)
Prefix pentru N gazde = 32 - ceil(log2(N + 2))
```

---

## IPv6

| Termen | Definiție | Exemplu |
|--------|-----------|---------|
| **Global Unicast** | Adrese publice rutabile pe Internet | `2001:db8::/32` |
| **Link-Local** | Adrese valide doar în rețeaua locală | `fe80::/10` |
| **Unique Local** | Echivalentul adreselor private IPv4 | `fc00::/7` |
| **SLAAC** | Stateless Address Autoconfiguration | Auto-configurare fără DHCP |
| **EUI-64** | Metodă de generare Interface ID din MAC | MAC → Interface ID |
| **Comprimare** | Eliminarea zerourilor și folosirea `::` | `2001:db8::1` |

### Reguli Comprimare IPv6

1. Zerourile din față ale grupului se omit: `0db8` → `db8`
2. Cel mai lung șir de grupuri zero devine `::` 
3. Doar O SINGURĂ secvență `::` permisă per adresă

---

## Docker și Containere

| Termen | Definiție |
|--------|-----------|
| **Container** | Instanță izolată a unei aplicații (împarte kernel-ul cu host-ul) |
| **Image** | Template read-only pentru crearea containerelor |
| **Volume** | Stocare persistentă atașată containerului |
| **Bridge network** | Rețea virtuală pentru comunicare între containere |
| **Port mapping** | Mapare port host → port container (`-p 8080:80`) |
| **docker-compose** | Instrument pentru definirea și rularea aplicațiilor multi-container |

### Diferențe Container vs VM

| Aspect | Container | Mașină Virtuală |
|--------|-----------|-----------------|
| Kernel | Împărțit cu host | Propriu |
| Pornire | Secunde | Minute |
| Dimensiune | MB | GB |
| Izolare | Procese | Hardware |

---

## Rețelistică Generală

| Termen | Definiție |
|--------|-----------|
| **TTL** | Time To Live — numărul maxim de hop-uri pentru un pachet |
| **MTU** | Maximum Transmission Unit — dimensiunea maximă a pachetului |
| **NAT** | Network Address Translation — traduce adrese private în publice |
| **Gateway** | Dispozitiv care conectează rețele diferite (de obicei router) |
| **ICMP** | Internet Control Message Protocol — folosit de ping, traceroute |
| **ARP** | Address Resolution Protocol — mapează IP la MAC |

---

## Comenzi Frecvente

### Docker

| Comandă | Scop |
|---------|------|
| `docker compose up -d` | Pornește stack-ul în background |
| `docker compose down` | Oprește și șterge containerele |
| `docker ps` | Listează containerele active |
| `docker logs <container>` | Afișează log-urile |
| `docker exec -it <container> bash` | Deschide shell în container |
| `docker network inspect <net>` | Detalii despre rețea |

### Linux/WSL

| Comandă | Scop |
|---------|------|
| `ip addr` | Afișează interfețele de rețea |
| `ping -c 3 <ip>` | Testează conectivitatea |
| `ss -tuln` | Listează porturile în ascultare |
| `traceroute <ip>` | Urmărește calea pachetelor |

### Windows PowerShell

| Comandă | Scop |
|---------|------|
| `wsl` | Intră în distribuția WSL implicită |
| `wsl --list -v` | Listează distribuțiile WSL |
| `ipconfig` | Afișează configurația de rețea |

---

## Acronime

| Acronim | Expansiune |
|---------|------------|
| CIDR | Classless Inter-Domain Routing |
| VLSM | Variable Length Subnet Mask |
| FLSM | Fixed Length Subnet Mask |
| NAT | Network Address Translation |
| DHCP | Dynamic Host Configuration Protocol |
| DNS | Domain Name System |
| TCP | Transmission Control Protocol |
| UDP | User Datagram Protocol |
| ICMP | Internet Control Message Protocol |
| ARP | Address Resolution Protocol |
| TTL | Time To Live |
| MTU | Maximum Transmission Unit |
| OSI | Open Systems Interconnection |
| RFC | Request For Comments |
| WSL | Windows Subsystem for Linux |

---

## Navigare Rapidă

| ← Anterior | Document | Următor → |
|------------|----------|-----------|
| [README](../README.md) | **Glosar** | [Rezumat Teoretic](rezumat_teorie.md) |

---

*Material pentru Laborator Rețele de Calculatoare – ASE București*
