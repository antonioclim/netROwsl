# Lecturi Suplimentare: Săptămâna 9

> Resurse pentru Aprofundare
> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

---

## Cărți Recomandate

### Rețelistică Fundamentală

**Kurose, J. & Ross, K. - Computer Networking: A Top-Down Approach (ed. 8)**
- Capitol 2: Nivelul Aplicație
- Secțiunea despre FTP și protocoale client-server
- Excelent pentru înțelegerea modelului stratificat

**Tanenbaum, A. & Wetherall, D. - Computer Networks (ed. 5)**
- Capitol 7: Nivelul Aplicație
- Discuție detaliată despre nivelurile sesiune și prezentare
- Perspectivă istorică asupra modelului OSI

**Stevens, W.R. - TCP/IP Illustrated, Volume 1 (ed. 2)**
- Capitol 27: FTP - File Transfer Protocol
- Analiză detaliată a protocolului cu capturi de pachete
- Referință definitivă pentru implementatori

### Programare Rețele Python

**Rhodes, B. & Goerzen, J. - Foundations of Python Network Programming (ed. 3)**
- Capitol despre FTP și ftplib
- Exemple practice de implementare
- Bune practici pentru aplicații de rețea

---

## Specificații RFC

### FTP și Protocoale Conexe

| RFC | Titlu | Descriere |
|-----|-------|-----------|
| **RFC 959** | File Transfer Protocol | Specificația de bază FTP |
| RFC 2228 | FTP Security Extensions | Extensii de securitate |
| RFC 2428 | FTP Extensions for IPv6 | Suport IPv6 (EPSV/EPRT) |
| RFC 4217 | Securing FTP with TLS | FTPS (FTP peste TLS) |
| RFC 5797 | FTP Command and Extension Registry | Registrul comenzilor |

### Reprezentarea Datelor

| RFC | Titlu | Descriere |
|-----|-------|-----------|
| RFC 4506 | XDR: External Data Representation | Serializare binară standard |
| RFC 7049 | CBOR | Format binar concis |
| RFC 8259 | JSON | JavaScript Object Notation |

### Lectura RFC 959

RFC 959 este documentul fundamental pentru FTP. Secțiuni cheie:
- Secțiunea 3: Funcții de transfer de date
- Secțiunea 4: Comenzi de transfer fișiere
- Secțiunea 5: Comenzi de control acces
- Anexa I: Diagrama de stare a serverului

---

## Resurse Online

### Documentație Oficială

- **Python struct module**: https://docs.python.org/3/library/struct.html
- **Python ftplib**: https://docs.python.org/3/library/ftplib.html
- **Docker Compose**: https://docs.docker.com/compose/
- **Wireshark FTP**: https://wiki.wireshark.org/FTP

### Tutoriale și Ghiduri

- **Real Python - Socket Programming**: https://realpython.com/python-sockets/
- **Wireshark University**: https://www.wireshark.org/docs/
- **Docker Getting Started**: https://docs.docker.com/get-started/

### Instrumente Utile

- **pyftpdlib**: https://github.com/giampaolo/pyftpdlib
- **vsftpd**: https://security.appspot.com/vsftpd.html
- **FileZilla**: https://filezilla-project.org/

---

## Articole Academice

### Articole Fundamentale

**Cohen, D. (1981). "On Holy Wars and a Plea for Peace"**
- IEN 137, USC/ISI
- Articolul clasic despre endianness
- Introduce termenii "big-endian" și "little-endian"

**Postel, J. & Reynolds, J. (1985). "File Transfer Protocol"**
- RFC 959
- Specificația originală FTP
- Arhitectură și design protocol

### Articole despre Securitate FTP

**Ford-Hutchinson, P. (2005). "Securing FTP with TLS"**
- RFC 4217
- Cum se securizează FTP cu TLS/SSL
- Moduri implicite și explicite

---

## Cursuri Online

### Rețelistică

- **Coursera - Computer Networks** (University of Washington)
- **edX - Introduction to Computer Networking** (Stanford)
- **MIT OpenCourseWare 6.829** - Computer Networks

### Python pentru Rețele

- **Udemy - Python Network Programming**
- **LinkedIn Learning - Python: Network Programming**

---

## Proiecte Practice

### Pentru Experimentare

1. **Implementați un server FTP minimal**
   - Folosind doar socket-uri
   - Suport pentru USER, PASS, LIST, QUIT
   
2. **Construiți un protocol binar personalizat**
   - Definiți formatul mesajelor
   - Implementați serializare/deserializare
   - Adăugați verificare integritate

3. **Analizați trafic FTP real**
   - Capturați cu Wireshark
   - Identificați fazele sesiunii
   - Documentați schimbul de mesaje

### Proiecte Avansate

1. **Client FTP cu interfață grafică**
   - Folosind tkinter sau PyQt
   - Suport pentru navigare directoare
   - Transfer fișiere cu bară de progres

2. **Proxy FTP pentru monitorizare**
   - Interceptează și loghează comenzile
   - Analiză de trafic în timp real

---

## Comunități și Forumuri

- **Stack Overflow** - Tag-uri: `python`, `ftp`, `networking`
- **Reddit** - r/networking, r/learnpython
- **Discord** - Python, Networking communities
- **GitHub** - Proiecte open-source FTP

---

## Instrumente de Laborator

### Servere FTP pentru Testare

| Instrument | Platformă | Caracteristici |
|------------|-----------|----------------|
| pyftpdlib | Cross-platform | Python, ușor de configurat |
| vsftpd | Linux | Securizat, performant |
| ProFTPD | Linux | Configurabil, modular |
| FileZilla Server | Windows | GUI, ușor de folosit |

### Clienți FTP

| Client | Platformă | Caracteristici |
|--------|-----------|----------------|
| FileZilla | Cross-platform | GUI, SFTP/FTPS |
| lftp | Linux | CLI, scripting |
| WinSCP | Windows | GUI, SCP/SFTP |
| Cyberduck | macOS/Windows | GUI, cloud storage |

---

## Note Finale

Această listă nu este exhaustivă. Domeniul rețelisticii evoluează constant,
iar noi resurse apar regulat. Vă încurajăm să:

1. **Citiți RFC-urile** - Sunt sursa definitivă de informații
2. **Experimentați** - Cel mai bun mod de a învăța
3. **Contribuiți** - La proiecte open-source
4. **Împărtășiți** - Cunoștințele cu colegii

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
