import numpy as np
import matplotlib.pyplot as plt
import math
# zmienna z najlepszym wynikiem- używana przy wykresie
last_good_configuration = dict.fromkeys(['time', 'sigma', 'centers', 'wages', 'x_plot', 'y_plot', 'y2_plot', 'y3_plot'])

dlugoscPatyka = 0.5
dlugoscPatyka1 = 0.05
masaPatyka = 0.1
masaPatyka1 = 0.1
masaWozka = 1
grawitacja = 9.8
miC = 0.0005
miP = 0.000002
czas = 0.02

class Pendulum:
    def __init__(self):
        self.pozycja = 0
        self.kat = 4
        self.kat1 = 0

        self.pX = 0
        self.pKat = 0
        self.pKat1 = 0
        self.time = 0

    def get_position(self):
        return self.pozycja

    def get_time(self):
        return self.time

    def get_kat(self):
        return self.kat

    def get_kat1(self):
        return self.kat1

    # metoda run() przyjmuje jako argument force która popycha wózek jakąś siłą w danym
    # momencie zależnym od iteracji. Operujemy siłą force
    # i tak wyliczoną siłą ten wózek wprawiać w ruch
    # jeśli force = 0 - nic się nie zmienia w ruchu wózka - jedzie zgodnie
    # z prędkością nadaną w poprzedniej iteracji
    # jeśli force < 0 - wózek zwalnia, jeśli wcześniej jechał do przodu
    # lub przyspiesza cofanie, jeśli jechał do tyłu
    # jeśli force > 0 - wózek przyspiesza, jeśli wcześniej jechał do przodu
    # lub zwalnia cofanie, jeśli jechał do tyłu
    def run(self, force):
        md = masaPatyka * dlugoscPatyka
        md1 = masaPatyka1 * dlugoscPatyka1

        pom11 = (miP * self.pKat) / md
        pom21 = grawitacja * np.sin(self.kat)

        pom12 = (miP * self.pKat1) / md1
        pom22 = grawitacja * np.sin(self.kat1)

        fF = md * self.kat * self.kat * np.sin(self.kat) + 0.75 * masaPatyka * np.cos(self.kat) * (pom11 + pom21)
        mF = masaPatyka * (1 - 0.75 * np.cos(self.kat) * np.cos(self.kat))

        fF1 = md1 * self.kat1 * self.kat1 * np.sin(self.kat1) + 0.75 * masaPatyka1 * np.cos(self.kat1) * (pom12 + pom22)
        mF1 = masaPatyka1 * (1 - 0.75 * np.cos(self.kat1) * np.cos(self.kat1))

        dpX = (force - miC + fF + fF1) / (masaWozka + mF + mF1)
        dpKat = -0.75 * (dpX * np.cos(self.kat) + pom21 + pom11) / dlugoscPatyka
        dpKat1 = -0.75 * (dpX * np.cos(self.kat1) + pom22 + pom12) / dlugoscPatyka1

        self.pX = self.pX + dpX * czas
        self.pKat = self.pKat + dpKat * czas
        self.pKat1 = self.pKat1 + dpKat1 * czas

        self.pozycja = self.pozycja + self.pX * czas
        self.kat = self.kat + self.pKat * czas
        self.kat1 = self.kat1 + self.pKat1 * czas
        self.time += czas


# liczba wchodzących danych do sieci - 6 (tyle elementów z powyższej
# klasy jest ważne w procesie uczenia się sieci, wrzucone do
# zmiennej X)
num_of_x = 6


# funkcja fi - według wzorów
def fi(x, c, s) -> float:
    # warunek - jeśli liczba z tej
    # potęgi jest zbyt duża, to zwracamy małą liczbę(problemy z licz. macierzy)
    if -math.pow(((x - c) / (s)), 2) < -1e7:
        return 1

    return math.exp(-math.pow(((x - c) / (s)), 2))


# sieć neurorozmyta - dostaje na wejściu:
# X - wartości z klasy, które wpływają na proces uczenia
# c - centra funkcji fi w neuronach radialnych
#     Centra, wagi losowane celem znalezienia najlepszej opcji
# s - parametr sigma w neuronach radialnych
#     Sigmy są losowane tak samo jak wagi w celu znalezienia najlepszego
#     zestawienia parametrów
#     na wyjściu dostajemy liczbę z zakresu 0-1 i oddejm 0.5 i dodaje do force
#     np dostajemy 0.7 - potem zostanie odjęte 0.5 - wychodzi 0.2 - wózek dostaje dodatkową siłę 0.2
#     dostajemy 0.1 - odejmujemy 0.5 - wychodzi -0.4 - siła wpływająca na wózek zmniejsza się o 0.4

#   sieć neuronowa uczy się bazując na:
# X - czyli [p.pozycja, p.kat, p.kat1, p.pX, p.pKat, p.pKat1]
# c,s,W - wartości, które wylicza na nowo, by maksymalizować czas z wagadłem w górze
def predict(X, c, s, W) -> float:
    # tworzenie matrycy dla FI - 2x 3 neurony radialne
    FI = np.zeros([(int)(num_of_x / 3), (int)(num_of_x / 2)])
    for i in range((int)(num_of_x / 3)):
        for j in range((int)(num_of_x / 2)):
             FI[0,0] = fi(X[0],c[0],s[0])
             FI[0,1] = fi(X[1],c[1],s[1])
             FI[0,2] = fi(X[2],c[2],s[2])
             FI[1,0] = fi(X[3],c[3],s[3])
             FI[1,1] = fi(X[4],c[4],s[4])
             FI[1,2] = fi(X[5],c[5],s[5])


    # dwa sumatory Y - wynikiem jest iloczyn trzech neuronów radialnych
    # po przejściu przez to mamy 2 wartości Y
    Y = np.ones(2)
    for i in range(2):
        for j in range((int)(num_of_x / 2)):
            Y[i] *= FI[i, j]

    # sum to iloczyn macierzy Y z macierzą wag W.
    # wynikiem są dwie liczby Sum[1], Sum[2]
    Sum = np.dot(Y, W)

    # reakcja na błędy
    # czasem sieć ma wyzerowaną drugą wartość, a wynikiem sieci jest Sum[0]/Sum[1],
    # co daje  błąd i program się nie przerywał, ale już nie
    # działał poprawnie. Rozwiązanie- zwrócenie wartości 0 w tym
    # przypadku - czyli według sieci w tym momencie trochę zwalniamy.

    if Sum[1] == 0:
        return 0

    # wynik sieci - dzielenie sum[0]/sum[1] jak w prezentacji góra/dól
    return (Sum[0] / Sum[1])


# main- start
def main():
    # wartości dla symulowanego wyżarzania
    # początkowa temperatura:   90
    # ostateczna temperatura:   0.1
    # mnożnik:  0.99    #do testów 0.9(krócej i bez zawiech)
    initial_temp = 90
    current_temp = initial_temp
    final_temp = 0.1
    alpha = 0.9

    # tworzymy obiekt klasy Pendulum
    p = Pendulum()

    # 6 wartości centrów - po 1 na każdy neuron radialny
    # losujemy w zakresie <-0.5, 0.5>
    c = np.random.random(num_of_x) - 1 / 2

    # 6 wartości sigma - po 1 na każdy neuron radialny
    # losowe inty w zakresie <1,9>
    sigma = np.random.randint(low=1, high=10, size=num_of_x)

    # wagi - dwie losowo, dwie mają wartość 1 (prezentacja)
    W = np.array([[np.random.random(), np.random.random()], [1, 1]])

    # pierwsze ruszenie pojazdu - siła = 0, czyli wózek
    # pierwsze ruszenie na losowych wagach - po tym działaniu wiadomo,
    # ile wytrzymał wózek kierowany taką siecią.
    force = 0

    # popchnięcie wózeka tą siłą
    p.run(force)

    # zapisanie poz_last i pX_last - wartości związane z przesunięciem.
    # w jednej iteracji sprawdzenie, o ile się przesunął wózek
    poz_last = 0
    pX_last = 0

    # sprawdzenie czy kąt wahadła jest w zakresie (-90, 90), czyli czy się nie wywróciło jeszcze
    while (p.get_kat() <= 90 and p.get_kat() >= -90):
        # sprawdzenie, o ile się przesunął wózek w tej iteracji
        poz_diff = p.pozycja - poz_last
        pX_diff = p.pX - pX_last

        # zapisanie obecnej pozycji jako ostatniej
        poz_last = p.pozycja
        pX_last = p.pX
        # tworzymy X, który będzie podlegał uczeniu
        # wartości wybrane metodą prób i błędów
        X = np.array([poz_diff, p.kat, p.kat1, pX_diff, p.pKat, p.pKat1])

        # do siły, która działa na wózek dodajemy wartość z wyjścia sieci, jednak - z racji
        # faktu, iż jest ona w zakresie <0,1>, to odejmuję od niej 0.5.
        # W tym momencie, jeśli jest mniejsza od 0.5 to zwalniamy, a jeśli
        # większa - przyspieszamy. Równe 0.5 powoduje niezmienność w sile
        force += predict(X, c, sigma, W) - 0.5

        # popychamy wózek
        p.run(force)

    # pobieramy czas, ile wózek wytrzymał na randomowych wartościach c,s,W
    time = p.get_time()

    # symulowane wyżarzanie- start
    #
    # warunek symulowanego wyżarzania - dopóki obecna temperatora jest większa
    # od finalnej
    while (current_temp > final_temp):
        print(f'temperatura: {format(current_temp, ".6f")}', end='\t') #wypisanie obecnej temperatury(wiemy w ktorej iter. najlepszy wynik

        # losujemy nowe wartości c, sigma, W
        new_c = np.random.random(num_of_x) - 0.5
        new_sigma = np.random.randint(low=1, high=10, size=num_of_x)

        # jedynki pozostają takie same - nie nadpisujemy ich zeby bylo jak we wzorach
        new_W = np.copy(W)
        for i in range(len(W)):
            for j in range(len(W[i])):

                #warunek o jedynkach - pominięcie ich
                if (W[i, j] != 1):
                    new_W[i, j] += np.random.random() - 0.5

        del (p) # del poprzedni wózek zachowując jego  wynik- czas

        #nowy wózek - zeruje się czas i wszystkie siły działające na niego
        p = Pendulum()

        force = np.random.randint(-10, 10) # los. początkowo działającą siłę

        # potraktowanie wózka tą siłą
        p.run(force)

        #dane do wykresu
        x_plot = []     #x  - czas
        y3_plot = []    # y3 - siła działająca na wózek w czasie
        y2_plot = []    # y2 - pozycja w czasie (ale wózek się porusza w 2D)
        y_plot = []     # y  - kąt wahadła w czasie

        # dopóki wahadło się nie przewróciło - w tym momencie liczymy wynik
        # naszej funkcji nagrody - czyli czas, jak długo wahadło się utrzymuje
        # jest to wynik, na podstawie którego będziemy wybierane coraz lepsze
        # rozwiązanie za pomocą symulowanego wyżarzania

        # zerowanie ostatniej pozycji
        poz_last = 0
        pX_last = 0


        while (p.get_kat() <= 90 and p.get_kat() >= -90): #dopóki się nie przewróciło

            # obliczenie, o ile przesunął się wózek i nadpisanie pozycji
            poz_diff = p.pozycja - poz_last
            px_diff = p.pX - pX_last

            poz_last = p.pozycja
            pX_last = p.pX

            # zapisanie pod X wszystkicj mających wpływ wartości wózka
            X = np.array([poz_diff, p.kat, p.kat1, px_diff, p.pKat, p.pKat1])

            # odjęcie 0.5 od otrzymanego wyjścia sieci:


            force += predict(X, new_c, new_sigma, new_W) - 0.5

            # aktualizacja siły
            p.run(force)

            # dodanie x,y,y2
            x_plot.append(p.get_time())
            y3_plot.append(force)
            y2_plot.append(p.get_position())
            y_plot.append(p.get_kat())

        # wahadło się przewróciło - pobieranie czasu
        new_time = p.get_time()

        # wartości potrzebne do symulowanego wyżarzania - nasza zmienna
        # z zakresu <0,1> oraz to prawdopodobieństwo ze wzoru
        check_propability = np.random.random()

        # obsługa błędu w przypadku przepełnienia metody,
        # to znaczy że wartość jest duża - dajemy infinity
        # dzięki temu na pewno nie zostanie spełniony warunek poboczny
        # symulowanego wyżarzania, bo <0,1> nie jest większe od inf  ##### z internetów
        try:
            case = math.exp(-(new_time - time) / current_temp)
        except OverflowError:
            case = float('inf')

        # warunek przyjęcia przypadku:
        # albo jest lepszy albo prawdopodobieństwo ze wzoru z symulowanego wyżarzania jest
        # mniejsze od naszej losowej liczby
        if new_time > time or check_propability > case:

            # wpisujemy wyniki do last_good_configuration, jeśli jwst w tym
            # momencie najlepszy wynik
            if new_time > time:
                last_good_configuration['time'] = new_time
                last_good_configuration['sigma'] = new_sigma
                last_good_configuration['centers'] = new_c
                last_good_configuration['wages'] = new_W
                last_good_configuration['x_plot'] = x_plot
                last_good_configuration['y_plot'] = y_plot
                last_good_configuration['y2_plot'] = y2_plot
                last_good_configuration['y3_plot'] = y3_plot

            # nadpis nowymi wartościami: czas, wagi, centra, sigmy
            time = new_time
            W = new_W
            sigma = new_sigma
            c = new_c

            print(f'NOWY WYNIK! Czas jazdy wózka: {time}')

        # jeśli nie weszlo w ten warunek, to przechodzimy do następnej lini
        else:
            print()

        # temperatura*mnnożnik
        current_temp *= alpha

    print(f"\nCzas jazdy wózka:\n{last_good_configuration['time']}\n")
    print(f"Wagi sieci:\n{last_good_configuration['wages']}\n")
    print(f"Centra neuronów radialnych:\n{last_good_configuration['centers']}\n")
    print(f"Sigmy neuronów radialnych:\n{last_good_configuration['sigma']}\n")
    print("Wykresy kluczowych wartości zależnych od siły działającej na wózek:\n\n")

    plt.figure(figsize=(20, 10))
    plt.title("Ruch wahadła w czasie (od dołu do góry)")
    plt.plot(last_good_configuration['y_plot'], last_good_configuration['x_plot'])
    plt.figure(figsize=(20, 10))
    plt.title("Ruch wózka w czasie (od dołu do góry)")
    plt.plot(last_good_configuration['y2_plot'], last_good_configuration['x_plot'])
    print()
    plt.figure(figsize=(20, 10))
    plt.title("Siła działająca na wózek w czasie (od dołu do góry)")
    plt.plot(last_good_configuration['y3_plot'], last_good_configuration['x_plot'])

    plt.show()
    print()

#na początku zostanie sprawdzony poniższy warunek okreslajacy funkcje od której mamy zacząć
if __name__ == "__main__":
    main()