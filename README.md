# Projekt 3-  Výsledky voleb 2017 – Extrakce dat z volby.cz
Třetí projekt na Python Akademii od Engeta
## Popis projektu
Tento projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017. Odkaz k prohlédnutí najdete [zde](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)
## Instalace knihoven
Knihovny, které jsou použity v kódu jsou uložené v souboru ```requirements.txt```. Pro instalaci doporučuji použít nové virtuální prostředí s nainstalovaným manažerem a spustit následovně:
```
$ pip3 --version                   # ověřím verzi manažeru
$ pip3 install -r requirments.txt  # nainstalujeme knihovny
```
# Spuštění projektu
Spuštění souboru ```elections_scraper.py``` v rámci příkazového řádku požaduje dva povinné argumenty:
```
python elections_scraper.py <odkaz-uzemniho-celku> <vysledny-soubor>
```
Následně se vám stáhnou výsledky jako soubor s příponou ```.csv```
# Ukázka projektu
Výsledky hlasování pro okres Benešov:
1. argument: ```https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101```
2. argument: ```vysledky_benesov.csv```

Spuštění programu:
```
python elections_scraper.py " https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" "vysledky_benesov.csv"
```
Průběh stahování:
```
Načítání dat z:  https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
Ukládám výsledky do: vysledky_benesov.csv
Export dokončen.
```
Částečný výstup:
```
Obecní kód,Název,Registrovaní,Obálky vydané, .....
529303,Benešov,13 104,8 485,8 437,"12,46 %","0,11 %","0,02 %","7,39 %","0,03 %","9,50 %","7,07 %","....
532568,Bernartice,191,148,148,"2,70 %","0,00 %","0,00 %","11,48 %","0,00 %","4,05 %","4,72 %","....
530743,Bílkovice,170,121,118,"5,93 %","0,00 %","0,00 %","12,71 %","0,00 %","6,77 %","15,25 %","....
532380,Blažejovice,96,80,77,"7,79 %","0,00 %","0,00 %","6,49 %","0,00 %","3,89 %","14,28 %","0,00 %"....
...
```
# Rozšíření programu nad rámec zadání
Po spuštění se často objevovala chybová hláška ``` ConnectionResetError (10054, 'Stávající připojení bylo vynuceně ukončeno vzdáleným hostitelem', None, 10054, None)```
Musela jsem tedy najít řešení, jak udržet program v chodu (aby nespadl) a zároveň, aby dokázal obejít blokování serveru v případě velkého množství dotazů najednou (aby zadaný dotaz nevyhodnotil server jako dotaz bota) proto jsem se rozhodla přidat k dotazu časování. Skript tedy navíc obsahuje ```retry mechanismus``` v ```getr```, ```timeouty``` a malé zdržení mezi požadavky.
