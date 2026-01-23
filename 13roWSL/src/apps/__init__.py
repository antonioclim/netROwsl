"""
================================================================================
Aplicații Demonstrative - Laborator Săptămâna 13
================================================================================
IoT și Securitate în Rețelele de Calculatoare

Aplicații disponibile:

    controler_iot / iot_controller
        Controler IoT care primește date de la senzori via MQTT
        și execută acțiuni bazate pe reguli configurabile.

    senzor_iot / iot_senzor
        Simulator de senzor IoT care publică date periodice
        (temperatură, umiditate, etc.) pe topicuri MQTT.

    verificare_backdoor_ftp
        Utilitar pentru detectarea backdoor-ului simulat
        în serverul FTP vsftpd din laborator.

Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix
================================================================================
"""

__all__ = [
    "controler_iot",
    "iot_controller", 
    "senzor_iot",
    "iot_senzor",
    "verificare_backdoor_ftp",
]
