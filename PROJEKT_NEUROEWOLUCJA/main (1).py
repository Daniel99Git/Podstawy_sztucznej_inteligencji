import math
import numpy as np
import pandas as pd
from random import randint
from numpy.random import permutation
from math import isnan
import random


class Neuroewolucja:
    def __init__(self):
        # config
        self.population_size = 100 #ilosc osobników w populacji
        self.max_iter = 1 #ilość iteracji całej populacji

        self.data = pd.read_csv("./trasy2.csv", delimiter=";")
        self.points = self.data.iloc[100:, :6].values
        self.population = self.create_population(self.population_size) #utworzenie populacji z punktów
        [self.blueprints, self.points] = self.split_data(self.data) #utworzenie tablic wskaźników i blueprintów
        self.split_data(self.data) #połączenie danych

        # ocena blueprintow i wskaznikow
        self.pointers_fitness = self.fitness(self.population, self.points, self.blueprints)  # ma wartości F dla kazdego wskaznika
        self.blueprints_fitness = self.assign_fitness() #przypisanie wartości fitness dla blueprntów

    #glowna funkcja
    def run(self): #główna pętla
        for i in range(self.max_iter):
            self.PSO(self.blueprints, self.blueprints_fitness) #algorytm PSO dla blueprintow
            #self.PSO(self.population, self.pointers_fitness) #algorytm PSO dla wskaznikow

    def PSO(self, arr, fitness_array):
        v1 = np.zeros(shape=(100,6)) #utworzenie tablic v i v1 (starych i nowych prędkości)
        v = np.zeros(shape=(100,6))
        glb = 4 #przypisanie indeksu globalnego maksimum
        locfit = np.zeros(shape=(100,6)) #tablica lokalnych maksimum
        for i in range(len(arr)): #pętla przypisanie początkowych wartości jako lokalne maksimum
                locfit[i] = arr[i]
        alfa = 0.3 #utworzenie zmiennych alfa i beta(stałe)
        beta = 0.3
        for pso_iter in range(100):
            print(arr[1])
            blueprints_fitness2 = self.assign_fitness() #przypisanie pomocniczej tablicy fitness lokalnego
            for i in range(len(arr)):   #szukanie globalnego maximum
                if blueprints_fitness2[glb] is not math.inf:
                    if blueprints_fitness2[glb] < blueprints_fitness2[i]:
                        glb = i #też powinien być wektor
            for i in range(len(arr)): #pętla wwyliczająca prędkość
                v1[i] = v[i] + alfa*(glb-arr[i]) + beta*(locfit[i]-arr[i]) #predkosc
                arr[i] = arr[i]+v1[i]
                v[i] = v1[i]

            self.blueprints_fitness = self.assign_fitness() #przypisanie fitness dla nowej iteracji
            for i in range(len(arr)):
                if self.blueprints_fitness[i] > blueprints_fitness2[i]: #jeżeli nowy fitness jest lepszy, podmieniamy maksimum lokalne
                    locfit[i] = arr[i]

    def create_population(self, population_size): #losowanie wartości wskaźników
        population = []
        for i in range(population_size):
            item = np.zeros(3, )
            for x in range(3):
                val = randint(0, 99)
                while val in item: #przypisanie losowych wartości wskaźników (indeksy 0-99)
                    val = randint(0, 99)
                item[x] = val
            population.append(item)

        return population

    #zwraca w jednej zmiennej 100 pierwszych punktow jako blueprinty i pozostale punkty w drugiej zmiennej
    def split_data(self, data):
        rows = np.shape(data)[0] #utworzenie wierszy
        perm = permutation(rows) #metoda tasująca losowo poszczególne rzędy (blueprinty)
        blueprints = perm[:100] #przypisanie potasowanych rzędów jako blueprinty
        points = perm[100:] #utworzenie pozostłych punktów
        return [data.iloc[blueprints, :6].values, data.iloc[points, :6].values] #zwrócenie tablicy blueprintów i pozostałych

    def fitness(self, population, points, blueprints):
        #przypisanie rozmiarow danych do zmiennych
        individual_size = np.shape(population)[1] # 3 centroidy
        blueprints_size = np.shape(blueprints)[0] # 100 bluprintow
        points_size = np.shape(points)[0] # punkty
        distance_matrix = np.zeros((blueprints_size, individual_size, points_size)) #stworzenie macierzy dla dystansu
        fitness_output = [[dict() for _ in range(points_size)] for x in range(blueprints_size)] #macierz wynikowa

        #obliczanie dystansu dla wszystkich osobnikow wzgledem punktow
        for point_idx in range(points_size): #pętla wyliczająca odległośći od centrów
            for blueprint_idx in range(blueprints_size):
                for individual_idx in range(individual_size):
                    p1 = blueprints[int(population[blueprint_idx][individual_idx])]
                    p2 = points[point_idx]
                    distance_matrix[blueprint_idx, individual_idx, point_idx] = self.euclidian_distance(p1, p2) #wyliczenie dystansu p1 (centra) od p2(punktu)
                [id, val] = self.find_min_index(distance_matrix[blueprint_idx, :, point_idx]) #utworzenie macierzy przypisując im ID
                fitness_output[blueprint_idx][point_idx] = {"id": id, "dist": val} #sformatowanie fitnessów na id:, dist:

        #wyznaczenie wartosci f dla osobnikow na podstawie macierzy dystansu
        individual_fitness = np.zeros((blueprints_size,)) #pojedynczy fitness centra
        for individual_idx in range(len(fitness_output)):
            individual_dist_sum = np.zeros((3,)) # średnia odległość od punktu od klastra
            individual_points_count = np.zeros((3,)) #ilość punktów w klastrze
            for point in fitness_output[individual_idx]:
                individual_dist_sum[point["id"]] = individual_dist_sum[point["id"]] + point["dist"]
                individual_points_count[point["id"]] = individual_points_count[point["id"]] + 1
                b1 = blueprints[int(population[blueprint_idx][0])] #przypisanie każdemu punktowi najbliższego centra
                b2 = blueprints[int(population[blueprint_idx][1])]
                b3 = blueprints[int(population[blueprint_idx][2])]
            M = self.mean_blueprint_distance(b1, b2, b3) #średnia odleglosc między centroidami
            L = []
            for i in range(len(individual_points_count)): #pętla przypisująca ilość puntów przypisanych do każdego centra
                if individual_points_count[i] > 0:
                    L.append(individual_dist_sum[i] / individual_points_count[i])
                else:
                    L.append(0)
            f = (sum(val for val in L if not isnan(val)) / 3) / M #policzenie finalnego fitnessu dla każdego centra, na podstawie ilości punktów, średniej
            individual_fitness[individual_idx] = f
        return individual_fitness

    def euclidian_distance(self, p1, p2): #odległość ekulidesowa
        val = 0
        dimensions = len(p1)
        for i in range(dimensions):
            val = val + (p1[i] - p2[i]) ** 2
        val = val ** 0.5
        return val

    def mean_blueprint_distance(self, b1, b2, b3): #średni dystans między centroidami (M)
        d1 = self.euclidian_distance(b1, b2)
        d2 = self.euclidian_distance(b1, b3)
        d3 = self.euclidian_distance(b3, b2)
        return (d1 + d2 + d3) / 3

    def find_min_index(self, arr): #metoda zwracająca minimum(f)
        min_val = arr[0]
        min_idx = 0
        for i in range(len(arr)):
            if arr[i] < min_val:
                min_val = arr[i]
                min_idx = i
        return [min_idx, min_val]

    #na podstawie wartosci wskaznikow tworzona jest tablica wartosci dla blueprintow
    def assign_fitness(self):
        fitness = np.ones((self.population_size,)) * np.inf #wykluczenie wartości nieprawidłowych
        for i in range(self.population_size): #pętla przypisująca najlepszy fitness, jeżeli jest większy, podmieniamy.
            for id in self.population[i]:
                rate = self.pointers_fitness[i]
                if fitness[int(id)] > rate:
                    fitness[int(id)] = rate

        return fitness

ne = Neuroewolucja()
ne.run()