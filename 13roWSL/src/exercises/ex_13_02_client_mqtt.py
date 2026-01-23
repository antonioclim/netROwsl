#!/usr/bin/env python3
"""
================================================================================
Exercițiul 2: Client MQTT cu Suport TLS
================================================================================
S13 - IoT și Securitate în Rețelele de Calculatoare

OBIECTIVE PEDAGOGICE:
1. Înțelegerea protocolului MQTT și modelului publish/subscribe
2. Implementarea comunicației cu broker-ul MQTT
3. Configurarea conexiunilor TLS pentru securitate
4. Înțelegerea nivelurilor QoS (Quality of Service)

UTILIZARE:
    # Abonare la topic
    python3 ex_13_02_client_mqtt.py --mod subscribe --topic "senzori/#" --broker localhost --port 1883
    
    # Publicare mesaj
    python3 ex_13_02_client_mqtt.py --mod publish --topic "senzori/temp" --mesaj "23.5" --broker localhost
    
    # Conexiune TLS
    python3 ex_13_02_client_mqtt.py --mod subscribe --topic "#" --broker localhost --port 8883 --tls --ca-cert certs/ca.crt

Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix
================================================================================
"""

import argparse
import json
import ssl
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("[EROARE] Biblioteca paho-mqtt nu este instalată!")
    print("         Instalați cu: pip install paho-mqtt")
    sys.exit(1)


# ==============================================================================
# ==============================================================================
# 🔮 PREDICȚIE - RĂSPUNDE ÎNAINTE DE A RULA CODUL
# ==============================================================================
#
# Înainte de a executa acest client MQTT, răspunde la următoarele întrebări:
#
# 1. COD CONECTARE: Ce cod de retur (rc) vei primi la conectare reușită?
#    A) 0 - Conexiune acceptată
#    B) 1 - Protocol incorect
#    C) 4 - Credențiale invalide
#    Răspuns corect: A (rc=0)
#
# 2. WILDCARDS: Dacă te abonezi la "senzori/#", vei primi mesaje de pe:
#    A) Doar "senzori/"
#    B) "senzori/temp", "senzori/umiditate", "senzori/camera1/temp"
#    C) Toate topicurile din sistem
#    Răspuns corect: B (# înlocuiește oricâte niveluri SUB "senzori/")
#
# 3. TLS: Ce diferență vei observa în Wireshark între portul 1883 și 8883?
#    Pe 1883: _______________
#    Pe 8883: _______________
#
# 4. QoS: Dacă publici cu QoS 2 și conexiunea cade, mesajul:
#    A) Se pierde
#    B) Ajunge exact o dată când conexiunea revine
#    C) Poate ajunge de mai multe ori
#    Răspuns corect: B
#
# După rulare, verifică predicțiile și notează diferențele!
# ==============================================================================

# CONSTANTE ȘI CONFIGURARE
# ==============================================================================

class Culori:
    ROSU = "\033[91m"
    VERDE = "\033[92m"
    GALBEN = "\033[93m"
    ALBASTRU = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


# Dezactivează culorile când nu este TTY
try:
    if not sys.stdout.isatty():
        for attr in ['ROSU', 'VERDE', 'GALBEN', 'ALBASTRU', 'CYAN', 'RESET', 'BOLD']:
            setattr(Culori, attr, "")
except Exception:
    pass


# ==============================================================================
# CALLBACK-URI MQTT
# ==============================================================================

def la_conectare(client, userdata, flags, rc, properties=None):
    """Callback la conectare cu broker-ul."""
    coduri_retur = {
        0: "Conexiune acceptată",
        1: "Protocol incorect",
        2: "Client ID invalid",
        3: "Server indisponibil",
        4: "Credențiale invalide",
        5: "Neautorizat"
    }
    
    mesaj = coduri_retur.get(rc, f"Cod necunoscut: {rc}")
    
    if rc == 0:
        print(f"{Culori.VERDE}[CONECTAT]{Culori.RESET} {mesaj}")
        
        # Dacă suntem în mod subscribe, ne abonam la topic
        if userdata and userdata.get('mod') == 'subscribe':
            topic = userdata.get('topic', '#')
            qos = userdata.get('qos', 0)
            client.subscribe(topic, qos)
            print(f"{Culori.CYAN}[ABONAT]{Culori.RESET} Topic: {topic} (QoS {qos})")
    else:
        print(f"{Culori.ROSU}[EROARE]{Culori.RESET} {mesaj}")


def la_deconectare(client, userdata, rc, properties=None):
    """Callback la deconectare."""
    if rc == 0:
        print(f"{Culori.GALBEN}[DECONECTAT]{Culori.RESET} Deconectare normală")
    else:
        print(f"{Culori.ROSU}[DECONECTAT]{Culori.RESET} Neașteptat (cod: {rc})")


def la_mesaj(client, userdata, msg):
    """Callback la primirea unui mesaj."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    
    try:
        # Încearcă să decodeze ca JSON
        payload = json.loads(msg.payload.decode('utf-8'))
        payload_str = json.dumps(payload, indent=2)
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Tratează ca text simplu
        try:
            payload_str = msg.payload.decode('utf-8')
        except UnicodeDecodeError:
            payload_str = msg.payload.hex()
    
    print(f"\n{Culori.VERDE}[MESAJ]{Culori.RESET} {timestamp}")
    print(f"  Topic: {Culori.CYAN}{msg.topic}{Culori.RESET}")
    print(f"  QoS:   {msg.qos}")
    print(f"  Payload: {payload_str}")


def la_publicare(client, userdata, mid, reason_code=None, properties=None):
    """Callback la confirmarea publicării."""
    print(f"{Culori.VERDE}[PUBLICAT]{Culori.RESET} Mesaj ID: {mid}")


def la_abonare(client, userdata, mid, reason_codes=None, properties=None):
    """Callback la confirmarea abonării."""
    print(f"{Culori.CYAN}[CONFIRMAT]{Culori.RESET} Abonare confirmată (ID: {mid})")


# ==============================================================================
# FUNCȚII PRINCIPALE
# ==============================================================================

def creeaza_client(id_client: str, config: dict) -> mqtt.Client:
    """
    Creează și configurează un client MQTT.
    
    Args:
        id_client: Identificatorul clientului
        config: Dicționar cu configurația (mod, topic, qos, etc.)
    
    Returns:
        Instanță mqtt.Client configurată
    """
    # Folosim callback API versiunea 2 dacă este disponibilă
    try:
        client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=id_client,
            userdata=config
        )
    except (AttributeError, TypeError):
        # Versiune mai veche de paho-mqtt
        client = mqtt.Client(client_id=id_client, userdata=config)
    
    # Atașează callback-urile
    client.on_connect = la_conectare
    client.on_disconnect = la_deconectare
    client.on_message = la_mesaj
    client.on_publish = la_publicare
    client.on_subscribe = la_abonare
    
    return client


def configureaza_tls(client: mqtt.Client, ca_cert: str, 
                     client_cert: str = None, client_key: str = None):
    """
    Configurează TLS pentru client.
    
    Args:
        client: Instanța mqtt.Client
        ca_cert: Calea către certificatul CA
        client_cert: Calea către certificatul client (opțional)
        client_key: Calea către cheia privată client (opțional)
    """
    if not Path(ca_cert).exists():
        raise FileNotFoundError(f"Certificat CA nu a fost găsit: {ca_cert}")
    
    client.tls_set(
        ca_certs=ca_cert,
        certfile=client_cert,
        keyfile=client_key,
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLS_CLIENT
    )
    
    # Permite conexiuni la localhost cu certificat auto-semnat
    client.tls_insecure_set(True)
    
    print(f"{Culori.CYAN}[TLS]{Culori.RESET} Configurare TLS activată")
    print(f"      CA: {ca_cert}")


def mod_subscribe(client: mqtt.Client, broker: str, port: int, 
                  topic: str, qos: int, durata: int = 0):
    """
    Rulează clientul în mod subscribe.
    
    Args:
        client: Instanța mqtt.Client
        broker: Adresa broker-ului
        port: Portul broker-ului
        topic: Topic-ul la care să se aboneze
        qos: Nivelul QoS
        durata: Durata în secunde (0 = nelimitat)
    """
    print(f"\n{Culori.BOLD}MOD: SUBSCRIBE{Culori.RESET}")
    print(f"Broker: {broker}:{port}")
    print(f"Topic:  {topic}")
    print(f"QoS:    {qos}")
    print("-" * 40)
    print("Apăsați Ctrl+C pentru a opri\n")
    
    try:
        client.connect(broker, port, keepalive=60)
        
        if durata > 0:
            client.loop_start()
            time.sleep(durata)
            client.loop_stop()
        else:
            client.loop_forever()
            
    except KeyboardInterrupt:
        print(f"\n{Culori.GALBEN}[INFO]{Culori.RESET} Întrerupt de utilizator")
    finally:
        client.disconnect()


def mod_publish(client: mqtt.Client, broker: str, port: int,
                topic: str, mesaj: str, qos: int, retine: bool = False):
    """
    Publică un mesaj și iese.
    
    Args:
        client: Instanța mqtt.Client
        broker: Adresa broker-ului
        port: Portul broker-ului
        topic: Topic-ul țintă
        mesaj: Mesajul de publicat
        qos: Nivelul QoS
        retine: Flag pentru mesaj reținut
    """
    print(f"\n{Culori.BOLD}MOD: PUBLISH{Culori.RESET}")
    print(f"Broker: {broker}:{port}")
    print(f"Topic:  {topic}")
    print(f"Mesaj:  {mesaj}")
    print(f"QoS:    {qos}")
    print("-" * 40)
    
    try:
        client.connect(broker, port, keepalive=60)
        client.loop_start()
        
        # Așteaptă conectarea
        time.sleep(1)
        
        # Publică mesajul
        info = client.publish(topic, mesaj, qos=qos, retain=retine)
        info.wait_for_publish()
        
        print(f"{Culori.VERDE}[SUCCES]{Culori.RESET} Mesaj publicat cu succes!")
        
    except Exception as e:
        print(f"{Culori.ROSU}[EROARE]{Culori.RESET} {e}")
    finally:
        client.loop_stop()
        client.disconnect()


# ==============================================================================
# FUNCȚIA PRINCIPALĂ
# ==============================================================================

def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Client MQTT cu Suport TLS - Laborator IoT și Securitate",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  # Abonare la toate topicurile senzorilor
  python ex_13_02_client_mqtt.py --mod subscribe --topic "senzori/#"
  
  # Publicare valoare temperatură
  python ex_13_02_client_mqtt.py --mod publish --topic "senzori/temp/camera1" --mesaj '{"temp": 23.5}'
  
  # Conexiune securizată TLS
  python ex_13_02_client_mqtt.py --mod subscribe --topic "#" --port 8883 --tls --ca-cert docker/configs/certs/ca.crt

Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix
        """
    )
    
    parser.add_argument("--mod", "-m", choices=["subscribe", "publish"], required=True,
                        help="Mod de operare: subscribe sau publish")
    parser.add_argument("--broker", "-b", default="localhost",
                        help="Adresa broker-ului MQTT (implicit: localhost)")
    parser.add_argument("--port", "-p", type=int, default=1883,
                        help="Portul broker-ului (implicit: 1883)")
    parser.add_argument("--topic", "-t", required=True,
                        help="Topic MQTT (suportă wildcards: + și #)")
    parser.add_argument("--mesaj", help="Mesajul de publicat (doar pentru mod publish)")
    parser.add_argument("--qos", type=int, choices=[0, 1, 2], default=0,
                        help="Nivel QoS: 0, 1, sau 2 (implicit: 0)")
    parser.add_argument("--id-client", default=None,
                        help="ID client personalizat")
    parser.add_argument("--durata", "-d", type=int, default=0,
                        help="Durata în secunde pentru subscribe (0=nelimitat)")
    
    # Opțiuni TLS
    parser.add_argument("--tls", action="store_true",
                        help="Activează conexiune TLS")
    parser.add_argument("--ca-cert", help="Calea către certificatul CA")
    parser.add_argument("--client-cert", help="Calea către certificatul client")
    parser.add_argument("--client-key", help="Calea către cheia privată client")
    
    args = parser.parse_args()
    
    # Validări
    if args.mod == "publish" and not args.mesaj:
        print(f"{Culori.ROSU}[EROARE]{Culori.RESET} Modul publish necesită --mesaj")
        return 1
    
    if args.tls and not args.ca_cert:
        # Încearcă să găsească certificatul implicit
        cale_implicita = Path(__file__).parent.parent.parent / "docker" / "configs" / "certs" / "ca.crt"
        if cale_implicita.exists():
            args.ca_cert = str(cale_implicita)
        else:
            print(f"{Culori.ROSU}[EROARE]{Culori.RESET} TLS activat dar --ca-cert nu este specificat")
            return 1
    
    print("=" * 50)
    print(f"{Culori.BOLD}CLIENT MQTT - LABORATOR SĂPTĂMÂNA 13{Culori.RESET}")
    print("IoT și Securitate în Rețelele de Calculatoare")
    print("=" * 50)
    
    # Generează ID client dacă nu e specificat
    id_client = args.id_client or f"lab13-client-{int(time.time())}"
    
    # Configurație pentru userdata
    config = {
        'mod': args.mod,
        'topic': args.topic,
        'qos': args.qos
    }
    
    # Creează clientul
    client = creeaza_client(id_client, config)
    
    # Configurează TLS dacă este cerut
    if args.tls:
        configureaza_tls(client, args.ca_cert, args.client_cert, args.client_key)
    
    # Rulează în modul specificat
    if args.mod == "subscribe":
        mod_subscribe(client, args.broker, args.port, args.topic, args.qos, args.durata)
    else:
        mod_publish(client, args.broker, args.port, args.topic, args.mesaj, args.qos)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
