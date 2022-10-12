import math
import numpy as np

# Funckja do liczenia dystansu
def dystans(x, y):  # Licznik ze wzoru to odleglosc euklidesowa
    roznica = 0
    for i in range(wymiary):
        roznica += abs(x[i] - y[i])
    return roznica

#PNN
# Sieć PNN ze wzoru z prezentacji
def pnn(x_ciag, xs,gamma, p=2):  # Implementacja całego wzoru z prezentacji, kolejnosc dzialania jak w prezentacji
    suma = 0
    for x in range(len(x_ciag)):
        wynik = dystans(x_ciag, xs[x])
        wynik = wynik / p * gamma
        wynik = -1 * wynik ** 2
        wynik = math.exp(wynik)
        suma += wynik
    return ((suma / len(x_ciag)) * 5) + 3 #Jest razy 5 poniewaz przedzialy ocen w danych jest od najmniejszej 3 do
                                            # największej 8
#Funkcja pnn oblicza wartośc dla podanego zbioru

#Część kodu odpowiedzlana za podzielenie danych na uczace i wyniki ostatani liczba w danych to ocena
dane = []
dane_wejsciowe = []
oceny = []
file = open("JakoscWina-Czerwone.txt")  # Czytanie danych z pliku
for line in file.readlines():           # pętla czytająca każdą linię z pliku
    line = line.strip()
    line = line.split(";")
    for i in range(0, len(line)):
        line[i] = float(line[i])
    dane.append(line)                   # Wszykie dane
    file.close()

for i in range(0, len(dane)-3):  # Podział danych na uczące i wyniki
    pomocnicza_lista = []
    for j in range(0, 11):
        pomocnicza_lista.append(dane[i][j])
    dane_wejsciowe.append(pomocnicza_lista)         # Dane wejsciowe ( 11 wymiarów)
    oceny.append(int(float(dane[i][-1])))  # [-1] oznacza ostani element w liście ,  czyli prawidłowe wyniki dla każdej danej

# print(dane_wejsciowe)
# print(wyniki)

# K-srednich
#Tabele pomocnicze
tablicaKlastrow = []
centra = 5 # 5 centorw liczba wybrana losowo
tablicaCentra = []
wymiary = 11 # 11 danych uczących

#Utworzenie losowych centrów
    # Centra początkowo są ustawione jako losowe punkty ze wszystkich danych wejsciowych
for i in range(centra):
    rob = np.random.randint(0, len(dane_wejsciowe))
    tablicaCentra.append(dane_wejsciowe[rob])
# print(tablicaCentra)

iloscIteracji = 0 #ile razy ma zostac wykonany algorytm Kmeans
while iloscIteracji < 100:
    tablicaKlastrow = []
    oceny_grup = []
    wyniki = []
    for l in range(centra):                     #
        tablicaKlastrow.append([])              # Zaimplementowanie pustych " miejsc" na klastry, wyniki i oceny
        wyniki.append([])                       #
        oceny_grup.append([])                   #
    for i in range(len(dane_wejsciowe)):
        dystansKM = 0
        for j in range(wymiary):
            dystansKM = dystansKM + abs(tablicaCentra[0][j] - dane_wejsciowe[i][j])
        klaster = 0
        for k in range(centra):
            nowyDystansKM = 0
            for j in range(wymiary):
                nowyDystansKM = nowyDystansKM + abs(tablicaCentra[k][j] - dane_wejsciowe[i][j])
            if nowyDystansKM <= dystansKM:
                klaster = k
                dystansKM = nowyDystansKM
        tablicaKlastrow[klaster].append(dane_wejsciowe[i])
        wyniki[klaster].append(i)
        oceny_grup[klaster]. append(i)
    # for i in range(centra):
        # print(tablicaKlastrow[i])
        # print(wyniki[i])

    staraTablicaCentra = tablicaCentra[:]
    for i in range(centra):
        tablicaPomocnicza = []
        for j in range(wymiary):
            w = 0
            for k in range(len(tablicaKlastrow[i])):
                w = w + tablicaKlastrow[i][k][j]
            tablicaPomocnicza.append(w/len(tablicaKlastrow[i]))
            tablicaCentra[i] = tablicaPomocnicza[:]
            # print(str(i), tablicaCentra[i])
    iloscIteracji = iloscIteracji + 1

                #Dane które były danymi uczacymi
szukana = np.array([8.8, 0.61, 0.3, 2.8, 0.088, 17, 46, 0.9976, 3.26, 0.51, 9.3]) # wynik ma byc 4
# szukana = np.array([8.4,0.715,0.2,2.4,0.076,10,38,0.99735,3.31,0.64,9.4]) # wynik ma być 5
# szukana = np.array([7.9, 0.545, 0.06, 4, 0.087, 27, 61, 0.9965, 3.36, 0.67, 10.7]) # wynik ma być 6

                #Szukane które nie były danymi uczącymi  - Dane testowe
# szukana = np.array([6.8,0.67,0.15,1.8,0.118,13,20,0.9954,3.42,0.67,11.3])    # ma wyjsc 6
# szukana = np.array([9,0.47,0.31,2.7,0.084,24,125,0.9984,3.31,0.61,9.4])    # ma wyjsc 6

odlegosc = 0
for i in range(11):                                     #
    odlegosc += abs(tablicaCentra[0][i] - szukana[i])   # Liczenie odleglosci naszej danej do pierwszego centra
przenaleznosc = 0                                       #
for j in range(1,len(tablicaCentra)):
    odleglosc = 0                                                  #
    for i in range(11):                                            # Liczenie odległości do kolejnych centrów
        odleglosc += abs(tablicaCentra[j][i] - szukana[i])         #

    if odleglosc < odlegosc:
        przenaleznosc = j                        #punkt należy do klastra, do centum którego jest najmniejsza odległość
print(przenaleznosc+1)      # Printujemy " + 1" by było czytelniejsze, która to grupa


# klastry = []
# for i in range(centra):
#     pom = []
#     for j in range(len(wyniki[i])):
#         pom.append(dane_wejsciowe[wyniki[i][j]])
#     klastry.append(pom)

wynik = pnn(szukana, tablicaKlastrow[przenaleznosc], 0.5, p=11)         # Wywołanie sieci używającej danych z grupy,
                                                                        #  do której przynależy szukany punkt
print(wynik)

# for i in range(len(dane_wejsciowe)):
#     x = pnn(dane_wejsciowe[i],dane_wejsciowe,0.3, p=11)               # Wywołanie całej sieci ( bez podziałów na klastry)
#     print(x)
