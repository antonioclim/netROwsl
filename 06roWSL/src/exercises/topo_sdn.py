#!/usr/bin/env python3
"""
Seminar 6 – Topologie Mininet: SDN cu OpenFlow 1.3

Topologie:
    h1 (10.0.6.11) ────┐
                       │
    h2 (10.0.6.12) ────┼──── s1 (OVS) ←───── Controller (OS-Ken)
                       │          ↑
    h3 (10.0.6.13) ────┘      OpenFlow 1.3

Toate hosturile sunt în aceeași subrețea (10.0.6.0/24).
Switch-ul s1 este controlat de un controller extern (OS-Ken) prin OpenFlow.

Politică așteptată (implementată în controller):
- ✓ h1 ↔ h2: PERMITE (tot traficul)
- ✗ * → h3: BLOCHEAZĂ (implicit, cu excepții configurabile)
- ? UDP → h3: CONFIGURABIL în controller

Scop educațional:
- Înțelegerea separării planului de control / planului de date
- Observarea instalării fluxurilor de la controller
- Analizarea tabelei de fluxuri cu ovs-ofctl
- Experimentarea cu politici de permitere/blocare per protocol

Utilizare:
    # Terminal 1 - pornește controller-ul
    osken-manager seminar/python/controllers/sdn_policy_controller.py

    # Terminal 2 - pornește topologia
    sudo python3 topo_sdn.py --cli

ing. dr. Antonio Clim | ASE-CSIE 2025-2026
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTURI
# ═══════════════════════════════════════════════════════════════════════════════

import argparse
import sys

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURARE_HOSTURI
# ═══════════════════════════════════════════════════════════════════════════════

# Format: (nume, ip/prefix, descriere)
HOSTURI_SDN = [
    ("h1", "10.0.6.11/24", "acces complet"),
    ("h2", "10.0.6.12/24", "server"),
    ("h3", "10.0.6.13/24", "acces restricționat"),
    # TODO: [TEMA 2] Adaugă h4 cu IP 10.0.6.14/24
    # Hint: Actualizează și controller-ul pentru noua politică
    # ("h4", "10.0.6.14/24", "reguli personalizate"),
]


# ═══════════════════════════════════════════════════════════════════════════════
# INSTALARE_FLUXURI_STATICE
# ═══════════════════════════════════════════════════════════════════════════════

def instaleaza_fluxuri_statice(net: Mininet) -> None:
    """Instalează un set minimal de reguli OpenFlow folosind ovs-ofctl.

    Motivație:
    - os-ken 4.0.0 a eliminat instrumentele CLI (osken-manager) și modulele os_ken.cmd.*,
      deci un controller extern nu este întotdeauna disponibil în VM-urile studenților.
    - Pentru Săptămâna 6 vrem totuși comportament determinist pentru exercițiile de politici.

    Politica implementată pe switch-ul s1 (OpenFlow 1.3):
    - h1 <-> h2: PERMITE (ICMP și ARP)
    - h1 -> h3: BLOCHEAZĂ (ICMP)
    - h2 -> h3: PERMITE (ICMP)
    - restul: NORMAL (acționează ca un switch simplu de învățare)
    """
    s1 = net.get("s1")
    
    # Obține hosturile existente
    hosturi = [(nume, ip, desc) for nume, ip, desc in HOSTURI_SDN]
    h1 = net.get("h1")
    h2 = net.get("h2")
    h3 = net.get("h3")

    # Mapează interfața hostului la numărul portului switch-ului
    p_h1 = s1.ports[h1.intf()].port_no
    p_h2 = s1.ports[h2.intf()].port_no
    p_h3 = s1.ports[h3.intf()].port_no

    def ofctl(cmd: str) -> None:
        s1.cmd(f"ovs-ofctl -O OpenFlow13 {cmd} s1")

    # Pornește de la o stare curată
    ofctl("del-flows")

    # Comportament implicit: switch de învățare
    ofctl("add-flow 'priority=0,actions=NORMAL'")

    # Permite întotdeauna ARP pentru ca hosturile să poată rezolva adresele MAC
    ofctl(f"add-flow 'priority=100,arp,in_port={p_h1},actions=output:{p_h2},output:{p_h3}'")
    ofctl(f"add-flow 'priority=100,arp,in_port={p_h2},actions=output:{p_h1},output:{p_h3}'")
    ofctl(f"add-flow 'priority=100,arp,in_port={p_h3},actions=output:{p_h1},output:{p_h2}'")

    # Permite ICMP între h1 și h2
    ofctl(f"add-flow 'priority=200,icmp,in_port={p_h1},nw_dst=10.0.6.12,actions=output:{p_h2}'")
    ofctl(f"add-flow 'priority=200,icmp,in_port={p_h2},nw_dst=10.0.6.11,actions=output:{p_h1}'")

    # Blochează ICMP de la h1 la h3 (demonstrează politica)
    ofctl(f"add-flow 'priority=250,icmp,in_port={p_h1},nw_dst=10.0.6.13,actions=drop'")

    # Permite explicit ICMP de la h2 la h3 (astfel demonstrația are un caz contrastant)
    ofctl(f"add-flow 'priority=200,icmp,in_port={p_h2},nw_dst=10.0.6.13,actions=output:{p_h3}'")
    ofctl(f"add-flow 'priority=200,icmp,in_port={p_h3},nw_dst=10.0.6.12,actions=output:{p_h2}'")
    
    # TODO: [TEMA 2] Adaugă reguli pentru h4 dacă este adăugat
    # Exemple:
    # - Permite doar TCP port 80 de la h1 la h4
    # - Blochează tot traficul de la h4 la h1
    # Hint: ofctl(f"add-flow 'priority=200,tcp,in_port={p_h1},nw_dst=10.0.6.14,tp_dst=80,actions=output:{p_h4}'")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASA_TOPOLOGIE_SDN
# ═══════════════════════════════════════════════════════════════════════════════

class TopologieSDN(Topo):
    """
    Topologie SDN simplă: 3+ hosturi conectate la un switch OVS.
    
    Switch-ul este configurat să folosească OpenFlow 1.3 și să se conecteze
    la un controller extern pe portul 6633.
    """
    
    def build(self):
        # Switch OpenFlow
        s1 = self.addSwitch(
            "s1",
            cls=OVSSwitch,
            protocols="OpenFlow13"  # OpenFlow 1.3 explicit
        )
        
        # Hosturi
        for nume, ip, desc in HOSTURI_SDN:
            host = self.addHost(nume, ip=ip)
            self.addLink(host, s1)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_RAPID
# ═══════════════════════════════════════════════════════════════════════════════

def ruleaza_test_rapid(net: Mininet) -> int:
    """
    Rulează teste pentru a verifica politicile SDN.
    """
    h1, h2, h3 = net.get("h1", "h2", "h3")
    
    info("\n*** TEST 1: Ping h1 → h2 (PERMITE așteptat)\n")
    out1 = h1.cmd("ping -c 2 -W 3 10.0.6.12")
    ok1 = "0% packet loss" in out1 or " 2 received" in out1
    info(f"    Rezultat: {'OK (PERMITE)' if ok1 else 'EȘUAT'}\n")
    
    info("*** TEST 2: Ping h1 → h3 (BLOCHEAZĂ așteptat)\n")
    out2 = h1.cmd("ping -c 2 -W 3 10.0.6.13")
    ok2 = "100% packet loss" in out2 or " 0 received" in out2
    info(f"    Rezultat: {'OK (BLOCHEAZĂ)' if ok2 else 'EȘUAT - traficul a trecut!'}\n")
    
    info("\n*** Tabel fluxuri s1:\n")
    fluxuri = net.get("s1").cmd("ovs-ofctl -O OpenFlow13 dump-flows s1")
    info(fluxuri + "\n")
    
    if ok1 and ok2:
        info("*** TOATE TESTELE AU TRECUT ***\n")
        return 0
    else:
        info("*** UNELE TESTE AU EȘUAT ***\n")
        return 1


# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Punct de intrare principal."""
    parser = argparse.ArgumentParser(
        description="Topologie SDN cu OpenFlow 1.3"
    )
    parser.add_argument("--cli", action="store_true", help="Mod interactiv")
    parser.add_argument("--install-flows", action="store_true", help="Instalează reguli OpenFlow folosind ovs-ofctl (fără controller extern necesar)")
    parser.add_argument("--test", action="store_true", help="Test rapid")
    parser.add_argument(
        "--controller-ip", default="127.0.0.1",
        help="IP controller (implicit: 127.0.0.1)"
    )
    parser.add_argument(
        "--controller-port", type=int, default=6633,
        help="Port controller (implicit: 6633)"
    )
    args = parser.parse_args()
    
    topo = TopologieSDN()
    
    # Controller extern (OS-Ken)
    # Trebuie pornit separat: osken-manager ...
    controller = RemoteController(
        "c0",
        ip=args.controller_ip,
        port=args.controller_port
    )
    
    net = Mininet(
        topo=topo,
        controller=controller,
        switch=OVSSwitch,
        link=TCLink,
        autoSetMacs=True
    )
    
    net.start()

    # Opțional: instalează reguli OpenFlow statice direct (util când CLI-ul os-ken nu este disponibil)
    if args.install_flows:
        instaleaza_fluxuri_statice(net)

    
    try:
        info("\n" + "="*60 + "\n")
        info("  TOPOLOGIE SDN PORNITĂ\n")
        info(f"  Controller: {args.controller_ip}:{args.controller_port}\n")
        info("  \n")
        info("  Politici implementate:\n")
        info("    ✓ h1 ↔ h2: PERMITE\n")
        info("    ✗ h1 → h3: BLOCHEAZĂ (ICMP)\n")
        info("    ✓ h2 ↔ h3: PERMITE (ICMP)\n")
        info("  \n")
        info("  Comenzi utile:\n")
        info("    h1 ping 10.0.6.12\n")
        info("    h1 ping 10.0.6.13\n")
        info("    sh ovs-ofctl -O OpenFlow13 dump-flows s1\n")
        info("="*60 + "\n\n")
        
        if args.test:
            import time
            time.sleep(2)  # Așteaptă conexiunea la controller
            return ruleaza_test_rapid(net)
        elif args.cli:
            CLI(net)
        else:
            info("Topologia a pornit. Folosește --cli pentru modul interactiv.\n")
        
        return 0
    finally:
        net.stop()


# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    setLogLevel("info")
    sys.exit(main())
