# Resurse Suplimentare

> Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

## Cărți Fundamentale

### Rețele de Calculatoare

1. **Kurose, J. F. & Ross, K. W. (2021)**
   *Computer Networking: A Top-Down Approach* (8th ed.)
   - Pearson
   - Abordare de sus în jos, de la aplicație la fizic
   - Capitole relevante: 2 (Stratul de Aplicație)

2. **Tanenbaum, A. S. & Wetherall, D. J. (2011)**
   *Computer Networks* (5th ed.)
   - Pearson
   - Perspectivă clasică, exhaustivă
   - Capitole relevante: 7 (Stratul de Aplicație)

### Programare Rețea

3. **Rhodes, B. & Goetzen, J. (2014)**
   *Foundations of Python Network Programming* (3rd ed.)
   - Apress
   - Python pentru programare de rețea
   - Exemple practice și moderne

4. **Stevens, W. R. (2003)**
   *UNIX Network Programming, Volume 1: The Sockets Networking API* (3rd ed.)
   - Addison-Wesley
   - Biblia programării socket
   - Referință fundamentală

---

## Documentație RFC

### FTP - File Transfer Protocol

| RFC | Titlu | An |
|-----|-------|-----|
| RFC 959 | File Transfer Protocol | 1985 |
| RFC 2228 | FTP Security Extensions | 1997 |
| RFC 2428 | FTP Extensions for IPv6 | 1998 |
| RFC 4217 | Securing FTP with TLS | 2005 |

**Lectură recomandată:** RFC 959 pentru fundamente, RFC 4217 pentru FTPS.

### DNS - Domain Name System

| RFC | Titlu | An |
|-----|-------|-----|
| RFC 1034 | Domain Names - Concepts and Facilities | 1987 |
| RFC 1035 | Domain Names - Implementation and Specification | 1987 |
| RFC 4033 | DNS Security Introduction and Requirements | 2005 |
| RFC 4034 | Resource Records for DNS Security Extensions | 2005 |
| RFC 4035 | Protocol Modifications for DNS Security Extensions | 2005 |
| RFC 8484 | DNS Queries over HTTPS (DoH) | 2018 |

**Lectură recomandată:** RFC 1034-1035 pentru fundamente, RFC 4033-4035 pentru DNSSEC.

### SSH - Secure Shell

| RFC | Titlu | An |
|-----|-------|-----|
| RFC 4251 | SSH Protocol Architecture | 2006 |
| RFC 4252 | SSH Authentication Protocol | 2006 |
| RFC 4253 | SSH Transport Layer Protocol | 2006 |
| RFC 4254 | SSH Connection Protocol | 2006 |

**Lectură recomandată:** RFC 4251 pentru arhitectură, RFC 4253-4254 pentru detalii.

**Unde găsiți RFC-urile:** https://www.rfc-editor.org/

---

## Resurse Nginx

### Documentație Oficială

- **Ghid pentru începători:** https://nginx.org/en/docs/beginners_guide.html
- **Modulul de echilibrare HTTP:** https://nginx.org/en/docs/http/ngx_http_upstream_module.html
- **Ghid proxy invers:** https://nginx.org/en/docs/http/ngx_http_proxy_module.html

### Tutoriale Practice

1. **DigitalOcean - Understanding Nginx**
   https://www.digitalocean.com/community/tutorials/understanding-nginx-server-and-location-block-selection-algorithms

2. **Nginx Blog - Load Balancing**
   https://www.nginx.com/resources/glossary/load-balancing/

---

## Instrumente și Biblioteci

### Python

| Bibliotecă | Scop | Link |
|------------|------|------|
| dnspython | Client DNS avansat | https://www.dnspython.org/ |
| paramiko | Client și server SSH | https://www.paramiko.org/ |
| pyftpdlib | Server FTP în Python | https://pypi.org/project/pyftpdlib/ |
| scapy | Manipulare pachete | https://scapy.net/ |
| requests | Client HTTP | https://docs.python-requests.org/ |

### Analiză Rețea

| Instrument | Scop | Link |
|------------|------|------|
| Wireshark | Analiză pachete (GUI) | https://www.wireshark.org/ |
| tshark | Wireshark CLI | Inclus cu Wireshark |
| tcpdump | Captură pachete Linux | https://www.tcpdump.org/ |
| mitmproxy | Proxy HTTP/HTTPS | https://mitmproxy.org/ |

### DNS

| Instrument | Scop | Link |
|------------|------|------|
| dig | Interogări DNS | Inclus în bind-utils |
| nslookup | Interogări DNS | Inclus în Windows/Linux |
| doggo | Client DNS modern | https://github.com/mr-karan/doggo |

---

## Cursuri Online

### Gratuite

1. **Stanford CS144 - Introduction to Computer Networking**
   - https://cs144.github.io/
   - Cursul clasic de rețele
   - Laboratoare practice

2. **Beej's Guide to Network Programming**
   - https://beej.us/guide/bgnet/
   - Ghid clasic pentru programare socket
   - Gratuit, online

### Plătite

3. **Pluralsight - DNS and BIND**
   - Administrare DNS în detaliu
   
4. **LinkedIn Learning - Learning Load Balancing**
   - Concepte și practici de echilibrare

---

## Articole și Bloguri

### Echilibrare de Sarcină

1. **Cloudflare - What is Load Balancing?**
   https://www.cloudflare.com/learning/performance/what-is-load-balancing/

2. **AWS - Elastic Load Balancing**
   https://aws.amazon.com/elasticloadbalancing/

3. **HAProxy Blog**
   https://www.haproxy.com/blog/

### DNS

1. **Cloudflare - What is DNS?**
   https://www.cloudflare.com/learning/dns/what-is-dns/

2. **Julia Evans - DNS Comics**
   https://wizardzines.com/zines/dns/
   - Explicații vizuale excelente

### SSH

1. **SSH.com - SSH Protocol**
   https://www.ssh.com/academy/ssh/protocol

---

## Traseu de Învățare Recomandat

### Nivel Începător (1-2 săptămâni)

1. Citiți capitolele relevante din Kurose & Ross
2. Parcurgeți tutorialele DigitalOcean pentru Nginx
3. Exersați cu exercițiile din acest kit

### Nivel Intermediar (2-4 săptămâni)

1. Studiați RFC 1034-1035 pentru DNS
2. Implementați un client/server FTP de la zero
3. Configurați un cluster Nginx de producție
4. Experimentați cu DNSSEC

### Nivel Avansat (1-2 luni)

1. Studiați toate RFC-urile SSH
2. Implementați un echilibror de sarcină cu health checks activi
3. Construiți un resolver DNS cu cache
4. Contribuiți la proiecte open-source (Nginx, dnspython)

---

## Proiecte Practice Sugerate

### Proiecte Mici

1. **Monitor de disponibilitate**
   - Verifică periodic servicii HTTP
   - Trimite alerte la căderi

2. **Client DNS cu cache**
   - Implementați un resolver local
   - Gestionați TTL-urile

3. **Proxy HTTP simplu**
   - Redirecționează cereri
   - Adaugă logging

### Proiecte Medii

4. **Echilibror de sarcină avansat**
   - Health checks activi
   - Multiple strategii
   - Interfață de management

5. **Server FTP securizat**
   - Suport FTPS
   - Gestionare utilizatori
   - Audit logging

### Proiecte Mari

6. **Sistem de load balancing distribuit**
   - Multiple noduri LB
   - Sincronizare stare
   - Failover automat

7. **Cluster DNS autoritar**
   - Zone multiple
   - Transfer de zone
   - Logging și metrici

---

## Comunități și Forumuri

- **Stack Overflow** - Întrebări tehnice
- **Reddit r/networking** - Discuții generale
- **Reddit r/sysadmin** - Administrare sisteme
- **Server Fault** - Administrare servere
- **Nginx Forum** - Comunitatea Nginx

---

*Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix*
