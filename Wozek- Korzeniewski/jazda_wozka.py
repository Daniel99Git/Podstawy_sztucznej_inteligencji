import copy
import math
import random
import numpy as np
import Symulator_wozka

def ustawienie_c_i_gamma():
    c = []
    gamma = []
    for j in range(liczba_regol):
        pom_c = []
        pom_gamma = []
        for i in range(4):
            pom_c.append(random.uniform(0,1))
            pom_gamma.append(random.uniform(-1,1))
        c.append(pom_c)
        gamma.append(pom_gamma)
    return c,gamma

def neuron_rozmyty(x,c,gamma):
    wynik = ((x-c)/gamma) ** 2
    return math.exp(-wynik)

def siec_podstawowa(wejscia, c, gamma, wagi):      # liczenie sieci z prezentacji
    suma = 0
    suma_z_waga = 0
    iloczyn = 1
    for i in range(0, len(wejscia)):            # pierwsze iloczyn ( mnozony razy wagi)
        wynik = neuron_rozmyty(wejscia[i],c[0][i],gamma[0][i])
        iloczyn *= wynik
    suma_z_waga += iloczyn * wagi[0]
    suma += iloczyn
    iloczyn = 1
    for i in range(0, len(wejscia)):            # pierwsze iloczyn ( mnozony razy wagi)
        wynik = neuron_rozmyty(wejscia[i],c[1][i],gamma[1][i])
        iloczyn *= wynik
    suma_z_waga += iloczyn * wagi[1]
    suma += iloczyn
    if suma ==0:
        suma += 0.00001
    return suma_z_waga / suma

def siec(wejscia, c, gamma, wagi):      # liczenie sieci z 10-cioma regulami
    suma = 0
    suma_z_waga = 0
    for j in range(liczba_regol):
        iloczyn = 1
        for i in range(0, len(wejscia)):            # pierwsze iloczyn ( mnozony razy wagi)
            wynik = neuron_rozmyty(wejscia[i],c[0][i],gamma[0][i])
            iloczyn *= wynik
        suma_z_waga += iloczyn * wagi[0]
        suma += iloczyn

    if suma ==0:
        suma += 0.00001
    return suma_z_waga / suma


def licz_czas(O,O_max,x,max_x,czas,X_predkosc,O_predkosc,nowe_wagi,c,gamma):  # liczenie błędu sieci
    przyspieszenie_wozka = 0
    przyspieszenie_wachadla = 0
    while O <= O_max and O >= -O_max and czas <= 1000 and x >= -max_x and x <= max_x:           # 1000 ==> Czas trwania ustalony, by wózek nie jeżdził w nieskończoność
        # Użycie sieci
        wejscia = [x, X_predkosc, O, O_predkosc]
        F = siec(wejscia,c,gamma, nowe_wagi) * 10
        if F > 10:
            F = 10
        if F < -10:
            F = -10
        Fi = Symulator_wozka.licz_Fi(m_wahadla, l, O, O_predkosc, Up,g)
        mi = Symulator_wozka.licz_mi(m_wahadla, O)
        przyspieszenie_wozka = Symulator_wozka.licz_przyspieszenie_X(F, Uc, X_predkosc, M_wozka, Fi, mi)
        przyspieszenie_wachadla = Symulator_wozka.licz_przyspieszenie_O(l, przyspieszenie_wozka, O, Up, O_predkosc, m_wahadla,g)

        # Zmiana parametrów pod wpływem czasu
        x = x + t * X_predkosc
        X_predkosc = X_predkosc + t * przyspieszenie_wozka
        O = O - t * O_predkosc
        O_predkosc = O_predkosc + t * przyspieszenie_wachadla

        czas = czas + 0.02
        print("Obecny kąt: " + str(O) + " Położenie wózka " + str(x) + ' wózek: ' + str(przyspieszenie_wozka) + ' wahadło: '
          + str(przyspieszenie_wachadla) + " X*: " + str(X_predkosc) + " wahadlo*: " + str(O_predkosc) + " Czas: " + str(czas) + "Siła: " + str(F))
    return czas



    ################################################### SYMULATOR WÓZKA ########################################################

        #    math.sin(math.radians(90))  --> Liczenie sinus 90 stopni

def losowanie_z_krokiem(warstwa, krok):  # losowanie nowych wartości przy uwzględnieniu kroku w symulowanym wyszarzaniu
    for i in range(0, len(warstwa)):
        for j in range(0, len(warstwa[i])):
            x = warstwa[i][j] - krok
            y = warstwa[i][j] + krok
            if x < 0: x = -1
            if y > 1: y = 1

            warstwa[i][j] = random.uniform(x, y)
    return warstwa

def losowanie_c(warstwa, krok):  # losowanie nowych wartości przy uwzględnieniu kroku w symulowanym wyszarzaniu
    for i in range(0, len(warstwa)):
        for j in range(0, len(warstwa[i])):
            x = warstwa[i][j] - krok
            y = warstwa[i][j] + krok
            if x < -1: x = 0
            if y > 1: y = 1

            warstwa[i][j] = random.uniform(x, y)
    return warstwa


            ########### dzialanie programu ##############################################################

if __name__ == "__main__":
    liczba_regol = 10


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
    czas_trwania = 500   # sekundy - czas trwania całego doświadczenia

    N = 1           # ilość wahadeł

    X_przyspieszenie = 0  # m/(s do kwadratu) - Przyspieszenie wózka     ( X z 2-ma kropkami)
    O_przyspieszenie = 0  # m/(s do kwadratu) - Przyspieszenie wahadła  ( O z 2-ma kropkami)
    O_2_przyspieszenie = 0  # -||- drugiego wahadła
    X_predkosc = 0   # prędkość wózka                                    ( X z jedną kropką)
    O_predkosc = 0   # prędkość wahadła                                 ( O z jedną kropką)
    O_drugie_predkosc = 0   # prędkość drugiego wahadła

    ################################################### Dzialanie ######################################################

    s_najlepsze = [-0.3721746648993727, -0.612701326340167, -0.4935373998989021]
    gamma_najlepsze = [[-0.9062240449202739, -0.6211299074606982, -0.7624337938729584, -0.658920204164519],
                       [-0.8806827245420082, -0.47924762765327655, -0.8699084270807342, -0.8956998742727079],
                       [-0.9875220915362336, -0.8419122096663553, -0.960781665001564, -0.8661907025937501]]
    c = [[-0.5841119419283208, 14.718162183601896, -0.6332001189572465, 0.0010210720229036074],
         [11.751517734528404, -9.656983922056176, -0.3899035368819443, 0.37109627309479193],
         [-13.385895757422064, -9.471301094385515, 1.2638847545001344, -0.13287821242286083]]

    czas = licz_czas(O,O_max,x,max_x,czas,X_predkosc,O_predkosc,s_najlepsze,c,gamma_najlepsze)

