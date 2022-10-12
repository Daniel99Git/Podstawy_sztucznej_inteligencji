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
    F = 0
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
            if x < 0: x = 0
            if y > 1: y = 1

            warstwa[i][j] = random.uniform(x, y)
    return warstwa

def losowanie_c(warstwa, krok):  # losowanie nowych wartości przy uwzględnieniu kroku w symulowanym wyszarzaniu
    for i in range(0, len(warstwa)):
        for j in range(0, len(warstwa[i])):
            x = warstwa[i][j] - krok
            y = warstwa[i][j] + krok
            if x < -1: x = -1
            if y > 1: y = 1

            warstwa[i][j] = random.uniform(x, y)
    return warstwa

def symulowane_wyzarzanie(O,O_max,x,max_x,czas,X_predkosc,O_predkosc,s,c,gamma):
    krok = 0.3  # wartość zmniejsza lub zwiększania zakresu poszukiwania
    temperatura = 200            # Temperatura początkowa
    e = 2.7182818284  #wartość e stała
    s_najlepsze = copy.deepcopy(s)
    gamma_najlepsze = copy.deepcopy(gamma)
    c_najlepsze = copy.deepcopy(c)
    czas_najlepszy = licz_czas(O,O_max,x,max_x,czas,X_predkosc,O_predkosc,s_najlepsze,c_najlepsze,gamma_najlepsze)
    print(czas_najlepszy)
    print("")

    while temperatura > 0:
        for z in range(0,3): # w każdej iteracji program wykonuje 3 probki poszukiwania najlepszej wartosci
            s2 = copy.deepcopy(s)
            for i in range(liczba_regol):
                s2[i] = random.uniform(-1, 1)
            gamma2 = copy.deepcopy(gamma)
            gamma2 = losowanie_z_krokiem(gamma2, krok)
            c2 = copy.deepcopy(c)
            c2 = losowanie_c(c2, krok)

            nowy_czas = licz_czas(O,O_max,x,max_x,czas,X_predkosc,O_predkosc,s2,c2,gamma2)
            stary_czas = licz_czas(O,O_max,x,max_x,czas,X_predkosc,O_predkosc,s,c,gamma)
            roznica = nowy_czas - stary_czas
            if nowy_czas > czas_najlepszy:
                s_najlepsze = copy.deepcopy(s2)
                gamma_najlepsze = copy.deepcopy(gamma2)
                c_najlepsze = copy.deepcopy(c2)
                czas_najlepszy = nowy_czas
                print("Wagi najlepsze: " + str(s_najlepsze) + " Najlepsze gamma: " + str(gamma_najlepsze))
                print(czas_najlepszy)
                print("########################")
            if roznica > 0:
                s = copy.deepcopy(s2)
                gamma = copy.deepcopy(gamma2)
                c = copy.deepcopy(c2)
            else:
                rand = random.randrange(0,1)
                if rand < e **(-roznica/temperatura):
                    s = copy.deepcopy(s2)
                    gamma = copy.deepcopy(gamma2)
                    c = copy.deepcopy(c2)
            # print(s)
        temperatura = temperatura - 1
        if czas_najlepszy >= 1000:
            break
    #     print("wartosc po przejsciu: " + str(s))
    print("najlepsze wagi,gamma,c: " + str(s_najlepsze) + str(gamma_najlepsze) + str(c_najlepsze) + " dają czas: " + str(czas_najlepszy))
    return s_najlepsze

            ########### dzialanie programu ##############################################################

if __name__ == "__main__":
    liczba_regol = 10
    wagi = []
    for i in range(liczba_regol):
        r = random.uniform(-1, 1)
        wagi.append(r)
    c ,gamma = ustawienie_c_i_gamma()

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

    ################################################### UCZENIE ########################################################

    najlepsze_proporcje = symulowane_wyzarzanie(O,O_max,x,max_x,czas,X_predkosc,O_predkosc,wagi,c,gamma)

