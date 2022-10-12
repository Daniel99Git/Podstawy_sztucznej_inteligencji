import math
import random
import numpy as np
import pygame, sys
from pygame.locals import *


                ################################################    PERCEPTRON    ########################################################

wagi = [[[ 0.51861536,  0.68686902, -0.61882454],
       [ 0.44331297, -0.15840287,  0.12906834],
       [-0.08508329,  0.77042587,  0.59692246],
       [-0.22254277, -0.93350914, -0.5850257 ]],

        [[-0.7388941, 0.57102073, -0.21235047],
         [0.63335724, 0.1048588, -0.16242957],
         [0.48996685, 0.5404248, -0.68059463]],

        [[-0.87611499, -0.11740482],
         [-0.61929822, 0.0282507],
         [-0.01342234, 0.48338039]],

        [[-0.44628651, 0.73116598],
         [0.58547502, -0.63887101]],

        [[-0.59292678],
         [0.79618677]]]

def licz_siec(wejscia, wagi_warstw):  # Działanie sieci
    pierwsza_warstwa = np.dot(wejscia, wagi_warstw[0])
    druga = np.dot(pierwsza_warstwa, wagi_warstw[1])
    trzecia = np.dot(druga, wagi_warstw[2])
    czwarta = np.dot(trzecia, wagi_warstw[3])
    piata = np.dot(czwarta, wagi_warstw[4])
    return float(piata)

def licz_czas(O,O_max,x,max_x,czas,X_predkosc,O_predkosc,nowe_wagi):  # liczenie błędu sieci

    while O <= O_max and O >= -O_max and czas <= 1000 and x >= -max_x and x <= max_x:           # 1000 ==> Czas trwania ustalony, by wózek nie jeżdził w nieskończoność
        # Użycie sieci
        wejscia = [x, X_predkosc, O, O_predkosc]
        F = licz_siec(wejscia, nowe_wagi) * 10
        if F > 10:
            F = 10
        if F < -10:
            F = -10

        Fi = licz_Fi(m_wahadla, l, O, O_predkosc, Up)
        mi = licz_mi(m_wahadla, O)
        przyspieszenie_wozka = licz_przyspieszenie_X(F, Uc, X_predkosc, M_wozka, Fi, mi)
        przyspieszenie_wachadla = licz_przyspieszenie_O(l, przyspieszenie_wozka, O, Up, O_predkosc, m_wahadla)
        print("Obecny kąt: " + str(O) + " Położenie wózka " + str(x) + ' wózek: ' + str(
            przyspieszenie_wozka) + ' wahadło: ' + str(przyspieszenie_wachadla) + " X*: " + str(
            X_predkosc) + " wahadlo*: " + str(O_predkosc) + " Czas: " + str(czas) + "Siła: " + str(F))

        # Zmiana parametrów pod wpływem czasu
        x = x + t * X_predkosc
        X_predkosc = X_predkosc + t * przyspieszenie_wozka
        O = O - t * O_predkosc
        O_predkosc = O_predkosc + t * przyspieszenie_wachadla

        czas = czas + t
    return czas

def losowanie_z_krokiem(warstwa, krok):  # losowanie nowych wartości przy uwzględnieniu kroku w symulowanym wyszarzaniu
    for i in range(0, len(warstwa)):
        for j in range(0, len(warstwa[i])):
            x = warstwa[i][j] - krok
            y = warstwa[i][j] + krok
            if x < -1: x = -1
            if y > 1: y = 1
            warstwa[i][j] = random.uniform(x, y)
    return warstwa
                #######################################    SYMULATOR WÓZKA    ##############################################
        #    math.sin(math.radians(90))  --> Liczenie sinus 90 stopni

g = 9.8           # Przyspieszenie ziemskie w m/(s do kwadratu)
l = 0.5  # metry - długość wahadła
drugi_l = 0.05   # metry - długość drugiego wahadła
m_wahadla = 0.1  # kilogramy - masa wahadła
m_drugiego_wahadla = 0.01  # kilogramy - masa wahadła
O_max = 12   # stopnie - maksymalne wychylenie wahadła na plus lub minus
O_max_drugie = 36  # stopnie - wychylenie DRUGIEGO wahadła jeśli istnieje
O = -9 # stopnie obecnego wychylenia
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
    ulamek = (Upi*O_predkosc) / (m*0.5*li)
    return -0.75 * ( przyspieszenie_X*math.cos(math.radians(Oi)) + g*math.sin(math.radians(Oi)) + ulamek)

def pokaz_tyczke(O):
    wynik = O * (8)
    x = wynik + 100
    y = wynik - 100
    if O < 0:
        y = -wynik - 100
    return [x,y]




    ##################################    WIZUALIZACJA WÓZKA PRZY POMOCY "PYGAME"    ##########################################
pygame.init()  # inicjacja modułu
FPS = 1000
fpsClock = pygame.time.Clock()
OKNO_SZER = 1200
OKNO_WYS = 600
OKNO = pygame.display.set_mode((OKNO_SZER, OKNO_WYS), 0,
                                  32)  # przygotowanie powierzchni do rysowania, czyli inicjacja okna wizualizacji
pygame.display.set_caption('Wizualizacja wózka z tyczką')  # tytuł okna gry
# kolory wykorzystywane w wizualizacji, których składowe RGB zapisane są w tuplach
LT_BLUE = (230, 255, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
###           OBIEKTY GRAFICZNE           ##
# szerokość, wysokość i pozycja wózka i tyczki
koniec_szer = 5; koniec_wys = 10
koniec_obr = pygame.Surface([koniec_szer, koniec_wys])
koniec_prost = koniec_obr.get_rect()
koniec_prost.x = max_x+100; koniec_prost.y = 250
poczatek_szer = 5; poczatek_wys = 10
poczatek_obr = pygame.Surface([poczatek_szer, poczatek_wys])
poczatek_prost = poczatek_obr.get_rect()
poczatek_prost.x = -max_x+100; poczatek_prost.y = 250
srodek_szer = 5; srodek_wys = 10
srodek_obr = pygame.Surface([srodek_szer, srodek_wys])
srodek_prost = srodek_obr.get_rect()
srodek_prost.x = 500; srodek_prost.y = 250

wozek_szer = 200
wozek_wys = 20

# Inicjacja wózka i tyczki:# utworzenie powierzchni dla obrazka, wypełnienie jej kolorem,# pobranie prostokątnego obszaru obrazka i ustawienie go na wstępnej pozycji
wozek_poz = (400, 200)  # początkowa pozycja wózka
wozek_obr = pygame.Surface([wozek_szer, wozek_wys])
wozek_obr.fill(BLUE)
wozek_prost = wozek_obr.get_rect()
wozek_prost.x = wozek_poz[0]
wozek_prost.y = wozek_poz[1]

tyczka_szer = 5; tyczka_wys = 5
tyczka_obr = pygame.Surface([tyczka_szer, tyczka_wys], pygame.SRCALPHA, 32).convert_alpha()
pygame.draw.ellipse(tyczka_obr, RED, [0, 0, tyczka_szer, tyczka_wys])
tyczka_prost = tyczka_obr.get_rect(); tyczka_prost.x = OKNO_SZER / 2; tyczka_prost.y = 100

tyczka2_szer = 5; tyczka2_wys = 5
tyczka2_obr = pygame.Surface([tyczka2_szer, tyczka2_wys], pygame.SRCALPHA, 32).convert_alpha()
pygame.draw.ellipse(tyczka2_obr, RED, [0, 0, tyczka2_szer, tyczka2_wys])
tyczka2_prost = tyczka2_obr.get_rect(); tyczka2_prost.x = OKNO_SZER / 2; tyczka2_prost.y = 120

tyczka3_szer = 5; tyczka3_wys = 5
tyczka3_obr = pygame.Surface([tyczka3_szer, tyczka3_wys], pygame.SRCALPHA, 32).convert_alpha()
pygame.draw.ellipse(tyczka3_obr, RED, [0, 0, tyczka3_szer, tyczka3_wys])
tyczka3_prost = tyczka3_obr.get_rect(); tyczka3_prost.x = OKNO_SZER / 2; tyczka3_prost.y = 140

tyczka4_szer = 5; tyczka4_wys = 5
tyczka4_obr = pygame.Surface([tyczka4_szer, tyczka4_wys], pygame.SRCALPHA, 32).convert_alpha()
pygame.draw.ellipse(tyczka4_obr, RED, [0, 0, tyczka4_szer, tyczka4_wys])
tyczka4_prost = tyczka4_obr.get_rect(); tyczka4_prost.x = OKNO_SZER / 2; tyczka4_prost.y = 160

tyczka5_szer = 5; tyczka5_wys = 5
tyczka5_obr = pygame.Surface([tyczka5_szer, tyczka5_wys], pygame.SRCALPHA, 32).convert_alpha()
pygame.draw.ellipse(tyczka5_obr, RED, [0, 0, tyczka5_szer, tyczka5_wys])
tyczka5_prost = tyczka5_obr.get_rect(); tyczka5_prost.x = OKNO_SZER / 2; tyczka5_prost.y = 180




    ##################################    DZIAŁANIE NAUCZONEJ SIECI    #########################################

while O <= O_max and O >= -O_max and czas <= 1000 and x >= -max_x and x <= max_x:           # 1000 ==> Czas trwania ustalony, by wózek nie jeżdził w nieskończoność
    # Użycie sieci
    wejscia = [x, X_predkosc, O, O_predkosc]
    F = licz_siec(wejscia, wagi) * 10
    if F > 10:
        F = 10
    if F < -10:
        F = -10

    Fi = licz_Fi(m_wahadla, l, O, O_predkosc, Up)
    mi = licz_mi(m_wahadla, O)
    przyspieszenie_wozka = licz_przyspieszenie_X(F, Uc, X_predkosc, M_wozka, Fi, mi)
    przyspieszenie_wachadla = licz_przyspieszenie_O(l, przyspieszenie_wozka, O, Up, O_predkosc, m_wahadla)
    print("Obecny kąt: " + str(O) + " Położenie wózka " + str(x) + ' wózek: ' + str(
        przyspieszenie_wozka) + ' wahadło: ' + str(przyspieszenie_wachadla) + " X*: " + str(
        X_predkosc) + " wahadlo*: " + str(O_predkosc) + " Czas: " + str(czas) + "Siła: " + str(F))

    szerokosc_do_wizualizacji = 400 + (x * (50/3))
    wozek_prost.x = szerokosc_do_wizualizacji

    # Zmiana parametrów pod wpływem czasu
    x = x + t * X_predkosc
    X_predkosc = X_predkosc + t * przyspieszenie_wozka
    O = O - t * O_predkosc
    O_predkosc = O_predkosc + t * przyspieszenie_wachadla



    wymiary = pokaz_tyczke(O)
    tyczka_prost.x = szerokosc_do_wizualizacji + (O*20)+100; tyczka_prost.y = wozek_poz[1] + wymiary[1]
    tyczka2_prost.x = szerokosc_do_wizualizacji + (O*4)+100; tyczka2_prost.y = wozek_poz[1] + (wymiary[1] * 0.2)
    tyczka3_prost.x = szerokosc_do_wizualizacji + (O*8)+100; tyczka3_prost.y = wozek_poz[1] + (wymiary[1] * 0.4)
    tyczka4_prost.x = szerokosc_do_wizualizacji + (O*12)+100; tyczka4_prost.y = wozek_poz[1] + (wymiary[1] * 0.6)
    tyczka5_prost.x = szerokosc_do_wizualizacji + (O*16)+100; tyczka5_prost.y = wozek_poz[1] + (wymiary[1] * 0.8)

    koniec_prost.x = 500 + max_x * (50/3)
    poczatek_prost.x = 500 - (max_x * (50/3))
    srodek_prost.x = 500

    OKNO.fill(LT_BLUE)  # kolor okna
    OKNO.blit(wozek_obr, wozek_prost)  # Rysowanie wózka i tyczki
    OKNO.blit(tyczka_obr, tyczka_prost);OKNO.blit(tyczka2_obr, tyczka2_prost);OKNO.blit(tyczka3_obr, tyczka3_prost);OKNO.blit(tyczka4_obr, tyczka4_prost);OKNO.blit(tyczka5_obr, tyczka5_prost)
    OKNO.blit(koniec_obr, koniec_prost)
    OKNO.blit(poczatek_obr, poczatek_prost)
    OKNO.blit(srodek_obr, srodek_prost)

    pygame.display.update()  # zaktualizuj okno i wyświetl
    fpsClock.tick(FPS)  # zaktualizuj zegar po narysowaniu obiektów

    czas = czas + t