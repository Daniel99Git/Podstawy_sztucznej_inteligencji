import numpy as np
import random

def utworzListeSasiadow(listaPunktow, Q, eps): #Q to aktualny punkt do którego szukam sasiadów
    listaSasiadow = []
    for P in listaPunktow:
        if np.linalg.norm(Q-P) <= eps:
            listaSasiadow.append(P)
    return np.array(listaSasiadow)

def DBSCAN(listaPunktow, eps, minPts, label):
    C = 0 #klaster
    for i in range(len(listaPunktow)):
        if label[i] !=0: # 0 jest undefined
            continue
        listaSasiadow = utworzListeSasiadow(listaPunktow, listaPunktow[i], eps)
        if len(listaSasiadow) < minPts:
            label[i] = 999 #przypisuje liczbe jako noise żeby nie konwertowac tablicy string
            continue
        C += 1
        label[i] = C #przypisanie punktu do klatsra
        sasiedztwo = np.copy(listaSasiadow)
        sasiedztwo = np.unique(sasiedztwo)
        for j in range(len(sasiedztwo)):
            sasiedztwo = np.unique(sasiedztwo)
            indeks = 0
            if len(listaPunktow) > 1:
                for k in range(len(listaPunktow)): #tworze dodatkową petle aby znalezc indeks punktu z glownej tablicy punktow
                    if sasiedztwo[j] == listaPunktow[k]:
                        indeks = k
            if label[indeks]  == 999:
                label[indeks] = C
            if label[indeks] != 0:
                continue
            label[indeks] = C
            listaSasiadow = utworzListeSasiadow(listaPunktow, listaPunktow[indeks], eps)
            if len(listaSasiadow) >= minPts:
                sasiedztwo = np.vstack(sasiedztwo, listaSasiadow)

    return listaPunktow, label
liczbaElementow = 100
listaPozycjiWozka = np.random.uniform(-2.4, 2.4, size=liczbaElementow)
listaKatowWahadla = np.random.randint(-36, 36, size=(liczbaElementow, 2))
listaPunktow = np.column_stack((listaPozycjiWozka, listaKatowWahadla))
label = np.zeros(len(listaPunktow))
eps = 5.0
minPts = 3


punkty, klastry = DBSCAN(listaPunktow, eps, minPts, label)
print (np.column_stack((punkty, klastry)))


