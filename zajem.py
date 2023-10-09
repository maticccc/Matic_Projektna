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

# zdaj funkcija iz vsake vrstice tabele naredi po en slovar z ustreznimi podatki
# potrebno je še, da vse slovarje dam v skupen seznam

def dodaj_slovarje_v_seznam(vrste):
    seznam = []
    for vrsta in vrste:
        seznam.append(izlusci_vse_podatke(vrsta))
    return seznam
# seznam, ki ga vrne funkcija je končen in vsebuje vse potrebne podatke za izdelavo csv datoteke

def prepisi_v_csv(seznam):
    naslovi_stolpcev = ['Drzava', 'Indeks stroskov', 'Mesecni dohodek', 'Indeks kupne moci']
    with open(csv_drzav, 'w', newline='') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=naslovi_stolpcev)
        writer.writeheader()
        for vrsta in seznam:
            writer.writerow(vrsta)

# manjka samo še funkcija, ki skupno izvede vse zgornje funkcije

def naredi_vse(url, datoteka):
    preberi_in_shrani_url(url, datoteka)
    vrstice = preberi_in_izlusci_vrstice(datoteka)
    koncni_seznam = dodaj_slovarje_v_seznam(vrstice)
    csv_dat = prepisi_v_csv(koncni_seznam) 

# na koncu še poženem zadnjo funkcijo, ki ustvari novo csv datoteko:

naredi_vse(url_spletne_strani, shrani_sem)
