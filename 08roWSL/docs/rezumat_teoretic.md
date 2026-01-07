# Rezumat Teoretic — Săptămâna 8

> Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

## Nivelul Transport

Nivelul transport asigură comunicarea logică între procese care rulează pe gazde diferite. Spre deosebire de nivelul rețea care oferă comunicare între gazde, nivelul transport extinde această comunicare la nivel de proces prin intermediul porturilor.

### Servicii Principale

Nivelul transport oferă două tipuri fundamentale de servicii:

**Transfer fără conexiune (UDP)** — Oferă un serviciu simplu, best-effort, fără garanții de livrare. Mesajele pot fi pierdute, duplicate sau livrate în altă ordine.

**Transfer orientat pe conexiune (TCP)** — Oferă un flux de octeți fiabil, ordonat și cu control al erorilor. Garantează livrarea corectă a datelor.

## Transmission Control Protocol (TCP)

TCP este un protocol de nivel transport orientat pe conexiune care oferă transfer fiabil de date.

### Caracteristici TCP

TCP asigură multiplexarea și demultiplexarea prin utilizarea porturilor sursă și destinație. Fiecare segment TCP conține numere de secvență și de confirmare pentru a asigura livrarea ordonată și detectarea pierderilor.

Controlul fluxului previne supraîncărcarea receptorului prin mecanismul ferestrei glisante. Receptorul anunță dimensiunea bufferului disponibil, iar emițătorul limitează cantitatea de date neconfirmate.

Controlul congestiei previne supraîncărcarea rețelei prin algoritmi precum slow start și congestion avoidance. Emițătorul ajustează dinamic rata de transmisie în funcție de condițiile rețelei.

### Stabilirea Conexiunii (Three-Way Handshake)

Stabilirea unei conexiuni TCP urmează un protocol în trei pași. Clientul trimite un segment SYN cu numărul de secvență inițial. Serverul răspunde cu SYN-ACK, confirmând recepția și trimițând propriul număr de secvență. Clientul finalizează cu ACK, confirmând recepția răspunsului serverului.

Acest mecanism asigură că ambele părți sunt pregătite pentru comunicare și sincronizează numerele de secvență.

### Închiderea Conexiunii

Închiderea conexiunii folosește un schimb în patru pași. Oricare parte poate iniția închiderea trimițând FIN. Cealaltă parte confirmă cu ACK și poate continua să trimită date. Când este pregătită, trimite propriul FIN, care este confirmat cu ACK.

## User Datagram Protocol (UDP)

UDP este un protocol simplu, fără conexiune, care oferă multiplexare și verificare minimă a erorilor.

### Caracteristici UDP

UDP nu oferă garanții de livrare, ordonare sau detectare a duplicatelor. Aplicațiile care folosesc UDP trebuie să implementeze aceste funcționalități dacă sunt necesare.

Avantajul principal este overhead-ul redus, făcându-l potrivit pentru aplicații care tolerează pierderi sau care implementează propriile mecanisme de fiabilitate.

### Cazuri de Utilizare

UDP este preferat pentru DNS (interogări scurte), streaming media (tolerează pierderi), jocuri online (latență redusă critică) și VoIP (comunicare în timp real).

## HTTP peste TCP

HTTP utilizează TCP ca protocol de transport pentru a beneficia de transferul fiabil de date.

### De Ce TCP pentru HTTP

HTTP necesită livrarea corectă a fiecărui octet din cerere și răspuns. Paginile web, imaginile și alte resurse trebuie să ajungă integre. TCP asigură că datele corupte sau pierdute sunt retransmise.

Ordonarea este critică pentru reconstruirea corectă a conținutului. Antetele HTTP trebuie procesate înainte de corp, iar corpul trebuie să fie complet pentru a fi utilizabil.

### Evoluția HTTP

HTTP/1.0 folosea o conexiune TCP per cerere, generând overhead semnificativ din cauza handshake-urilor repetate.

HTTP/1.1 a introdus conexiuni persistente și pipelining, permițând reutilizarea conexiunilor TCP pentru multiple cereri.

HTTP/2 a adus multiplexarea fluxurilor pe o singură conexiune, eliminând blocajul head-of-line la nivel aplicație.

HTTP/3 folosește QUIC peste UDP pentru a elimina blocajul head-of-line la nivel transport și pentru a permite migrarea conexiunilor.

## Arhitectura Proxy Invers

Un proxy invers acționează ca intermediar între clienți și servere, acceptând cereri de la clienți și redirecționându-le către serverele backend.

### Beneficii

Echilibrarea încărcării distribuie traficul între multiple servere, îmbunătățind performanța și fiabilitatea. Algoritmii comuni includ round-robin, weighted round-robin, least connections și IP hash.

Terminarea TLS descarcă criptografia de la serverele backend, simplificând configurația și îmbunătățind performanța acestora.

Cache-ul la nivel de proxy reduce încărcarea backend-urilor pentru conținut static sau rar modificat.

Securitatea este îmbunătățită prin ascunderea infrastructurii interne și prin posibilitatea de a implementa rate limiting și filtrare.

### Antetele de Proxy

Când un proxy redirecționează cereri, informația despre clientul original poate fi pierdută. Antetele speciale păstrează această informație:

**X-Forwarded-For** conține adresa IP originală a clientului și lista de proxy-uri intermediare.

**X-Forwarded-Proto** indică protocolul original (HTTP sau HTTPS) folosit de client.

**X-Forwarded-Host** păstrează hostname-ul original din cererea clientului.

## TLS (Transport Layer Security)

TLS oferă securitate pentru comunicațiile de rețea prin criptare, autentificare și integritate.

### Obiective de Securitate

Confidențialitatea asigură că doar părțile autorizate pot citi datele transmise. Criptarea simetrică cu chei negociate securizează conținutul.

Autentificarea verifică identitatea serverului (și opțional a clientului) prin certificate digitale semnate de autorități de certificare.

Integritatea detectează orice modificare a datelor în tranzit prin coduri de autentificare a mesajelor (MAC).

### Handshake TLS

Negocierea TLS stabilește parametrii sesiunii securizate. Clientul și serverul agreează versiunea protocolului, algoritmii criptografici și schimbă materialul pentru generarea cheilor.

TLS 1.3 a simplificat semnificativ handshake-ul, reducându-l la un singur round-trip în cazul optim și oferind confidențialitate înainte (forward secrecy) implicit.

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (ed. 7). Pearson.
- RFC 793 — Transmission Control Protocol
- RFC 768 — User Datagram Protocol
- RFC 9110 — HTTP Semantics
- RFC 8446 — Transport Layer Security 1.3

---

*Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
