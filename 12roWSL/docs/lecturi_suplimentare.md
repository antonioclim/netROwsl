# Lecturi Suplimentare - Săptămâna 12

> Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

## Specificații și Standarde

### SMTP și Email

| Resursă | Descriere | Link |
|---------|-----------|------|
| RFC 5321 | Simple Mail Transfer Protocol (SMTP) | https://tools.ietf.org/html/rfc5321 |
| RFC 5322 | Internet Message Format | https://tools.ietf.org/html/rfc5322 |
| RFC 2045 | MIME Partea 1: Format mesaje Internet | https://tools.ietf.org/html/rfc2045 |
| RFC 2046 | MIME Partea 2: Tipuri media | https://tools.ietf.org/html/rfc2046 |
| RFC 2047 | MIME Partea 3: Extensii pentru anteturi non-ASCII | https://tools.ietf.org/html/rfc2047 |
| RFC 2048 | MIME Partea 4: Proceduri de înregistrare | https://tools.ietf.org/html/rfc2048 |
| RFC 2049 | MIME Partea 5: Criterii de conformitate | https://tools.ietf.org/html/rfc2049 |
| RFC 3207 | SMTP STARTTLS | https://tools.ietf.org/html/rfc3207 |

### JSON-RPC

| Resursă | Descriere | Link |
|---------|-----------|------|
| Specificație JSON-RPC 2.0 | Documentul oficial al specificației | https://www.jsonrpc.org/specification |
| JSON-RPC History | Istoricul și evoluția protocolului | https://www.jsonrpc.org/specification_v1 |

### XML-RPC

| Resursă | Descriere | Link |
|---------|-----------|------|
| Specificație XML-RPC | Documentul original XML-RPC | http://xmlrpc.com/spec.md |
| XML-RPC Tutorial | Tutorial introductiv | http://xmlrpc.com/ |

### gRPC și Protocol Buffers

| Resursă | Descriere | Link |
|---------|-----------|------|
| Documentație gRPC | Documentația oficială gRPC | https://grpc.io/docs/ |
| Ghid Protocol Buffers | Ghidul pentru limbajul proto3 | https://developers.google.com/protocol-buffers/docs/proto3 |
| Ghid Stil Protobuf | Convenții de stil pentru .proto | https://developers.google.com/protocol-buffers/docs/style |
| gRPC Python | Tutorial gRPC pentru Python | https://grpc.io/docs/languages/python/ |

---

## Biblioteci Python

### Email și SMTP

| Bibliotecă | Descriere | Documentație |
|------------|-----------|--------------|
| smtplib | Bibliotecă SMTP inclusă în Python | https://docs.python.org/3/library/smtplib.html |
| email | Gestionare mesaje email | https://docs.python.org/3/library/email.html |
| aiosmtpd | Server SMTP asincron | https://aiosmtpd.readthedocs.io/ |

### RPC

| Bibliotecă | Descriere | Documentație |
|------------|-----------|--------------|
| xmlrpc.client | Client XML-RPC standard | https://docs.python.org/3/library/xmlrpc.client.html |
| xmlrpc.server | Server XML-RPC standard | https://docs.python.org/3/library/xmlrpc.server.html |
| grpcio | Implementare gRPC pentru Python | https://grpc.github.io/grpc/python/ |
| grpcio-tools | Instrumente pentru generare cod gRPC | https://pypi.org/project/grpcio-tools/ |
| jsonrpclib-pelix | Bibliotecă JSON-RPC pentru Python | https://pypi.org/project/jsonrpclib-pelix/ |

---

## Cărți Recomandate

### Rețelistică Generală

1. **Kurose, J. & Ross, K.** (2021). *Computer Networking: A Top-Down Approach* (ed. 8). Pearson.
   - Capitol 2: Nivelul aplicație
   - Secțiunea despre email și SMTP

2. **Tanenbaum, A. & Wetherall, D.** (2021). *Computer Networks* (ed. 6). Pearson.
   - Capitol 7: Nivelul aplicație

3. **Stevens, W. R.** (2003). *UNIX Network Programming, Volume 1* (ed. 3). Addison-Wesley.
   - Clasic pentru programarea de rețea

### Python pentru Rețele

4. **Rhodes, B. & Goerzen, J.** (2014). *Foundations of Python Network Programming* (ed. 3). Apress.
   - Capitol despre email și RPC

5. **Goerzen, J.** (2004). *Foundations of Python Network Programming*. Apress.
   - Fundamente ale programării de rețea în Python

### Sisteme Distribuite

6. **Kleppmann, M.** (2017). *Designing Data-Intensive Applications*. O'Reilly.
   - Capitol despre comunicarea între servicii

7. **Burns, B.** (2018). *Designing Distributed Systems*. O'Reilly.
   - Patterns pentru sisteme distribuite moderne

---

## Tutoriale Online

### Video

| Resursă | Descriere | Link |
|---------|-----------|------|
| gRPC Crash Course | Introducere rapidă în gRPC | YouTube - TechWorld with Nana |
| Protocol Buffers Tutorial | Tutorial Protocol Buffers | YouTube - Google Developers |
| SMTP Explained | Explicație vizuală SMTP | YouTube - PowerCert |

### Cursuri Interactive

| Resursă | Descriere | Link |
|---------|-----------|------|
| Wireshark Tutorial | Tutorial oficial Wireshark | https://www.wireshark.org/docs/wsug_html/ |
| gRPC Web Tutorial | Tutorial interactiv gRPC | https://grpc.io/docs/tutorials/ |

---

## Instrumente și Utilitare

### Testare Email

| Instrument | Descriere | Link |
|------------|-----------|------|
| MailHog | Server SMTP pentru testare | https://github.com/mailhog/MailHog |
| Mailtrap | Serviciu de testare email | https://mailtrap.io/ |
| smtp4dev | Server SMTP local pentru dezvoltare | https://github.com/rnwood/smtp4dev |

### Testare API/RPC

| Instrument | Descriere | Link |
|------------|-----------|------|
| Postman | Testare API | https://www.postman.com/ |
| grpcurl | curl pentru gRPC | https://github.com/fullstorydev/grpcurl |
| BloomRPC | GUI pentru testare gRPC | https://github.com/bloomrpc/bloomrpc |
| Insomnia | Client REST/GraphQL/gRPC | https://insomnia.rest/ |

### Analiză Rețea

| Instrument | Descriere | Link |
|------------|-----------|------|
| Wireshark | Analizor de protocoale | https://www.wireshark.org/ |
| tcpdump | Captură pachete în linie de comandă | https://www.tcpdump.org/ |
| ngrep | grep pentru rețea | https://github.com/jpr5/ngrep |

---

## Articole și Bloguri

### Comparații Protocoale

- *gRPC vs REST: Understanding gRPC, OpenAPI and REST* - Google Cloud Blog
- *Choosing between REST and gRPC* - Microsoft Architecture Center
- *JSON-RPC vs REST* - Nordic APIs

### Performanță

- *gRPC Performance Best Practices* - gRPC.io
- *Optimizing Protocol Buffers* - Google Developers Blog

### Securitate

- *Email Security Best Practices* - OWASP
- *Securing gRPC Services* - gRPC Security Documentation

---

## Comunități și Forumuri

| Comunitate | Descriere | Link |
|------------|-----------|------|
| Stack Overflow | Întrebări și răspunsuri | https://stackoverflow.com/questions/tagged/smtp |
| gRPC GitHub Discussions | Discuții despre gRPC | https://github.com/grpc/grpc/discussions |
| r/networking | Subreddit rețelistică | https://reddit.com/r/networking |
| Protocol Buffers Google Group | Grup de discuții | https://groups.google.com/g/protobuf |

---

## Exerciții Suplimentare

Pentru aprofundarea cunoștințelor, încercați:

1. **Implementați un server SMTP minimal** care salvează mesajele într-o bază de date SQLite

2. **Creați un serviciu gRPC** cu streaming bidirecțional pentru un chat simplu

3. **Comparați performanța** JSON-RPC vs gRPC pentru 10,000 de cereri

4. **Analizați în Wireshark** diferențele de overhead între protocoale

5. **Implementați autentificare** pentru un serviciu JSON-RPC folosind tokens JWT

---

*Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix*
