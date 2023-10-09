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
    return None

def preberi_in_shrani_url(url, datoteka):
    niz = url_v_niz(url)
    shrani_niz_v_datoteko(niz, datoteka)

preberi_in_shrani_url(url_spletne_strani, shrani_sem)

def preberi_datoteko(datoteka):
    with open(datoteka, 'r', encoding='utf-8') as dat:
        return dat.read()

def izlusci_vrstice(vsebina_strani):
    vzorec_vrstice = r'<tr>(.*?)</tr>'
    return re.findall(vzorec_vrstice, vsebina_strani, re.DOTALL)



def preberi_in_izlusci_vrstice(datoteka):
    besedilo = preberi_datoteko(datoteka)
    vrstice = izlusci_vrstice(besedilo)
    return vrstice

vrstice = preberi_in_izlusci_vrstice('primerjava_drzav.html')
# funckija vrne vrstice oblike <tr>...</tr>, kjer so zajeti podatki iz spletne strani

def izlusci_vse_podatke(vrstice_tabele):
    slovar = {}
    vzorec_drzava = r'">(.*?)</a>'
    drzave = re.findall(vzorec_drzava, vrstice_tabele)
    for drzava in drzave:
        slovar['Drzava'] = drzava
    vzorec_vseh_treh_stevil = r'<td>(.+?)</td>'
    stevila = re.findall(vzorec_vseh_treh_stevil, vrstice_tabele)
    slovar['Indeks stroskov'] = stevila[2]
    slovar['Mesecni dohodek'] = stevila[3]
    slovar['Indeks kupne moci'] = stevila[4]

    return slovar




