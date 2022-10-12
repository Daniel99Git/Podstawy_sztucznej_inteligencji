import math
import random

def DB_Scan(wejscia):
    minimum_sasiadow = 3
    min_odleglosc = 0.3
    grupa = 0
    C = 0

    dane = []
    try:
        file = open("dane_plus.txt")            #Czytanie danych z pliku
        for line in file.readlines():
            line = line.strip()
            line = line.strip("[")
            line = line.strip("]")
            line = line.split(",")
            line[0] = float(line[0])
            line[1] = float(line[1])
            line[2] = float(line[2])
            line[3] = float(line[3])
            dane.append(line)
        file.close()

        file2 = open("dane_minus.txt")
        for line in file2.readlines():
            line = line.strip()
            line = line.strip("[")
            line = line.strip("]")
            line = line.split(",")
            line[0] = float(line[0])
            line[1] = float(line[1])
            line[2] = float(line[2])
            line[3] = float(line[3])
            dane.append(line)
        file2.close()
    except FileNotFoundError:
        print(("brak danych"))
    dane.append(wejscia)

    przynaleznosc = []
    for i in range(0,len(dane)):
        przynaleznosc.append(False)


    for i in range(len(dane)):         # Dzialanie DB Scan
        licznik = 0
        label = []
        istnieje_podobna = False
        grupa_podobnej = []
        if przynaleznosc[i] == False:
            for j in range(0, len(dane)):
                odleglosc = 0
                for k in range(len(dane[i])):
                    odleglosc += abs(dane[i][k] - dane[j][k])
                if odleglosc <= min_odleglosc:
                    if przynaleznosc[j] != False:
                        istnieje_podobna = True
                        grupa_podobnej = przynaleznosc[j]
                    licznik += 1
                    label.append(j)
            if licznik >= minimum_sasiadow:
                if istnieje_podobna == False:
                    C += 1
                    for x in range(len(label)):                # Zaznaczenie grupy, do której należy punkt
                        przynaleznosc[label[x]] = C
                else:
                    for x in range(len(label)):
                        przynaleznosc[label[x]] = grupa_podobnej
        else:
            continue
    print(przynaleznosc)
    return przynaleznosc[-1]

x = DB_Scan([0,0,-1,0])
print(x)