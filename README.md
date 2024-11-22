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