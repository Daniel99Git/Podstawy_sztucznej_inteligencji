import math
import copy
import random
import numpy as np

def licz_Fi(m,li,Oi,O_kropka,Upi):     #liczenie siły
    Ooi = Oi**2
    pierwsza_czesc = m * 0.5 * li * (Ooi) * (math.sin(math.radians(Oi)))
    druga_czesc = 0.75*m * math.cos(math.radians(Oi)) * ((Upi*O_kropka)/(m*0.5*li)) + g*math.sin(math.radians(Oi))
    return pierwsza_czesc + druga_czesc

def licz_mi(mi,Oi):                     # liczenie masy względem kąta
    cos = math.cos(math.radians(Oi))
    return mi * (1 - (0.75 * cos**2))

def licz_przyspieszenie_X(F,Uc,x_predkosc,M,Fi_fala,mi_fala):     # Na początku dla jednego wahadła
    gora = F - Uc + Fi_fala
    dol = M + mi_fala
    return gora / dol

def licz_przyspieszenie_O(li,przyspieszenie_X,Oi,Upi,O_predkosc,m):     # Przyspieszenie kątowe wahadła
    ulamek = (Upi*O_predkosc) / (m*li)
    return -0.75 * li * ( przyspieszenie_X*math.cos(math.radians(Oi)) + g*math.sin(math.radians(Oi)) + ulamek)



            #-------------------------- SIEC ------------------------#

            #---------- SIEC ---------#

def odleglosc(x1, x2):
    odl = 0
    for i in range(len(x1)):        # Dlugosc 4 ( boi 4-ro wymiorowa dana)
        odl += (x1[i] - x2[i])**2
    odl =np.sqrt(odl)
    return odl

def neuron(uczace, centra):     # gamma to szerokosc/zasięg neurona
        odl = odleglosc(uczace, centra)
        wynik = np.exp(-odl **2 / 25 * 2)
        return wynik


def RBF(dana_uczaca, wagi, centra):
    wyniki = []
    for i in range(0,len(wagi)):
        pom = neuron(dana_uczaca, centra[i])
        pom = pom * wagi[i]
        wyniki.append(pom)
    suma = 0
    for i in range(0, len(wyniki)):
        suma += wyniki[i]               # Sumujemy wyniki neuronów pomnozone przez wagi
    return suma

                         #-------------------UCZENIE----------------------#


def licz_czas(O,O_max,x,max_x,czas,X_predkosc,O_predkosc,wagi, centra):  # liczenie błędu sieci

    while O <= O_max and O >= -O_max and czas <= 1000 and x >= -max_x and x <= max_x:           # 1000 ==> Czas trwania ustalony, by wózek nie jeżdził w nieskończoność
        # Użycie sieci
        wejscia = [x, X_predkosc, O, O_predkosc]
        F = RBF(wejscia, wagi, centra)
        if F > 10:
            F = 10
        if F < -10:
            F = -10

        Fi = licz_Fi(m_wahadla, l, O, O_predkosc, Up)
        mi = licz_mi(m_wahadla, O)
        przyspieszenie_wozka = licz_przyspieszenie_X(F, Uc, X_predkosc, M_wozka, Fi, mi)
        przyspieszenie_wachadla = licz_przyspieszenie_O(l, przyspieszenie_wozka, O, Up, O_predkosc, m_wahadla)


        # Zmiana parametrów pod wpływem czasu
        x += t * X_predkosc
        X_predkosc +=  t * przyspieszenie_wozka
        O += t * O_predkosc
        O_predkosc += t * przyspieszenie_wachadla

        czas = czas + t
    print("Obecny kąt: " + str(O) + " Położenie wózka " + str(x) + ' wózek: ' + str(
        przyspieszenie_wozka) + ' wahadło: ' + str(przyspieszenie_wachadla) + " X*: " + str(
        X_predkosc) + " wahadlo*: " + str(O_predkosc) + " Czas: " + str(czas) + "Siła: " + str(F))

    return czas

def losowanie_z_krokiem(krok, lista):
    pom = []
    for i in range(len(lista)):
        x = lista[i] - krok
        y = lista[i] + krok
        pom.append(random.uniform(x,y))
    return pom

def symulowane_wyzarzanie(O,O_max,x,max_x,czas,X_predkosc,O_predkosc,wagi,centra):
    krok = 2
    temperatura = 300            # Temperatura początkowa
    e = 2.7182818284  #wartość e stała
    wagi_najlepsze = copy.deepcopy(wagi)

    centra_najlepsze = copy.deepcopy(centra)

    czas_najlepszy = licz_czas(O,O_max,x,max_x,czas,X_predkosc,O_predkosc,wagi_najlepsze,centra_najlepsze)
    print(czas_najlepszy)
    print("")

    while temperatura > 0:
        for z in range(0,3): # w każdej iteracji program wykonuje 3 probki poszukiwania najlepszej wartosci

            # wagi2 = losowanie_z_krokiem(krok, wagi)               # losowanie wag i centow z krokiem
            # centra2 = []
            # for i in range(4):
            #     centra2.append(losowanie_z_krokiem(krok,centra[i]))

            wagi2 = [random.uniform(-24, 24), random.uniform(-20, 20), random.uniform(-12, 12), random.uniform(-20, 20)]        # losowanie nowych wag i centrow
            centra2 = []
            for i in range(4):
                centra2.append([random.uniform(-24, 24), random.uniform(-20, 20), random.uniform(-12, 12),
                               random.uniform(-20, 20)])

            nowy_czas = licz_czas(O,O_max,x,max_x,czas,X_predkosc,O_predkosc,wagi2,centra2)
            stary_czas = licz_czas(O,O_max,x,max_x,czas,X_predkosc,O_predkosc,wagi,centra)
            roznica = nowy_czas - stary_czas
            if nowy_czas > czas_najlepszy:
                wagi_najlepsze = copy.deepcopy(wagi2)

                centra_najlepsze = copy.deepcopy(centra2)

                czas_najlepszy = nowy_czas
                print("Wagi najlepsze: " + str(wagi_najlepsze) + " Najlepsze centra: " + str(centra))
                print(czas_najlepszy)
                print("#  #############  #")
            if roznica > 0:
                wagi = copy.deepcopy(wagi2)
                centra = copy.deepcopy(centra2)
            else:
                rand = random.randrange(0,1)
                if rand < e **(-roznica/temperatura):
                    wagi = copy.deepcopy(wagi2)
                    centra = copy.deepcopy(centra2)
            # print(wagi)
        temperatura = temperatura - 1
        if czas_najlepszy >= 1000:
            break
    #     print("wartosc po przejsciu: " + str(wagi))
    print("najlepsze wagi, centra: " + str(wagi_najlepsze) + str(centra_najlepsze) + " dają czas: " + str(czas_najlepszy))
    return wagi_najlepsze

g = 9.8           # Przyspieszenie ziemskie w m/(s do kwadratu)
l = 0.5  # metry - długość wahadła
drugi_l = 0.05   # metry - długość drugiego wahadła
m_wahadla = 0.1  # kilogramy - masa wahadła
m_drugiego_wahadla = 0.01  # kilogramy - masa wahadła
O_max = 12   # stopnie - maksymalne wychylenie wahadła na plus lub minus
O_max_drugie = 36  # stopnie - wychylenie DRUGIEGO wahadła jeśli istnieje
O = 4 # stopnie obecnego wychylenia
O_drugie = 0  # stopnie obecnego wyhylenia 2 wahadła

x = 0
max_x = 24  # metry -  maksymalna pozycja wózka  ( -2.4 do 2.4 m)
M_wozka = 1    # kilogramy - masa wózka
F = 0    #od -10N do 10 Newtonów
Uc = 0.0005     # współczynnik tarcia wózka
Up = 0.000002   # Współczynnik tarcia wahadła na wózku ( dla obu wahadeł takie samo)
t = 0.02        # sekundy - wielkość kroku

czas = 0        # sekundy  - obecny upływ czasu
czas_trwania = 1000   # sekundy - czas trwania całego doświadczenia

N = 1           # ilość wahadeł

X_przyspieszenie = 0  # m/(s do kwadratu) - Przyspieszenie wózka     ( X z 2-ma kropkami)
O_przyspieszenie = 0  # m/(s do kwadratu) - Przyspieszenie wahadła  ( O z 2-ma kropkami)
O_2_przyspieszenie = 0  # -||- drugiego wahadła
X_predkosc = 0   # prędkość wózka                                    ( X z jedną kropką)
O_predkosc = 0   # prędkość wahadła                                 ( O z jedną kropką)
O_drugie_predkosc = 0   # prędkość drugiego wahadła


wagi = [random.uniform(-24, 24),random.uniform(-20, 20),random.uniform(-12, 12),random.uniform(-20, 20)]

centra = []
for i in range(4):
    centra.append([random.uniform(-24, 24),random.uniform(-20, 20),random.uniform(-12, 12),random.uniform(-20, 20)])


najlepsze = symulowane_wyzarzanie(O,O_max,x,max_x,czas,X_predkosc,O_predkosc,wagi,centra)


