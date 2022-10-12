import random
import matplotlib.pyplot as plt
             ############ Uczenie k-srednich, ktora podzieli dane wejsciowe na 2 grupy
dane_uczace = []
for i in range(500):        # stworzenie randomowych stanow wozka
    dane_uczace.append([random.uniform(-24,24),random.uniform(-25,25),random.uniform(-12,12),random.uniform(-18,18)])

def k_srednich(dane_uczace):
    l_punktow = len(dane_uczace)
    wartosci = 4
    l_centrow = 3
    centra = []

    for i in range(0, l_centrow):
        centra.append(dane_uczace[random.randint(0,500)])
    print("punkty centrow = " +str(centra))

    grupy_centroidow = 0
    warunek_zakonczenia = False
    while warunek_zakonczenia == False:
        stare_centra = centra[:]
        odleglosc = []
        for i in range(0, l_punktow):
            x = []
            for j in range(0, l_centrow):
                suma = 0
                for y in range(0, wartosci):
                    suma = suma + (abs(dane_uczace[i][y] - centra[j][y]))  # odległość euklidesowa punktu od centoidu)
                x.append(suma)
            odleglosc.append(x)
        # print(" odleglosci = " + str(odleglosc))

        grupy_centroidow = []
        for i in range(0, l_centrow):
            grupy_centroidow.append([])

        for i in range(0, l_punktow):
            najmniejsza_wartosc = odleglosc[i][0]
            indeks = 0
            for j in range(1, l_centrow):
                if najmniejsza_wartosc > odleglosc[i][j]:
                    najmniejsza_wartosc = odleglosc[i][j]
                    indeks = j
            grupy_centroidow[indeks].append(i)

        # print("grupowanie punktów do centrum " + str(grupy_centrow))

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
                    nowy_centroid.append(centra[i][j])

            centra[i] = nowy_centroid

        warunek_zakonczenia = True
        for i in range(len(centra)):
            roznica = 0
            for j in range(wartosci):
                roznica = roznica + (centra[i][j] - stare_centra[i][j])
            if roznica != 0:
                warunek_zakonczenia = False

    for i in range(len(dane_uczace)):
        plt.plot(dane_uczace[i][0], dane_uczace[i][1], 'b.')
    for i in range(len(centra)):
        plt.plot(centra[i][0], centra[i][1], 'r*')
    plt.show()
    print(grupy_centroidow)
        #print("nowe centra " + str(centra))
    return centra
k = k_srednich(dane_uczace)
print(k)