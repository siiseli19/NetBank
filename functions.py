from datetime import date
import pandas as pd
import csv
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates


# Lukee saldon arvon csv filusta
def saldo():
    file = open("Saldo.csv")
    csvreader = csv.reader(file)
    header = next(csvreader)
    rows = []
    for row in csvreader:
        rows.append(row)
        tilin_saldo = (row[0])
        print("Tilisi saldo on: " + (tilin_saldo))
    file.close()


# Printtaa tilitapahtumat csv filusta
def tilitapahtumat():
    file = open("tilitapahtumat.csv")
    lines = file.readlines()
    for line in lines:
        print(line)
    file.close()


# Ottaa parametrina siirrettavan summan ja vahentaa sen Saldo-filusta.
# Tarkastaa etta summa < Saldo
# Paivittaa uuden saldon tiedostoon.
def tilisiirto(saaja, summa, pvm):
    file = open("Saldo.csv")
    csvreader = csv.reader(file)
    header = next(csvreader)
    rows = []
    for row in csvreader:
        rows.append(row)
    temp_saldo = float(row[0])

    if summa >= temp_saldo:
        print("Siirto epäonnistui, tilin kate ei riitä")
    else:
        temp_saldo = temp_saldo - summa  ##float muodossa
        row[0] = str(temp_saldo)  ##Back to string

        new_header = ['Saldo']
        data = pd.DataFrame(row, columns=new_header)
        data.to_csv('Saldo.csv', index=False)
        summa = str(summa)
        kirjaa_lokiin(summa, saaja, pvm)
        print('Siirto onnistui')


# Kirjaa uuden tapahtuman tilitapahtumat-filuun
# Parametreina summa, paivamaara ja saaja
def kirjaa_lokiin(summa, saaja, pvm):
    summa = '-' + summa
    with open('tilitapahtumat.csv', 'a', newline='') as filu:
        writer = csv.writer(filu)
        writer.writerow([pvm, saaja, summa])


# Piirtaa kaavion 'tilitapahtumat'-filusta
def seuraa_kulutusta():
    df = pd.read_csv('tilitapahtumat.csv')
    ajankohta = df['pvm']
    summa = df['summa']
    plt.plot_date(ajankohta, summa, linestyle='solid')
    plt.title('Kulutuskäyttäytyminen')
    plt.xlabel('Ajankohta')
    plt.ylabel('Summan suuruus')
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(5)
    plt.close()

#Parameteina lainan maara, maksuaika ja kk-tulot. Riskikartoitus siten, etta lainan kk-osuus ei yli 30% kk-tuloista.
#Uudessa versiossa jos hakemus lapi niin lisaa saldoon
#Hakee automaattisesti palkan tilitapahtumista.
def hae_lainaa(lainan_maara, maksuaika, kk_tulot):

    kuukaudet = 12
    vuosikorko = 10.18
    lainan_maara = float(lainan_maara)
    kk_tulot = float(kk_tulot)
    maksuaika = int(maksuaika)
    kk_maksuaika = maksuaika * kuukaudet
    lopullinen_summa = lainan_maara * (1.1018)**maksuaika
    kuukausi_era = lopullinen_summa / kk_maksuaika

    if kuukausi_era / kk_tulot >= 0.3:
        return print('Lainamaaralle '+str(lainan_maara)+ 'kuukausiera on:'+ str(kuukausi_era)+' ja lopullinen summa: '+str(lopullinen_summa))
    else:
        return print('Lainahakemus hylattiin, koska tulosi eivät riitä haettuun lainamaaraan')

#Ulkomaan maksu? Jos kylla, niin perii lisamaksun. Muuten normisiirto
#Pyytaa kayttajalta tiedon maasta johon maksu lahetetaan
#Vertaa RestrictedNations.csv
#def kyc(summa):