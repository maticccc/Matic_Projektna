import requests
import csv
import re

url_spletne_strani = 'https://www.worlddata.info/cost-of-living.php'
shrani_sem = 'primerjava_drzav.html'
csv_drzav = 'drzave.csv'

def url_v_niz(url):
    try:
        vsebina = requests.get(url)
        if vsebina.status_code == 200:
            return vsebina.text
        else:
            raise ValueError(f'Prišlo je do napake: {vsebina.status_code}')
    except Exception:
        print(f'Napaka v prepoznavanju spletne strani')

def shrani_niz_v_datoteko(niz, datoteka):
    with open(datoteka, 'w', encoding='utf-8') as dat:
        dat.write(niz)


def preberi_in_shrani_url(url, datoteka):
    niz = url_v_niz(url)
    shrani_niz_v_datoteko(niz, datoteka)

