import copy
import random
import numpy as np
import math

dane_uczace = []
indeksy_danych_1_sieci = [0, 1, 2, 3, 5, 7, 8, 9, 10, 11, 12, 17, 18, 19, 21, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 55, 56, 57, 60, 61, 62, 63, 64, 67, 68, 69, 70, 71, 72, 73, 74, 75, 77, 82, 87]
indeksy_danych_2_sieci = [4, 6, 13, 14, 15, 16, 20, 22, 23, 37, 38, 39, 53, 54, 58, 59, 65, 66, 76, 78, 79, 80, 81, 83, 84, 85, 86, 88, 89]
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

### ZMIANA INDEKSU NA WARTOŚĆ

###GRUPA 1
# grupa_1 = [[0],[0]]
# for i in range(0, 2):
#     grupa_1[i] = dane_uczace[indeksy_danych_1_sieci[i]]
# for i in range(2, len(indeksy_danych_1_sieci)):
#     grupa_1.append(dane_uczace[indeksy_danych_1_sieci[i]])
#
# wyniki_1 = [[0],[0]]
#
# for i in range(0, 2):
#     wyniki_1[i] = wyniki[indeksy_danych_1_sieci[i]]
# for i in range(2, len(indeksy_danych_1_sieci)):
#     wyniki_1.append(wyniki[indeksy_danych_1_sieci[i]])


### GRUPA 2
grupa_2 = [[0],[0]]
for i in range(0, 2):
    grupa_2[i] = dane_uczace[indeksy_danych_2_sieci[i]]
for i in range(2, len(indeksy_danych_2_sieci)):
    grupa_2.append(dane_uczace[indeksy_danych_2_sieci[i]])

wyniki_2 = [[0],[0]]

for i in range(0, 2):
    wyniki_2[i] = wyniki[indeksy_danych_2_sieci[i]]
for i in range(2, len(indeksy_danych_2_sieci)):
    wyniki_2.append(wyniki[indeksy_danych_2_sieci[i]])

################################ PERCEPTRON

### WARSTWY
w1 = np.random.random([7, 4])
w2 = np.random.random([4, 3])
w3 = np.random.random([3, 2])
w4 = np.random.random([2, 3])
wagi = w1, w2, w3, w4


### NEURON SIGMOIDALNY
def neuron(x):
    wynik = 1/ (1 + (math.exp(-x)))
    return wynik

def licz_warstwe(dane_uczace,wagi,numer_warstwy):
    neurony = []
    for i in range(0, len(wagi[numer_warstwy][0])):
        suma = 0
        for j in range(0, len(wagi[numer_warstwy])):
            suma += dane_uczace[j] * wagi[numer_warstwy][j][i]
        suma = suma/len(wagi[numer_warstwy])
        neurony.append(neuron(suma) * 100)
    return neurony

def siec(wagi, dane_uczace):  # Działanie sieci
    pierwsze_neurony = licz_warstwe(dane_uczace,wagi,0)
    drugie_neurony = licz_warstwe(pierwsze_neurony,wagi,1)
    trzecie = licz_warstwe(drugie_neurony,wagi,2)
    czwarta = licz_warstwe(trzecie,wagi,3)
    return np.array(czwarta)


### JEDEN SUMARYCZNY BŁĄD

def liczenie_bledu(wagi, dane_uczace, wyniki):
    roznica = 0
    for i in range(0, len(dane_uczace)):
        x = siec(wagi, dane_uczace[i])
        roznica += abs(wyniki[i] - x)
    suma = roznica[0] + roznica[1] + roznica[2]
    return suma



################################ SYMULOWANE WYŻARZANIE

def losowanie_nowych_wag(wagi, krok):
    for i in range(0, len(wagi)):
        for j in range(0, len(wagi[i])):
            for z in range(0, len(wagi[i][j])):
                odejmowanie = wagi[i][j][z] - krok
                dodawanie = wagi[i][j][z] + krok
                if odejmowanie < -1:
                    odejmowanie = -1
                if dodawanie > 1:
                    dodawanie = 1
                wagi[i][j][z] = random.uniform(odejmowanie, dodawanie)
    return wagi

def uczenie_sym_wyz(dane_uczace, wagi, wyniki):
    krok = 0.15
    t = 500            # Temperatura początkowa
    e = 2.7182818284
    s_najlepsze = [[[ 0.05074009,  0.83219618,  0.60828107, -0.97041873],
       [ 0.59134228,  0.52686539, -0.66677692, -0.90525955],
       [ 0.56246156, -0.87935867, -0.27584406,  0.23584057],
       [ 0.49799057, -0.25493165, -0.44741044, -0.05006975],
       [-0.229593  , -0.75135937,  0.54469815, -0.47014396],
       [-0.36292478,  0.21316507,  0.41823127, -0.40689291],
       [-0.19649515,  0.20141992,  0.04888245, -0.75196476]],

                   [[-0.33876152, 0.78188531, 0.09325856],
                    [0.34889439, 0.25215251, 0.2759953],
                    [-0.39140942, -0.94582877, 0.72611437],
                    [0.44441256, 0.90702015, -0.33371427]],

                   [[0.17208397, -0.37474193],
                    [-0.36729274, -0.18136256],
                    [-0.70649718, 0.0129038]],

                   [[-0.84545079, -0.47108025, -0.27752269],
                    [-0.60873828, -0.02172267, -0.27712745]]]

    while t > 0:
        for i in range(0,3):
            wagi2 = losowanie_nowych_wag(wagi, krok)
            xx = liczenie_bledu(wagi2, dane_uczace, wyniki)
            yy = liczenie_bledu(wagi, dane_uczace, wyniki)
            roznica = xx - yy
            if xx < liczenie_bledu(s_najlepsze, dane_uczace, wyniki):
                s_najlepsze = copy.deepcopy(wagi2)
                #print(s_najlepsze)
                #print(liczenie_bledu(s_najlepsze, dane_uczace, wyniki))
            if roznica < 0:
                wagi = copy.deepcopy(wagi2)
            else:
                x = random.randrange(0,1)
                if x < e **(-roznica/t):
                    wagi = copy.deepcopy(wagi2)
            # print(s)
        t = t - 1
        #print("wartosc po przejsciu: " + str(wagi))
    print("najlepszy punk s : " + str(s_najlepsze) + " błąd wynosi: " + str(liczenie_bledu(s_najlepsze, dane_uczace, wyniki)))
    return  s_najlepsze

x = uczenie_sym_wyz(grupa_2, wagi, wyniki_2)
print(x)





