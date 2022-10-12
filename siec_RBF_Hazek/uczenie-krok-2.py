import copy
import random
import numpy as np

#def neuron(x):
    #wynik = 1
    #return wynik

def neuron(uczace, centra):
        odl = odleglosc(uczace, centra)
        wynik = np.exp(-odl *2 / 16 * 2)
        return wynik
def odleglosc(x1, x2):
    odl = 0
    for i in range(len(x1)):
        odl += (x1[i] - x2[i])**2
    odl =np.sqrt(odl)
    return odl

def warstwa_ukryta(dana_uczaca, wagi, centra):
    wyniki = []
    for i in range(0,len(wagi)):
        pom = neuron(dana_uczaca, centra[i])
        pom = pom * wagi[i]
        wyniki.append(pom)
    suma = 0
    for i in range(0, len(wagi)):
        suma = wyniki[i] + suma
    return suma

def blad(sumy,wyniki):
    blad = 0
    for i in range(0, len(wyniki)):
        blad = blad + abs(sumy[i]-wyniki[i])
    return blad

def funkcja (dane_uczace,wagi,wyniki,centra):                      #liczenie bledu
    sumy = []
    for i in range(len(wyniki)):
        sumy.append(warstwa_ukryta(dane_uczace[i],wagi,centra))
    wynik_funkcji = blad(sumy,wyniki)
    return wynik_funkcji



def uczenie_symulowane_wyrzarzanie(centra, dane_uczace, wyniki):
            #######################       #Uczenie wyrzarzadnie  #####################################33

    temperatura = 1000

    e = 2.7182818
    wagi = [random.random(),random.random(),random.random(),random.random()]
    best = copy.deepcopy(wagi)


    while temperatura > 0:  #petla sie wykonuje dopoki warunek sie zgadza
        krok = [random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1)]
        wagi_p = []
        for i in range(0,len(wagi)):
            ppp = wagi[i]+krok[i]
            if ppp > 1:
                ppp = 1
            if ppp <-1:
                ppp = -1
            wagi_p.append(ppp)

        roznica = funkcja(dane_uczace,wagi_p,wyniki,centra) - funkcja(dane_uczace,wagi,wyniki,centra)
        if roznica < 0:
            wagi = wagi_p
            if funkcja(dane_uczace,wagi_p,wyniki,centra) < funkcja(dane_uczace,best,wyniki,centra):
                best = copy.deepcopy(wagi_p)        #najlepszy wynik zapisany do zmiennej
        else:
            x = random.uniform(0, 1)
            if x < e ** (-roznica/temperatura):
                wagi = wagi_p
        temperatura = temperatura-1
    print("najlepsze wagi : " + str(best))
    print(str(funkcja(dane_uczace,best,wyniki,centra)))
    return best



dane_uczace = []
wyniki = []
pomocnicza = []

### POBIERANIE DANYCH Z PLIKU

file = open("dane.txt")
for linia in file.readlines():
    linia = linia.strip()
    linia = linia.split(",")
    for i in range(0, len(linia)):
        linia[i] = float(linia[i])
    pomocnicza.append(linia)
file.close()


### PODZIAŁ DANYCH NA WEJŚCIA I WYJŚCIA

for i in range(0, 12):
    x = []
    y = []
    for j in range(0, 2):
        x.append(pomocnicza[i][j])
    dane_uczace.append(x)
    wyniki.append(pomocnicza[i][2])

np.array(dane_uczace)
np.array(wyniki)


centra = []
for i in range(4):
    centra.append([random.uniform(0, 10), random.uniform(-5, 5)])
best_centra = copy.deepcopy(centra)


################################################################
grupy = [[[1.0, -5.0]],

         [[2.0, 5.0], [1.0, 2.0]],

         [[3.0, -2.0], [2.0, 0.0], [6.0, -5.0],[7.0, 5.0], [6.0, -2.0], [7.0, 2.0], [6.0, 0.0],[8.0, -5.0], [9.0, 5.0],
                                    [10.0, -2.0], [8.0, 2.0],[9.0, 0.0]]]  # poklastrowane dane przez DB_scam

wyniki_grup = [[0.3],
               [0.3, 0.5],
               [0.5, 0.7, 0.5, 0.5, 0.3, 0.3, 0.7, 0.5, 0.5, 0.3, 0.3, 0.5]]

wagi = []                       #przechowywanie listy z wagami dla danej grupy
for i in range(len(grupy)):
    waga = uczenie_symulowane_wyrzarzanie(centra, grupy[i],wyniki_grup[i])
    wagi.append(waga)
# print(wagi)


centroidy = []                  #ustalanie centroidow dla grup w celu grupowania nowych danych
for i in range(len(grupy)):
    centroid = []
    for j in range(2):
        suma = 0
        for k in range(len(grupy[i])):
            suma += grupy[i][k][j]
        suma = suma / len(grupy[i])
        centroid.append(suma)
    centroidy.append(centroid)
# print(centroidy)

punkt = [8,2]
odl = odleglosc(punkt,centroidy[0])
przynaleznosc = 0
for i in range(1, len(centroidy)):
    odl2 = odleglosc(punkt,centroidy[i])
    if odl2 < odl:
        przynaleznosc = i

wynik = warstwa_ukryta(punkt,wagi[przynaleznosc],centra)

print("wynik")
print(wynik)









