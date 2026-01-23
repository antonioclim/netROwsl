# Glosar de Termeni — Săptămâna 11

> Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

---

## Termeni Docker și Containerizare

| Termen | Definiție | Exemplu în Lab |
|--------|-----------|----------------|
| **Backend** | Server care procesează cererile din spatele unui load balancer | `web1`, `web2`, `web3` |
| **Container** | Instanță izolată a unei aplicații, rulând pe baza unei imagini | `s11_nginx_lb` |
| **Docker Compose** | Instrument pentru definirea și rularea aplicațiilor multi-container | `docker-compose.yml` |
| **Health Check** | Verificare periodică a stării unui serviciu | Bloc `healthcheck:` în compose |
| **Image** | Template read-only pentru crearea containerelor | `nginx:alpine` |
| **Network Bridge** | Rețea virtuală care permite comunicarea între containere | `s11_network` |
| **Port Mapping** | Mapare între portul host și portul container | `8080:80` |
| **Volume** | Stocare persistentă pentru date container | `portainer_data` |

---

## Termeni Load Balancing

| Termen | Definiție | Configurare Nginx |
|--------|-----------|-------------------|
| **Load Balancer** | Distribuitor de trafic pe mai multe servere | nginx cu `upstream` |
| **Round Robin** | Algoritm de distribuție ciclică (implicit) | (fără directivă specială) |
| **Least Connections** | Algoritm ce alege serverul cu cele mai puține conexiuni | `least_conn;` |
| **IP Hash** | Algoritm ce mapează același client la același server | `ip_hash;` |
| **Weighted** | Distribuție proporțională cu capacitatea | `server web1 weight=3;` |
| **Upstream** | Grup de servere backend în nginx | Bloc `upstream { }` |
| **Proxy Pass** | Directivă ce redirecționează cereri către upstream | `proxy_pass http://backend;` |
| **Failover** | Trecere automată la alt server când unul cade | `max_fails=3` |
| **Backup Server** | Server folosit doar când celelalte sunt indisponibile | `server web3 backup;` |

---

## Termeni DNS

| Termen | Definiție | Exemplu |
|--------|-----------|---------|
| **A Record** | Înregistrare ce mapează nume la adresă IPv4 | `google.com → 142.250.185.78` |
| **AAAA Record** | Înregistrare ce mapează nume la adresă IPv6 | `google.com → 2607:f8b0::` |
| **CNAME** | Alias pentru alt nume de domeniu | `www → example.com` |
| **MX Record** | Server de email pentru domeniu | `10 mail.google.com` |
| **NS Record** | Nameserver autoritativ pentru zonă | `ns1.google.com` |
| **TTL** | Time To Live — durata de viață a unei înregistrări în cache | 300 secunde |
| **Resolver** | Server DNS care face interogări recursive | 8.8.8.8 (Google DNS) |
| **Zone** | Porțiune a spațiului de nume DNS gestionată de o autoritate | `example.com` |

---

## Termeni FTP

| Termen | Definiție | Port |
|--------|-----------|:----:|
| **Canal Control** | Conexiune pentru comenzi și răspunsuri | 21 |
| **Canal Date** | Conexiune pentru transfer efectiv de date | dinamic |
| **Mod Activ (PORT)** | Serverul inițiază conexiunea de date către client | - |
| **Mod Pasiv (PASV)** | Clientul inițiază conexiunea de date către server | - |
| **RETR** | Comandă pentru descărcare fișier | - |
| **STOR** | Comandă pentru încărcare fișier | - |
| **LIST** | Comandă pentru listare director | - |

---

## Termeni SSH

| Termen | Definiție | Comandă |
|--------|-----------|---------|
| **Local Forwarding** | Tunel de la port local către server remote | `ssh -L 8080:db:5432 bastion` |
| **Remote Forwarding** | Tunel de la server remote către port local | `ssh -R 9000:localhost:3000 server` |
| **Dynamic Forwarding** | Proxy SOCKS prin SSH | `ssh -D 1080 server` |
| **Key-based Auth** | Autentificare cu cheie publică/privată | `ssh -i key.pem user@host` |
| **Agent Forwarding** | Partajare agent SSH prin conexiuni | `ssh -A bastion` |

---

## Termeni Rețelistică Generală

| Termen | Definiție | Exemplu |
|--------|-----------|---------|
| **NAT** | Network Address Translation — traducere adrese | Router casnic |
| **Firewall** | Sistem ce filtrează traficul de rețea | `iptables`, Windows Firewall |
| **Subnet** | Subdiviziune a unei rețele IP | `172.28.0.0/16` |
| **Gateway** | Punct de ieșire din rețea către altă rețea | `172.28.0.1` |
| **CIDR** | Notație pentru specificarea subrețelelor | `/24` = 255.255.255.0 |
| **Handshake** | Secvență de pachete pentru stabilirea conexiunii | TCP three-way handshake |
| **Latency** | Timpul necesar pentru a ajunge un pachet la destinație | ~10ms local, ~100ms intercontinental |
| **Throughput** | Cantitatea de date transferate pe unitatea de timp | 100 Mbps |

---

## Termeni Wireshark

| Termen | Definiție | Filtru Exemplu |
|--------|-----------|----------------|
| **Capture Filter** | Filtru aplicat în timpul capturii | `port 8080` |
| **Display Filter** | Filtru aplicat după captură | `http.request` |
| **Frame** | Unitate de date la nivel data link | - |
| **Packet** | Unitate de date la nivel rețea | - |
| **Segment** | Unitate de date TCP | - |
| **Datagram** | Unitate de date UDP | - |
| **pcap** | Format standard pentru capturi de pachete | `.pcap`, `.pcapng` |

---

## Termeni Specifici Acestui Laborator

| Termen | Definiție | Locație |
|--------|-----------|---------|
| **s11_nginx_lb** | Container Nginx load balancer | `docker/docker-compose.yml` |
| **s11_backend_N** | Containere backend (N = 1, 2, 3) | `docker/docker-compose.yml` |
| **s11_network** | Rețea Docker pentru acest laborator | Subnet: `172.28.0.0/16` |
| **Portainer** | Interfață web pentru gestionarea Docker | `http://localhost:9000` |

---

## Acronime

| Acronim | Expansiune | Traducere |
|---------|------------|-----------|
| **DNS** | Domain Name System | Sistem de Nume de Domenii |
| **FTP** | File Transfer Protocol | Protocol de Transfer Fișiere |
| **HTTP** | HyperText Transfer Protocol | Protocol de Transfer HiperText |
| **HTTPS** | HTTP Secure | HTTP Securizat |
| **IP** | Internet Protocol | Protocol Internet |
| **LB** | Load Balancer | Echilibror de Sarcină |
| **NAT** | Network Address Translation | Traducere Adrese de Rețea |
| **SSH** | Secure Shell | Shell Securizat |
| **TCP** | Transmission Control Protocol | Protocol de Control al Transmisiei |
| **TLS** | Transport Layer Security | Securitate la Nivel Transport |
| **TTL** | Time To Live | Timp de Viață |
| **UDP** | User Datagram Protocol | Protocol Datagramă Utilizator |
| **WSL** | Windows Subsystem for Linux | Subsistem Windows pentru Linux |

---

*Vezi [Analogii pentru Concepte](./analogii_concepte.md) pentru explicații detaliate cu metoda CPA.*

---

*Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix*
