# Glosar de Termeni - Săptămâna 10

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

---

## Termeni Tehnici (păstrați în engleză)

| Termen | Definiție | Exemplu în laborator |
|--------|-----------|---------------------|
| **Container** | Unitate izolată de execuție care include aplicația și toate dependențele necesare | `docker run nginx` creează un container din imaginea nginx |
| **Image** | Template read-only din care se creează containere; conține sistemul de fișiere și configurația | `python:3.11-alpine` - imagine Python minimală |
| **Volume** | Mecanism de persistență a datelor în afara ciclului de viață al containerului | `week10_ssh_data` păstrează datele SSH între reporniri |
| **Port Mapping** | Maparea unui port de pe host (gazdă) la un port din interiorul containerului | `-p 8080:80` expune portul 80 al containerului pe portul 8080 al host-ului |
| **Bridge Network** | Rețea virtuală Docker care permite comunicarea între containere | `week10_labnet` cu subnet 172.20.0.0/24 |
| **Health Check** | Verificare periodică a stării de sănătate a unui container | `wget -q --spider http://localhost:8000/` |
| **TLS Handshake** | Procesul de negociere a parametrilor pentru o conexiune securizată TLS | Client Hello → Server Hello → Certificate → Finished |
| **HATEOAS** | Hypermedia As The Engine Of Application State - principiu REST în care API-ul furnizează linkuri pentru navigare | `_links: { self: "/produse/1", delete: ... }` |
| **NXDOMAIN** | Non-Existent Domain - răspuns DNS care indică că domeniul cerut nu există | Răspuns pentru `dig xyz.lab.local` |
| **Passive Mode** | Mod FTP în care clientul inițiază ambele conexiuni (control și date) | Folosit pentru traversarea firewall-urilor |

---

## Acronime

| Acronim | Expansiune | Descriere |
|---------|------------|-----------|
| **HTTP** | Hypertext Transfer Protocol | Protocol de nivel aplicație pentru transferul resurselor web |
| **HTTPS** | HTTP Secure | HTTP cu strat de securitate TLS/SSL |
| **TLS** | Transport Layer Security | Protocol criptografic pentru securizarea comunicațiilor |
| **SSL** | Secure Sockets Layer | Predecesorul TLS (depreciat, dar termenul e încă folosit) |
| **DNS** | Domain Name System | Sistem distribuit pentru rezoluția numelor de domenii în adrese IP |
| **FTP** | File Transfer Protocol | Protocol pentru transferul fișierelor între sisteme |
| **SSH** | Secure Shell | Protocol pentru acces remote securizat și transfer de fișiere |
| **REST** | Representational State Transfer | Stil arhitectural pentru proiectarea API-urilor web |
| **API** | Application Programming Interface | Interfață pentru comunicarea între aplicații |
| **CRUD** | Create, Read, Update, Delete | Cele patru operații de bază pentru persistența datelor |
| **URI** | Uniform Resource Identifier | Identificator unic pentru o resursă |
| **URL** | Uniform Resource Locator | Subset al URI care include și locația (adresa) resursei |
| **JSON** | JavaScript Object Notation | Format text pentru reprezentarea datelor structurate |
| **YAML** | YAML Ain't Markup Language | Format de serializare a datelor, folosit în docker-compose |
| **WSL** | Windows Subsystem for Linux | Strat de compatibilitate pentru rularea Linux pe Windows |
| **NAT** | Network Address Translation | Tehnica de mapare a adreselor IP private la publice |
| **TTL** | Time To Live | Durata de viață a unei înregistrări DNS în cache |
| **RPC** | Remote Procedure Call | Paradigmă de comunicare în care clientul apelează proceduri pe server |

---

## Coduri de Stare HTTP

| Cod | Nume | Când apare |
|-----|------|------------|
| **200** | OK | Cererea a reușit |
| **201** | Created | Resursă creată cu succes (POST) |
| **204** | No Content | Succes fără corp de răspuns (DELETE) |
| **301** | Moved Permanently | Redirecționare permanentă |
| **302** | Found | Redirecționare temporară |
| **304** | Not Modified | Resursa nu s-a schimbat (cache valid) |
| **400** | Bad Request | Cerere malformată |
| **401** | Unauthorized | Autentificare necesară |
| **403** | Forbidden | Acces interzis |
| **404** | Not Found | Resursa nu există |
| **405** | Method Not Allowed | Metodă HTTP nepermisă pentru resursă |
| **500** | Internal Server Error | Eroare pe server |
| **502** | Bad Gateway | Gateway/proxy a primit răspuns invalid |
| **503** | Service Unavailable | Serviciul temporar indisponibil |

---

## Coduri de Răspuns DNS

| Cod | Nume | Semnificație |
|-----|------|--------------|
| **NOERROR** | No Error | Interogare procesată cu succes |
| **NXDOMAIN** | Non-Existent Domain | Domeniul nu există |
| **SERVFAIL** | Server Failure | Serverul DNS a întâmpinat o eroare |
| **REFUSED** | Query Refused | Serverul refuză să proceseze cererea |
| **NOTIMP** | Not Implemented | Tipul de cerere nu e suportat |

---

## Tipuri de Înregistrări DNS

| Tip | Nume | Utilizare | Exemplu |
|-----|------|-----------|---------|
| **A** | Address | Mapare nume → IPv4 | `web.lab.local → 172.20.0.10` |
| **AAAA** | IPv6 Address | Mapare nume → IPv6 | `web.lab.local → 2001:db8::1` |
| **CNAME** | Canonical Name | Alias pentru alt domeniu | `www.lab.local → web.lab.local` |
| **MX** | Mail Exchange | Server de email pentru domeniu | `lab.local → mail.lab.local` |
| **TXT** | Text | Informații text arbitrare | SPF, DKIM, verificări |
| **NS** | Name Server | Server DNS autoritativ | `lab.local → ns1.lab.local` |
| **SOA** | Start of Authority | Metadate despre zonă | Serial, refresh, retry |

---

## Comenzi Docker Frecvente

| Comandă | Descriere |
|---------|-----------|
| `docker ps` | Listează containerele active |
| `docker ps -a` | Listează toate containerele (inclusiv oprite) |
| `docker logs <container>` | Afișează jurnalele containerului |
| `docker exec -it <container> /bin/sh` | Deschide shell în container |
| `docker compose up -d` | Pornește serviciile în fundal |
| `docker compose down` | Oprește și elimină containerele |
| `docker compose down -v` | Oprește și elimină inclusiv volumele |
| `docker network ls` | Listează rețelele Docker |
| `docker network inspect <rețea>` | Detalii despre rețea |

---

## Comenzi de Diagnosticare Rețea

| Comandă | Scop | Exemplu |
|---------|------|---------|
| `curl` | Cereri HTTP din linia de comandă | `curl -v http://localhost:8000/` |
| `dig` | Interogări DNS | `dig @localhost -p 5353 web.lab.local` |
| `nc` (netcat) | Test conectivitate porturi | `nc -zv localhost 2222` |
| `ss` | Statistici socket-uri | `ss -tlnp` (porturi TCP în ascultare) |
| `tcpdump` | Captură pachete (CLI) | `tcpdump -i any port 8000` |

---

## Termeni Specifici Laboratorului

| Termen | Semnificație în context |
|--------|------------------------|
| `week10_labnet` | Rețeaua Docker bridge pentru laboratorul săptămânii 10 |
| `week10_web` | Containerul cu serverul HTTP Python |
| `week10_dns` | Containerul cu serverul DNS personalizat |
| `week10_ssh` | Containerul cu serverul OpenSSH |
| `week10_ftp` | Containerul cu serverul FTP pyftpdlib |
| `week10_debug` | Containerul utilitar cu instrumente de rețea |
| `labuser` / `labpass` | Credențiale pentru serverul SSH |
| `labftp` / `labftp` | Credențiale pentru serverul FTP |
| `stud` / `studstudstud` | Credențiale pentru Portainer |

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
