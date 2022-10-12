import copy
import random
import numpy as np
import matplotlib.pyplot as plt


dane_uczace = []
wyniki = []
pomocnicza = []

### POBIERANIE DANYCH Z PLIKU

file = open("slump_test.data")
for linia in file.readlines():
    linia = linia.strip()
    linia = linia.split(",")
    for i in range(0, len(linia)):
        linia[i] = float(linia[i])
    pomocnicza.append(linia)
file.close()

### PODZIAŁ DANYCH NA WEJŚCIA I WYJŚCIA

for i in range(0, 90):
    x = []
    y = []
    for j in range(1, 8):
        x.append(pomocnicza[i][j])
    dane_uczace.append(x)
    for z in range(8, 11):
        y.append(pomocnicza[i][z])
    wyniki.append(y)


np.array(dane_uczace)
np.array(wyniki)



################ K-SREDNICH

def k_srednich(dane_uczace):
    l_punktow = len(dane_uczace)
    wartosci = 7
    l_centroid = 2
    #centroidy = [[251.99180327868854, 84.35409836065574, 122.37704918032787, 202.19180327868852, 8.788524590163934, 831.927868852459, 771.2196721311476], [180.76551724137934, 58.706896551724135, 165.09310344827585, 189.51034482758624, 8.389655172413793, 987.7103448275863, 706.051724137931]]
    centroidy = []

    for i in range(0, l_centroid):
        centroidy.append(dane_uczace[random.randint(0, 89)])
    print("punkty centrów = " +str(centroidy))

    grupy_centroidow = 0
    warunek = False
    while warunek == False:
        stare_centroidy = centroidy[:]
        odleglosc = []
        for i in range(0, l_punktow):
            x = []
            for j in range(0, l_centroid):
                suma = 0
                for y in range(0, wartosci):
                    suma = suma + (abs(dane_uczace[i][y] - centroidy[j][y]))  # odległość euklidesowa punktu od centoidu)
                x.append(suma)
            odleglosc.append(x)
        # print(" odleglosci = " + str(odleglosc))

        grupy_centroidow = []
        for i in range(0, 2):
            grupy_centroidow.append([])

        for i in range(0, l_punktow):
            najmniejsza_wartosc = odleglosc[i][0]
            indeks = 0
            for j in range(1, l_centroid):
                if najmniejsza_wartosc > odleglosc[i][j]:
                    najmniejsza_wartosc = odleglosc[i][j]
                    indeks = j
            grupy_centroidow[indeks].append(i)

        # print("grupowanie punktów do centrum " + str(grupy_centroidow))

        ###nowa wspolrzedna centroida
        for i in range(len(grupy_centroidow)):
            nowy_centroid = []
            for j in range(wartosci):
                suma = 0
                for k in range(len(grupy_centroidow[i])):
                    suma = suma + dane_uczace[grupy_centroidow[i][k]][j]
                if len(grupy_centroidow[i]) != 0:
                    srednia = suma/len(grupy_centroidow[i])
                    nowy_centroid.append(srednia)
                else:
                    nowy_centroid.append(centroidy[i][j])

            centroidy[i] = nowy_centroid

        warunek = True
        for i in range(len(centroidy)):
            roznica = 0
            for j in range(wartosci):
                roznica = roznica + (centroidy[i][j] - stare_centroidy[i][j])
            if roznica != 0:
                warunek = False

    for i in range(len(dane_uczace)):
        plt.plot(dane_uczace[i][0], dane_uczace[i][1], 'b.')
    for i in range(len(centroidy)):
        plt.plot(centroidy[i][0], centroidy[i][1], 'r*')
    plt.show()
    print(grupy_centroidow)
        #print("nowe centroidy " + str(centroidy))
    return centroidy
k = k_srednich(dane_uczace)
print(k)


