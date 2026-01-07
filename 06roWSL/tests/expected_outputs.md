# Output-uri așteptate pentru exercițiile Săptămânii 6

> Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

## Exercițiul 1: Configurare NAT/PAT

### Output așteptat pentru tabela NAT

```
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination

Chain INPUT (policy ACCEPT)
target     prot opt source               destination

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination
MASQUERADE  all  --  192.168.1.0/24       0.0.0.0/0
```

### Output așteptat Observator NAT (partea server)

```
[Server Observator NAT]
Ascultă pe 203.0.113.2:5000
Așteaptă conexiuni...
------------------------------------------------------------
[2025-XX-XX XX:XX:XX] Conexiune de la 203.0.113.1:50001
            Mesaj: Salut de la h1

[2025-XX-XX XX:XX:XX] Conexiune de la 203.0.113.1:50002
            Mesaj: Salut de la h2
```

Notă: Ambele conexiuni apar ca venind de la 203.0.113.1 (IP-ul public NAT) cu porturi diferite.

## Exercițiul 2: Observare fluxuri SDN

### Tabel fluxuri așteptat (inițial)

```
 cookie=0x0, duration=Xs, table=0, n_packets=0, n_bytes=0, priority=0 actions=CONTROLLER:65535
```

### Tabel fluxuri așteptat (după trafic)

```
 cookie=0x0, duration=Xs, table=0, n_packets=N, n_bytes=M, priority=200,icmp,in_port=1,nw_dst=10.0.6.12 actions=output:2
 cookie=0x0, duration=Xs, table=0, n_packets=N, n_bytes=M, priority=200,icmp,in_port=2,nw_dst=10.0.6.11 actions=output:1
 cookie=0x0, duration=Xs, table=0, n_packets=N, n_bytes=M, priority=250,icmp,in_port=1,nw_dst=10.0.6.13 actions=drop
 cookie=0x0, duration=Xs, table=0, n_packets=0, n_bytes=0, priority=0 actions=CONTROLLER:65535
```

### Rezultate ping așteptate

```
# h1 → h2 (PERMITE)
PING 10.0.6.12 (10.0.6.12) 56(84) bytes of data.
64 bytes from 10.0.6.12: icmp_seq=1 ttl=64 time=X ms
64 bytes from 10.0.6.12: icmp_seq=2 ttl=64 time=X ms
--- 10.0.6.12 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss

# h1 → h3 (BLOCHEAZĂ)
PING 10.0.6.13 (10.0.6.13) 56(84) bytes of data.
--- 10.0.6.13 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss
```

## Exercițiul 3: Modificare politici

### Output așteptat după adăugarea regulii ICMP de permitere

```
# Adaugă regula
sh ovs-ofctl -O OpenFlow13 add-flow s1 "priority=300,icmp,nw_src=10.0.6.11,nw_dst=10.0.6.13,actions=output:3"

# Verifică că ping funcționează acum
h1 ping -c 2 10.0.6.13
PING 10.0.6.13 (10.0.6.13) 56(84) bytes of data.
64 bytes from 10.0.6.13: icmp_seq=1 ttl=64 time=X ms
64 bytes from 10.0.6.13: icmp_seq=2 ttl=64 time=X ms
--- 10.0.6.13 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss
```

---

*Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
