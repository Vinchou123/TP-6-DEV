# TP6 DEV : Chat room

## I. Débuts avec l'asynchrone

### I. Faire joujou avec l'asynchrone

1. Premiers pas

🌞 sleep_and_print.py

```bash
[vince@ClientTP4 tp-dev-3]$ python sleep_and_print.py
0
1
2
3
4
5
6
7
8
9
0
1
2
3
4
5
6
7
8
9
```

🌞 sleep_and_print_async.py

```bash
[vince@ClientTP4 TP6]$ python sleep_and_print_async.py
0
0
1
1
2
2
3
3
4
4
5
5
6
6
7
7
8
8
9
9
```


2. Web Requests

🌞 web_sync.py

```bash
[vince@ClientTP4 tp-dev-3]$ python web_sync.py https://www.ynov.com
Le contenu a été écrit dans /tmp/web_page/page.html
```

🌞 web_async.py

```bash
[vince@ClientTP4 tp-dev-3]$ python web_async.py https://www.ynov.com
Le contenu a été écrit dans /tmp/web_page/page.html
```



🌞 web_sync_multiple.py

```bash
[vince@ClientTP4 tp-dev-3]$ python web_sync_multiple.py url.txt
Page téléchargée : https://www.ynov.com -> /tmp/web_pages/web_www.ynov.com.html
Page téléchargée : https://example.org -> /tmp/web_pages/web_example.org.html
Page téléchargée : https://www.thinkerview.com -> /tmp/web_pages/web_www.thinkerview.com.html
Page téléchargée : https://www.torproject.org -> /tmp/web_pages/web_www.torproject.org.html
Page téléchargée : https://www.wikipedia.org -> /tmp/web_pages/web_www.wikipedia.org.html
Page téléchargée : https://www.reddit.com -> /tmp/web_pages/web_www.reddit.com.html
Page téléchargée : https://www.github.com -> /tmp/web_pages/web_www.github.com.html
Page téléchargée : https://www.python.org -> /tmp/web_pages/web_www.python.org.html
Page téléchargée : https://www.medium.com -> /tmp/web_pages/web_www.medium.com.html
Page téléchargée : https://www.twitter.com -> /tmp/web_pages/web_www.twitter.com.html
```

🌞 web_async_multiple.py

```bash
[vince@ClientTP4 tp-dev-3]$ python web_async_multiple.py url.txt
Page téléchargée : https://www.torproject.org -> /tmp/web_pages/web_www.torproject.org.html
Page téléchargée : https://www.wikipedia.org -> /tmp/web_pages/web_www.wikipedia.org.html
Page téléchargée : https://www.python.org -> /tmp/web_pages/web_www.python.org.html
Page téléchargée : https://example.org -> /tmp/web_pages/web_example.org.html
Page téléchargée : https://www.thinkerview.com -> /tmp/web_pages/web_www.thinkerview.com.html
Page téléchargée : https://www.github.com -> /tmp/web_pages/web_www.github.com.html
Page téléchargée : https://www.medium.com -> /tmp/web_pages/web_www.medium.com.html
Page téléchargée : https://www.reddit.com -> /tmp/web_pages/web_www.reddit.com.html
Page téléchargée : https://www.twitter.com -> /tmp/web_pages/web_www.twitter.com.html
Page téléchargée : https://www.ynov.com -> /tmp/web_pages/web_www.ynov.com.html
```





🌞 Mesure !

Version synchrone
```bash
[vince@ClientTP4 tp-dev-3]$ python web_sync_multiple.py url.txt
Page téléchargée : https://www.ynov.com -> /tmp/web_pages/web_www.ynov.com.html
Page téléchargée : https://example.org -> /tmp/web_pages/web_example.org.html
Page téléchargée : https://www.thinkerview.com -> /tmp/web_pages/web_www.thinkerview.com.html
Page téléchargée : https://www.torproject.org -> /tmp/web_pages/web_www.torproject.org.html
Page téléchargée : https://www.wikipedia.org -> /tmp/web_pages/web_www.wikipedia.org.html
Page téléchargée : https://www.reddit.com -> /tmp/web_pages/web_www.reddit.com.html
Page téléchargée : https://www.github.com -> /tmp/web_pages/web_www.github.com.html
Page téléchargée : https://www.python.org -> /tmp/web_pages/web_www.python.org.html
Page téléchargée : https://www.medium.com -> /tmp/web_pages/web_www.medium.com.html
Page téléchargée : https://www.twitter.com -> /tmp/web_pages/web_www.twitter.com.html
Temps d'exécution : 5.83 secondes
```

Version asynchrone
```bash
[vince@ClientTP4 tp-dev-3]$ python web_async_multiple.py url.txt
Page téléchargée : https://www.thinkerview.com -> /tmp/web_pages/web_www.thinkerview.com.html
Page téléchargée : https://www.wikipedia.org -> /tmp/web_pages/web_www.wikipedia.org.html
Page téléchargée : https://www.torproject.org -> /tmp/web_pages/web_www.torproject.org.html
Page téléchargée : https://www.python.org -> /tmp/web_pages/web_www.python.org.html
Page téléchargée : https://www.github.com -> /tmp/web_pages/web_www.github.com.html
Page téléchargée : https://example.org -> /tmp/web_pages/web_example.org.html
Page téléchargée : https://www.medium.com -> /tmp/web_pages/web_www.medium.com.html
Page téléchargée : https://www.reddit.com -> /tmp/web_pages/web_www.reddit.com.html
Page téléchargée : https://www.twitter.com -> /tmp/web_pages/web_www.twitter.com.html
Page téléchargée : https://www.ynov.com -> /tmp/web_pages/web_www.ynov.com.html
Temps d'exécution asynchrone: 1.87 secondes
```

## II. Chat room

## 1. Intro

## 2. Première version

🌞 chat_server_ii_2.py

```bash
[vince@ServeurTP4 tp-dev-3]$ python chat_server_ii_2.py
Serving on ('10.2.2.2', 8888)
Message du client (10.2.2.222:47148): Hello
Réponse envoyée à 10.2.2.222:47148
```

🌞 chat_client_ii_2.py

```bash
[vince@ClientTP4 tp-dev-3]$ python chat_client_ii_2.py
Connecté au serveur ('10.2.2.2', 8888)
Réponse du serveur: Hello 10.2.2.222:47148
Fermeture de la connexion
```

## 3. Client asynchrone

🌞 chat_client_ii_3.py*

```bash
[vince@ClientTP6 TP-6-DEV]$ python chat_client_ii_3.py
Connecté au serveur 10.2.2.2:8888
Vous : salut !
Serveur : Message reçu : salut !
Vous : ^C
Arrêt de la saisie utilisateur.

Arrêt de la réception des messages.

Client arrêté par l'utilisateur.
Fermeture de la connexion.

Arrêt du client (CTRL + C).
```

```bash
[vince@Client2TP6 TP-6-DEV]$ python3 chat_client_ii_3.py
Connecté au serveur 10.2.2.2:8888
Vous : salut
Serveur : Message reçu : salut
Vous : ^C
Arrêt de la saisie utilisateur.

Arrêt de la réception des messages.

Client arrêté par l'utilisateur.
Fermeture de la connexion.

Arrêt du client (CTRL + C).
```


🌞 chat_server_ii_3.py

```bash
[vince@ServeurTP6 TP-6-DEV]$ python chat_server_ii_3.py
Serving on ('10.2.2.2', 8888)
Nouvelle connexion de ('10.2.2.223', 48628)
Nouvelle connexion de ('10.2.2.222', 40486)
Message received from 10.2.2.222:40486 : salut
Message received from 10.2.2.223:48628 : salut
Connexion terminée avec ('10.2.2.223', 48628)
Connexion fermée avec ('10.2.2.223', 48628)
Connexion terminée avec ('10.2.2.222', 40486)
Connexion fermée avec ('10.2.2.222', 40486)
^C
Serveur arrêté manuellement.
```



## 4. Un chat fonctionnel

🌞 chat_server_ii_4.py

```bash
[vince@ServeurTP6 TP-6-DEV]$ python chat_server_ii_4.py
Serving on ('10.2.2.2', 8888)
Nouvelle connexion de ('10.2.2.223', 32984)
Nouvelle connexion de ('10.2.2.222', 53632)
Message received from 10.2.2.222:53632 : salut
Message received from 10.2.2.223:32984 : coucou !
Message received from 10.2.2.223:32984 : tu va sn=bien ?
Message received from 10.2.2.222:53632 : ouui super !
^CConnexion annulée avec ('10.2.2.222', 53632)
Connexion annulée avec ('10.2.2.223', 32984)
Connexion fermée avec ('10.2.2.222', 53632)
Connexion fermée avec ('10.2.2.223', 32984)

Serveur arrêté manuellement.
```

```bash
[vince@ClientTP6 TP-6-DEV]$ python chat_client_ii_3.py
Connecté au serveur 10.2.2.2:8888
Vous : salut
Serveur : 10.2.2.223:32984 a dit : coucou !
Serveur : 10.2.2.223:32984 a dit : tu va sn=bien ?
Vous : ouui super !
Vous :
Connexion avec le serveur fermée.
^C
Arrêt de la saisie utilisateur.

Client arrêté par l'utilisateur.
Fermeture de la connexion.

Arrêt du client (CTRL + C).
```

```bash
[vince@Client2TP6 TP-6-DEV]$ python3 chat_client_ii_3.py
Connecté au serveur 10.2.2.2:8888
Serveur : 10.2.2.222:53632 a dit : salut
Vous : coucou !
Vous : tu va sn=bien ?
Serveur : 10.2.2.222:53632 a dit : ouui super !
Vous :
Connexion avec le serveur fermée.
^C
Arrêt de la saisie utilisateur.

Client arrêté par l'utilisateur.
Fermeture de la connexion.

Arrêt du client (CTRL + C).
```

## 5. Gérer des pseudos

🌞 chat_client_ii_5.py

```bash


🌞 chat_server_ii_5.py

```bash
[vince@ServeurTP6 TP-6-DEV]$ python chat_server_ii_5.py
Serving on ('10.2.2.2', 8888)
Connexion de ('10.2.2.223', 51056)
Connexion de ('10.2.2.222', 38672)
('10.2.2.223', 51056) est connecté avec le pseudo 'Vince'.
('10.2.2.222', 38672) est connecté avec le pseudo 'Jin'.
Message de Jin (('10.2.2.222', 38672)): salut !
Message de Vince (('10.2.2.223', 51056)): Salut !!
Message de Vince (('10.2.2.223', 51056)): Comment tu vas ?
Message de Jin (('10.2.2.222', 38672)): Bien et toi ?
Déconnexion de ('10.2.2.222', 38672) (Jin)
Connexion fermée avec ('10.2.2.222', 38672) (Jin)
Déconnexion de ('10.2.2.223', 51056) (Vince)
Connexion fermée avec ('10.2.2.223', 51056) (Vince)
^C
Serveur arrêté manuellement.
```
