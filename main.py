from sys import exit as sysExit
from functions import saldo, tilitapahtumat, tilisiirto, seuraa_kulutusta, hae_lainaa
from datetime import date


# Kayttoliittyma josta ohjataan applikaatiota
# Pyorii kunnes kayttaja valitsee 'Q'
def user_interface():
    valinta = None
    while True:
        print("-------------------------------------------")
        print("Tervetuloa kayttamaan mobiilipankkia!")
        saldo()
        print("VALITSE TOIMINTO:")
        print("Tilisiirto -- S")
        print("Tilitapahtumat -- T")
        print("Hae lainaa -- H")
        print("Poistu -- Q")
        print("Seuraa kulutsta -- K")
        print("-------------------------------------------")

        valinta = str(input().upper())

        if valinta == "S":
            saaja = input("Syota maksun saajan nimi")
            summa = float(input("Syota siirrettava summa"))
            pvm = date.today()

            if summa < 1000 and summa > 0:
                tilisiirto(saaja, summa, pvm)

            elif summa > 0 and summa >= 1000:
                cont = input("Siirrettävä summa yli 1000,\njos haluat jatkaa paina 'Y' ").upper()
                if cont == 'Y':
                    print('Suoritetaan siirto')
                    tilisiirto(saaja, summa, pvm)

            else:
                print('Toimintoa ei voitu suorittaa')

        elif valinta == "T":
            print("Tulostetaan tilitapahtumat:")
            tilitapahtumat()

        elif valinta == "K":
            seuraa_kulutusta()

        elif valinta == "H":
            lainan_maara = float(input('Syota haluttu lainan maara, min:1000eur - max:50 000eur'))
            maksu_aika = int(input('Syota haluttu maksuaika, min:2v - max:5v'))
            kk_tulot = input('Syota kuukausitulosi') #Hae csv-filusta

            if lainan_maara >= 1000 and lainan_maara <= 5000 and  maksu_aika >=2 and maksu_aika <=5:
                hae_lainaa(lainan_maara, maksu_aika, kk_tulot)

            else:
                print('Jotain meni vikaan :(')

        elif valinta == "Q":
            print("Suljetaan sovellus")
            sysExit()


user_interface()
