import math

def licz_Fi(m,li,Oi,O_kropka,Upi,g):     #liczenie siły
    pierwsza_czesc = m * 0.5*li * Oi**2 * (math.sin(math.radians(Oi)))
    druga_czesc = 0.75*m * math.cos(math.radians(Oi)) * ((Upi*O_kropka)/(m*0.5*li)) + g*math.sin(math.radians(Oi))
    return pierwsza_czesc + druga_czesc

def licz_mi(mi,Oi):                     # liczenie masy względem kąta
    cos = math.cos(math.radians(Oi))
    return mi * (1 - (0.75 * cos**2))

def licz_przyspieszenie_X(F,Uc,x_predkosc,M,Fi_fala,mi_fala):     # Na początku dla jednego wahadła
    gora = F - Uc * + Fi_fala
    dol = M + mi_fala
    return gora / dol

def licz_przyspieszenie_O(li,przyspieszenie_X,Oi,Upi,O_predkosc,m,g):     # Przyspieszenie kątowe wahadła
    ulamek = (Upi*O_predkosc) / (m*0.5*li)
    return -0.75 * ( przyspieszenie_X*math.cos(math.radians(Oi)) + g*math.sin(math.radians(Oi)) + ulamek)
        #    math.sin(math.radians(90))  --> Liczenie sinus 90 stopni

if __name__ == "__main__":
    g = 9.8           # Przyspieszenie ziemskie w m/(s do kwadratu)
    l = 0.5  # metry - długość wahadła
    drugi_l = 0.05   # metry - długość drugiego wahadła
    m_wahadla = 0.1  # kilogramy - masa wahadła
    m_drugiego_wahadla = 0.01  # kilogramy - masa wahadła
    O_max = 12   # stopnie - maksymalne wychylenie wahadła na plus lub minus
    O_max_drugie = 36  # stopnie - wychylenie DRUGIEGO wahadła jeśli istnieje
    O = -1 # stopnie obecnego wychylenia
    O_drugie = 0  # stopnie obecnego wyhylenia 2 wahadła

    x = 0
    max_x = 2.4  # metry -  maksymalna pozycja wózka  ( -2.4 do 2.4 m)
    M_wozka = 1    # kilogramy - masa wózka
    F = 0    #od -10N do 10 Newtonów
    Uc = 0.0005     # współczynnik tarcia wózka
    Up = 0.000002   # Współczynnik tarcia wahadła na wózku ( dla obu wahadeł takie samo)
    t = 0.02        # sekundy - wielkość kroku

    czas = 0        # sekundy  - obecny upływ czasu
    czas_trwania = 10   # sekundy - czas trwania całego doświadczenia

    N = 1           # ilość wahadeł

    X_przyspieszenie = 0  # m/(s do kwadratu) - Przyspieszenie wózka     ( X z 2-ma kropkami)
    O_przyspieszenie = 0  # m/(s do kwadratu) - Przyspieszenie wahadła  ( O z 2-ma kropkami)
    O_2_przyspieszenie = 0  # -||- drugiego wahadła
    X_predkosc = 0   # prędkość wózka                                    ( X z jedną kropką)
    O_predkosc = 0   # prędkość wahadła                                 ( O z jedną kropką)
    O_drugie_predkosc = 0   # prędkość drugiego wahadła



    Fi = licz_Fi(m_wahadla,l,O,O_predkosc,Up,g)
    mi = licz_mi(m_wahadla,O)
    przyspieszenie_wozka = licz_przyspieszenie_X(F,Uc,X_predkosc,M_wozka,Fi,mi)
    przyspieszenie_wachadla = licz_przyspieszenie_O(l,przyspieszenie_wozka,O,Up,O_predkosc,m_wahadla,g)
    print('fi: ' + str(Fi) + ' mi: ' + str(mi) + ' wózek: ' + str(przyspieszenie_wozka) + ' wahadło: ' + str(przyspieszenie_wachadla))
    print(" ")

    dane_do_uczenia_DB_Scan = []

    while O <= O_max and O >= -O_max and czas <= czas_trwania:
                                    # Obliczenia parametrów wózka po upływoie czasu
        Fi = licz_Fi(m_wahadla, l, O, O_predkosc, Up,g)
        mi = licz_mi(m_wahadla, O)
        przyspieszenie_wozka = licz_przyspieszenie_X(F, Uc, X_predkosc, M_wozka, Fi, mi)
        przyspieszenie_wachadla = licz_przyspieszenie_O(l, przyspieszenie_wozka, O, Up, O_predkosc, m_wahadla,g)
        print("Obecny kąt: " + str(O) + " Położenie wózka " + str(x) + ' wózek: ' + str(przyspieszenie_wozka) + ' wahadło: ' + str(przyspieszenie_wachadla) + " X* : " + str(X_predkosc) + "wahadlo*: " + str(O_predkosc) + " Obecny upływ czasu: " + str(czas))


        stan_wozka = [x, X_predkosc, O, O_predkosc]
        dane_do_uczenia_DB_Scan.append(stan_wozka)

                                    # Zmiana parametrów pod wpływem czasu
        x = x + t * X_predkosc
        X_predkosc = X_predkosc + t * przyspieszenie_wozka
        O = O - t * O_predkosc
        O_predkosc = O_predkosc + t * przyspieszenie_wachadla


        czas = czas + t

    # file = open("dane_minus.txt", "w")
    # for i in dane_do_uczenia_DB_Scan:
    #     file.write(str(i)+"\n")
    # file.close()


