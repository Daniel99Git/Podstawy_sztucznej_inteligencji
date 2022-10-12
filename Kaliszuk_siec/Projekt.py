import numpy as np
import sklearn.metrics as cma
import math, random
import pandas as pd
from sklearn import datasets
import time


iris = datasets.load_iris() #wczytanie danych
X = iris.data #podpisanie zbioru pod zmienną X
y = list(iris.target + 1)
#print(y)

ilość_neuronów = 3 #Ilość neuronów
#Zmienne do DBSCAN
C = 0 #licznik klastry
klastry = []
minpkt = 3 #minimum punktów
maxodl = 4.43 #minimalna odległość
wymiardanych = 4

X = np.insert(X, 4, 0, axis = 1) #Dodanie 5 kolumny określającej przynależość

#print("Dane: " ,X)

for i in range(len(X)):
    zbior = []
    odw = []
    if X[i][wymiardanych] == 0:
        for j in range(len(X)):
            odl = 0
            for k in range(wymiardanych):
                odl = odl + abs(X[i][k] - X[j][k])
            if odl <= maxodl:
                dod = X[j]
                zbior.append(dod)
                odw.append(j)
        if len(zbior) > minpkt:
            C += 1
            for g in range(len(odw)):
                X[odw[g]][wymiardanych] = C
            for e in range(len(zbior)):
                zbior[e][wymiardanych] = C
                dod2 = zbior[e]
                klastry.append(dod2)
    else:
        continue

iris_1 = []
iris_2 = []
iris_3 = []
#Wyodrębnienie klastrów
for i in range(len(X)):
    if X[i][4] == 1:
        iris_1.append(X[i])
for i in range(len(X)):
    if X[i][4] == 2:
        iris_2.append(X[i])
for i in range(len(X)):
    if X[i][4] == 3:
        iris_3.append(X[i])
#print(iris_1)
#print(iris_2)
#print(iris_3)
#Usunięcie 5 kolumny
a = np.delete(iris_1, 4, 1)
b = np.delete(iris_2, 4, 1)
c = np.delete(iris_3, 4, 1)

#Wyznaczenie centrów klastrów
aa = np.sum(a,axis = 0)
a1 = aa/len(a)
bb = np.sum(b,axis = 0)
b1 = bb/len(b)
cc = np.sum(c,axis = 0)
c1 = cc/len(c)

centra_klastrów = [a1,b1,c1]
print ("Centra klastrów na podstawie dbscan",centra_klastrów)

#przygotowanie danych do obliczeń
f_res = []
for i in X:
    res = []
    for j in centra_klastrów:
        temp = []
        for x, z in zip(i, j):
            temp.append(x - z)
        temp = np.array(temp)
        res.append(math.exp(-np.dot(temp, temp.T)/2)) #użycie wzoru z prezentacji
    #print(res)
    f_res.append(res)
#print(f_res)

final_data = np.full((150,ilość_neuronów+2), 0.0)

for k in range(150):
    temp = [1]
    temp = np.concatenate((temp, f_res[k], [y[k]]))
    final_data[k] = temp #finalny zbiór danych
#print(final_data)
train_data = np.zeros(shape=(120,ilość_neuronów+2)) #zadeklarowanie pustch zbiorów danych uczących
test_data = np.zeros(shape=(30,ilość_neuronów+2)) #zadeklarowanie pustch zbiorów danych testowych

l = 0
k = 0
#Podział na dane uczące i dane przeznaczone do testu.
for i in range(150):
    if i % 5 == 0:
        test_data[l] = final_data[i] #przypisanie danych testowych, 30 danych
        l += 1
    else:
        train_data[k] = final_data[i] #przypisanie danych uczących, 120 danych
        k+= 1
#print(test_data)
#print(train_data)
wagi = np.array([[random.uniform(-10, 10) for i in range(ilość_neuronów+1)], [random.uniform(-10, 10) for i in range(ilość_neuronów+1)], #wygenerowanie wstępnych wag
                      [random.uniform(-10, 10) for i in range(ilość_neuronów+1)]])
print("Losowe wagi wstępne: ",wagi)

eta = 0.1 #Współczynnik uczenia
def model_uczacy(label):
    pdt = 0
    licznik = 20
    while licznik > 0:
        for i in train_data:

            pdt = np.dot(i[:-1], np.transpose(wagi[label - 1]))
            #print("Wynik: ", pdt)
            if (i[-1] != label and pdt >= 0):
                wagi[label - 1] = wagi[label - 1] - eta * i[:-1] #współczynnik uczenia ujemny
            if (i[-1] == label and pdt < 0):
                wagi[label - 1] = wagi[label - 1] + eta * i[:-1] #współczynnik uczenia dodatni
        #print('wagi kolejnych iteracji: ',wagi)
        licznik -= 1

def identyfikacja_RBF(test_data):
    identyfikacja = [None]*30
    licznik = 0
    for i in test_data:
        test_prd_1 = np.dot(i[:ilość_neuronów + 1], np.transpose(wagi[0])) #mnożenie przez wagi
        test_prd_2 = np.dot(i[:ilość_neuronów + 1], np.transpose(wagi[1])) #mnożenie przez wagi
        test_prd_3 = np.dot(i[:ilość_neuronów + 1], np.transpose(wagi[2])) #mnożenie przez wagi

        if test_prd_1 >= 0:
            identyfikacja[licznik] = "iris_satosa"
        elif test_prd_2 >= 0:
            identyfikacja[licznik] = "iris_versicolour"
        elif test_prd_3 >= 0:
            identyfikacja[licznik] = 'iris_virginica'
        else:
            identyfikacja[licznik] = 'nie rozpoznano'
        licznik += 1
        print("Identyfikacja",licznik,"danej testowej:",identyfikacja[licznik-1])
        time.sleep(0.5)

model_uczacy(1)
model_uczacy(2)
model_uczacy(3)
print ("Końcowe wagi:", wagi)
identyfikacja_RBF(test_data) #final_data zbiór obrobionych danych gotowych do identyfikacji