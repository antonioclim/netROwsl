#!/usr/bin/env python3
"""
Seminar 6 – Controller SDN (OS-Ken + OpenFlow 1.3)

Controller educațional pentru topologie SDN cu politici de securitate.

Arhitectură SDN:
┌─────────────────────────────────────────┐
│            Planul de Control            │
│  ┌─────────────────────────────────┐    │
│  │    Controller (acest fișier)   │    │
│  │   - Primește packet_in         │    │
│  │   - Decide politica            │    │
│  │   - Instalează fluxuri         │    │
│  └──────────────┬──────────────────┘    │
└─────────────────┼───────────────────────┘
                  │ OpenFlow 1.3
┌─────────────────┼───────────────────────┐
│            Planul de Date               │
│  ┌──────────────▼──────────────────┐    │
│  │      Switch OVS (s1)           │    │
│  │   - Tabel fluxuri (match→acțiune)   │
│  │   - Redirecționare hw/sw       │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘

Politica implementată:
- h1 (10.0.6.11) ↔ h2 (10.0.6.12): PERMITE (tot traficul)
- * → h3 (10.0.6.13): BLOCHEAZĂ (implicit)
- UDP → h3: CONFIGURABIL (vezi ALLOW_UDP_TO_H3)

Utilizare:
    osken-manager sdn_policy_controller.py
    
    # Opțional, cu depanare detaliată:
    osken-manager --verbose sdn_policy_controller.py
"""

from __future__ import annotations

from os_ken.base import app_manager
from os_ken.controller import ofp_event
from os_ken.controller.handler import (
    MAIN_DISPATCHER,
    CONFIG_DISPATCHER,
    set_ev_cls
)
from os_ken.ofproto import ofproto_v1_3
from os_ken.lib.packet import packet, ethernet, ipv4, arp


# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURARE EDUCAȚIONALĂ - studenții pot modifica aceste constante
# ═══════════════════════════════════════════════════════════════════════════

# Schimbă în True pentru a permite UDP către h3 (dar TCP rămâne blocat)
ALLOW_UDP_TO_H3 = False

# Adrese IP hosturi (corespund topologiei topo_sdn.py)
# Standard Săptămâna 6: 10.0.6.0/24
H1_IP = "10.0.6.11"
H2_IP = "10.0.6.12"
H3_IP = "10.0.6.13"

# Port de rezervă pentru h3 (în topologia noastră: portul 3)
H3_PORT_FALLBACK = 3

# Timeout pentru fluxurile instalate (secunde)
FLOW_IDLE_TIMEOUT = 60
FLOW_HARD_TIMEOUT = 0  # 0 = fără timeout hard


class SDNPolicyController(app_manager.OSKenApp):
    """
    Controller SDN cu politici de securitate per-host și per-protocol.
    
    Funcționare:
    1. La conectarea switch-ului: instalează regula table-miss
    2. La packet_in: învață MAC-urile, apoi decide:
       - ARP: flood/forward pentru operare L2
       - IPv4 h1↔h2: instalează fluxuri de permitere
       - IPv4 *→h3: instalează flux de blocare (sau permite UDP dacă e configurat)
       - Restul: switch de învățare L2 de bază
    """
    
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tabel de învățare: dpid → {mac → port}
        self.mac_to_port: dict[int, dict[str, int]] = {}
    
    # ───────────────────────────────────────────────────────────────────────
    # Handler eveniment: Switch conectat
    # ───────────────────────────────────────────────────────────────────────
    
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def on_switch_features(self, ev):
        """
        Apelat când switch-ul se conectează la controller.
        
        Instalăm regula table-miss cu prioritate 0:
        - Match: orice pachet (match gol)
        - Acțiune: trimite la controller (OFPP_CONTROLLER)
        
        Această regulă asigură că pachetele necunoscute ajung la controller
        pentru a fi procesate și a genera fluxuri specifice.
        """
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        # Match gol = potrivește orice
        match = parser.OFPMatch()
        
        # Acțiune: trimite la controller
        actions = [
            parser.OFPActionOutput(
                ofproto.OFPP_CONTROLLER,
                ofproto.OFPCML_NO_BUFFER
            )
        ]
        
        # Instalează cu prioritate minimă (0)
        self._add_flow(datapath, priority=0, match=match, actions=actions)
        
        self.logger.info(
            "Table-miss instalat pe dpid=%s (pachete→controller)", 
            datapath.id
        )
    
    # ───────────────────────────────────────────────────────────────────────
    # Ajutor: Instalare flux
    # ───────────────────────────────────────────────────────────────────────
    
    def _add_flow(
        self,
        datapath,
        priority: int,
        match,
        actions: list,
        buffer_id=None,
        idle_timeout: int = FLOW_IDLE_TIMEOUT,
        hard_timeout: int = FLOW_HARD_TIMEOUT
    ):
        """
        Instalează un flux în switch.
        
        Argumente:
            datapath: Switch-ul țintă
            priority: Prioritatea regulii (mai mare = verificată prima)
            match: Criterii de potrivire
            actions: Lista de acțiuni (goală = drop)
            buffer_id: ID buffer dacă pachetul e în switch
            idle_timeout: Șterge după X secunde de inactivitate
            hard_timeout: Șterge după X secunde (0 = niciodată)
        """
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        # Construiește instrucțiunile (wrapper în jurul acțiunilor)
        instructions = [
            parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS,
                actions
            )
        ]
        
        # Parametri flow_mod
        kwargs = dict(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=instructions,
            idle_timeout=idle_timeout,
            hard_timeout=hard_timeout,
        )
        
        # Dacă pachetul e în buffer, leagă-l de flux
        if buffer_id is not None and buffer_id != ofproto.OFP_NO_BUFFER:
            kwargs["buffer_id"] = buffer_id
        
        # Trimite mesajul flow_mod
        flow_mod = parser.OFPFlowMod(**kwargs)
        datapath.send_msg(flow_mod)
    
    # ───────────────────────────────────────────────────────────────────────
    # Ajutor: Învățare MAC
    # ───────────────────────────────────────────────────────────────────────
    
    def _learn_mac(self, dpid: int, mac: str, port: int) -> None:
        """Învață asocierea MAC → port pentru un switch."""
        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][mac] = port
    
    def _get_port(self, dpid: int, mac: str, fallback=None) -> int:
        """Obține portul pentru un MAC, sau fallback dacă e necunoscut."""
        return self.mac_to_port.get(dpid, {}).get(mac, fallback)
    
    # ───────────────────────────────────────────────────────────────────────
    # Handler eveniment: Packet-in (pachet necunoscut)
    # ───────────────────────────────────────────────────────────────────────
    
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def on_packet_in(self, ev):
        """
        Apelat când switch-ul trimite un pachet necunoscut.
        
        Flux de procesare:
        1. Extrage informații din pachet (MAC-uri, IP-uri)
        2. Învață MAC-ul sursă
        3. Gestionează ARP (flood/forward pentru operare L2)
        4. Gestionează IPv4 conform politicii:
           - h1↔h2: permite
           - *→h3: blochează (sau permite UDP)
           - restul: switch de învățare L2
        """
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        dpid = datapath.id
        in_port = msg.match["in_port"]
        
        # Parsează pachetul
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        
        src_mac = eth.src
        dst_mac = eth.dst
        
        # Învață MAC-ul sursă
        self._learn_mac(dpid, src_mac, in_port)
        
        # ─────────────────────────────────────────────────────────────────
        # Gestionare ARP: învățare + flood/forward
        # ─────────────────────────────────────────────────────────────────
        
        arp_pkt = pkt.get_protocol(arp.arp)
        if arp_pkt:
            # Log pentru depanare
            self.logger.debug(
                "ARP: %s → %s (op=%s)",
                arp_pkt.src_ip, arp_pkt.dst_ip, arp_pkt.opcode
            )
            
            # Determină portul de ieșire
            out_port = self._get_port(dpid, dst_mac, fallback=ofproto.OFPP_FLOOD)
            
            # Trimite pachetul (nu instalăm flux pentru ARP)
            actions = [parser.OFPActionOutput(out_port)]
            out = parser.OFPPacketOut(
                datapath=datapath,
                buffer_id=ofproto.OFP_NO_BUFFER,
                in_port=in_port,
                actions=actions,
                data=msg.data
            )
            datapath.send_msg(out)
            return
        
        # ─────────────────────────────────────────────────────────────────
        # Gestionare IPv4: aplică politica
        # ─────────────────────────────────────────────────────────────────
        
        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        if not ip_pkt:
            # Nu e IPv4, ignoră
            return
        
        src_ip = ip_pkt.src
        dst_ip = ip_pkt.dst
        proto = ip_pkt.proto  # 1=ICMP, 6=TCP, 17=UDP
        
        self.logger.info(
            "IPv4: %s → %s (proto=%s) in_port=%s",
            src_ip, dst_ip, proto, in_port
        )
        
        # ─────────────────────────────────────────────────────────────────
        # Politica 1: Permite h1 ↔ h2
        # ─────────────────────────────────────────────────────────────────
        
        if self._is_h1_h2_traffic(src_ip, dst_ip):
            out_port = self._get_port(dpid, dst_mac, fallback=ofproto.OFPP_FLOOD)
            actions = [parser.OFPActionOutput(out_port)]
            
            # Instalează flux pentru acest trafic
            match = parser.OFPMatch(
                eth_type=0x0800,
                ipv4_src=src_ip,
                ipv4_dst=dst_ip
            )
            self._add_flow(
                datapath,
                priority=10,
                match=match,
                actions=actions,
                buffer_id=msg.buffer_id if msg.buffer_id != ofproto.OFP_NO_BUFFER else None
            )
            
            # Trimite pachetul curent
            if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                self._send_packet_out(datapath, in_port, actions, msg.data)
            
            self.logger.info(
                "PERMITE: %s → %s (proto=%s) out_port=%s",
                src_ip, dst_ip, proto, out_port
            )
            return
        
        # ─────────────────────────────────────────────────────────────────
        # Politica 2: Gestionează traficul către h3
        # ─────────────────────────────────────────────────────────────────
        
        if dst_ip == H3_IP:
            # Caz special: UDP permis (dacă e configurat)
            if proto == 17 and ALLOW_UDP_TO_H3:
                out_port = self._get_port(dpid, dst_mac, fallback=H3_PORT_FALLBACK)
                actions = [parser.OFPActionOutput(out_port)]
                
                # Flux pentru UDP către h3
                match = parser.OFPMatch(
                    eth_type=0x0800,
                    ip_proto=17,
                    ipv4_dst=H3_IP
                )
                self._add_flow(
                    datapath,
                    priority=20,
                    match=match,
                    actions=actions,
                    buffer_id=msg.buffer_id if msg.buffer_id != ofproto.OFP_NO_BUFFER else None
                )
                
                if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                    self._send_packet_out(datapath, in_port, actions, msg.data)
                
                self.logger.info("PERMITE UDP → %s out_port=%s", H3_IP, out_port)
                return
            
            # Implicit: BLOCHEAZĂ (flux fără acțiuni)
            match_kwargs = dict(eth_type=0x0800, ipv4_dst=H3_IP)
            
            # Opțional: potrivește și pe protocol pentru a vedea reguli separate
            if proto in (1, 6, 17):  # ICMP, TCP, UDP
                match_kwargs["ip_proto"] = proto
            
            match = parser.OFPMatch(**match_kwargs)
            actions = []  # Listă goală = BLOCHEAZĂ
            
            self._add_flow(
                datapath,
                priority=30,
                match=match,
                actions=actions,
                buffer_id=msg.buffer_id if msg.buffer_id != ofproto.OFP_NO_BUFFER else None
            )
            
            self.logger.info(
                "BLOCHEAZĂ: → %s (proto=%s)",
                H3_IP, proto
            )
            return
        
        # ─────────────────────────────────────────────────────────────────
        # Implicit: Switch de învățare L2
        # ─────────────────────────────────────────────────────────────────
        
        out_port = self._get_port(dpid, dst_mac, fallback=ofproto.OFPP_FLOOD)
        actions = [parser.OFPActionOutput(out_port)]
        
        # Instalează flux doar dacă știm portul
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst_mac)
            self._add_flow(
                datapath,
                priority=1,
                match=match,
                actions=actions,
                buffer_id=msg.buffer_id if msg.buffer_id != ofproto.OFP_NO_BUFFER else None
            )
        
        # Trimite pachetul
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            self._send_packet_out(datapath, in_port, actions, msg.data)
    
    # ───────────────────────────────────────────────────────────────────────
    # Ajutoare private
    # ───────────────────────────────────────────────────────────────────────
    
    def _is_h1_h2_traffic(self, src_ip: str, dst_ip: str) -> bool:
        """Verifică dacă traficul este între h1 și h2."""
        return (
            (src_ip == H1_IP and dst_ip == H2_IP) or
            (src_ip == H2_IP and dst_ip == H1_IP)
        )
    
    def _send_packet_out(self, datapath, in_port: int, actions: list, data: bytes):
        """Trimite un pachet individual prin switch."""
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=ofproto.OFP_NO_BUFFER,
            in_port=in_port,
            actions=actions,
            data=data
        )
        datapath.send_msg(out)
