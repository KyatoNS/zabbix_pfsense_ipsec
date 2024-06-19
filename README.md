# Monitoring des Tunnels IPsec PFsense avec Zabbix

## Dépendances

- Zabbix agent >= 6 (installable depuis le gestionnaire de paquets pfsense)
- sudo (installable depuis le gestionnaire de paquets pfsense)
- Zabbix Server >= 6.0.23
- check_ipsec.sh
- check_ipsec_traffic.sh
- zabbix-ipsec.py
- zabbix_sudoers

## Fonctionnement

Le script "zabbix-ipsec.py" récupère les identifiants (conX) et les informations des tunnels à partir d'une analyse du fichier de configuration.

Ensuite, le script "check_ipsec.sh", à partir des informations des tunnels, crée les déclencheurs dans Zabbix.

Le script "check_ipsec_traffic.sh" est utilisé par Zabbix pour récupérer les informations de trafic d'un tunnel.

## Installation

- Vous devez upload les fichiers check_ipsec.sh, check_ipsec_traffic.sh et zabbix-ipsec.py sur le pfsense dans le chemin suivant : /usr/local/bin/
  
- Installez le paquet sudo et zabbix agent depuis le gestionnaire de paquets pfsense. (System -> Package Manager)
  
- Copier le fichier zabbix_sudoers dans "/usr/local/etc/sudoers.d"
  
- Activer la configuration personnalisée dans sudo (System -> Sudo)
  

IMAGE

- Mettre les paramètres suvaints sur la page de configuration du Zabbix Agent sur Pfsense (Service -> Zabbix-Agent -> Options avancées)
  

```
UserParameter=ipsec.discover,/usr/local/bin/python3.8 /usr/local/bin/zabbix-ipsec.py
UserParameter=ipsec.tunnel[*],/usr/local/bin/sudo /usr/local/bin/check_ipsec.sh $1
UserParameter=ipsec.traffic[*],/usr/local/bin/sudo /usr/local/bin/check_ipsec_traffic.sh $1 $2
```

IMAGE

- Rendre executable les scripts pour tout les utilisateurs
  

```
chmod +x /usr/local/bin/zabbix-ipsec.py
chmod +x /usr/local/bin/check_ipsec.sh 
chmod +x /usr/local/bin/check_ipsec_traffic.sh 
```

- Importer le modèle ipsec_template.xml sur zabbix et l'attacher aux hôtes pfsense
