import numpy as np
import math

### PERCEPTORN


#NEURON SIGMOIDALNY
def neuron(x):
    wynik = 1/ (1 + (math.exp(-x)))
    return wynik

def licz_warstwe(dane_uczace,wagi,numer_warstwy):
    neurony = []
    for i in range(0, len(wagi[numer_warstwy][0])):
        suma = 0
        for j in range(0, len(wagi[numer_warstwy])):
            suma += dane_uczace[j] * wagi[numer_warstwy][j][i]
        suma = suma/len(wagi[numer_warstwy])
        neurony.append(neuron(suma) * 100)
    return neurony

### DZIAŁANIE SIECI

def siec(wagi, dane_uczace):
    pierwsze_neurony = licz_warstwe(dane_uczace,wagi,0)
    drugie_neurony = licz_warstwe(pierwsze_neurony,wagi,1)
    trzecie = licz_warstwe(drugie_neurony,wagi,2)
    czwarta = licz_warstwe(trzecie,wagi,3)
    return np.array(czwarta)


###WAGI PIERWSZEJ SIECI

wagi_pierwszej_s = [[[-0.6584203 ,  0.51510294, -0.41158092,  0.81260879],
       [ 0.0961155 , -0.88341077,  0.22053467,  0.86760872],
       [-0.12967938, -0.27932844, -0.35072941, -0.78584586],
       [-0.41321434, -0.57713515, -0.86401195, -0.55399575],
       [ 0.30814128, -0.05482043,  0.93765542,  0.59528903],
       [ 0.01800419, -0.38993047, -0.53473559, -0.33609787],
       [ 0.73649188, -0.15823368,  0.05798465,  0.01500593]],

                   [[0.13571697, -0.23964386, -0.56618296],
                    [-0.41065666, 0.1352888, 0.65982125],
                    [-0.19275992, -0.66688615, 0.52308393],
                    [-0.08118317, -0.99694336, -0.0251532]],

                   [[-0.11412576, -0.95733596],
                    [-0.57918131, 0.74578681],
                    [0.53998712, 0.83151569]],

                   [[-0.90177725, -0.22102975, -0.3105531],
                    [-0.53276113, 0.06192515, 0.30449704]]]

### WAGI DRUGIEJ SIECI

wagi_drugiej_s = [[[ 0.05074009,  0.83219618,  0.60828107, -0.97041873],
       [ 0.59134228,  0.52686539, -0.66677692, -0.90525955],
       [ 0.56246156, -0.87935867, -0.27584406,  0.23584057],
       [ 0.49799057, -0.25493165, -0.44741044, -0.05006975],
       [-0.229593  , -0.75135937,  0.54469815, -0.47014396],
       [-0.36292478,  0.21316507,  0.41823127, -0.40689291],
       [-0.19649515,  0.20141992,  0.04888245, -0.75196476]],

                   [[-0.33876152, 0.78188531, 0.09325856],
                    [0.34889439, 0.25215251, 0.2759953],
                    [-0.39140942, -0.94582877, 0.72611437],
                    [0.44441256, 0.90702015, -0.33371427]],

                   [[0.17208397, -0.37474193],
                    [-0.36729274, -0.18136256],
                    [-0.70649718, 0.0129038]],

                   [[-0.84545079, -0.47108025, -0.27752269],
                    [-0.60873828, -0.02172267, -0.27712745]]]


centrum_pierwszej_s = [251.99180327868854, 84.35409836065574, 122.37704918032787, 202.19180327868852, 8.788524590163934, 831.927868852459, 771.2196721311476]
centrum_drugiej_s = [180.76551724137934, 58.706896551724135, 165.09310344827585, 189.51034482758624, 8.389655172413793, 987.7103448275863, 706.051724137931]

def k_srednich(centrum_pierwszej_s, centrum_drugiej_s, wejscie):
    roznica_1 = 0
    roznica_2 = 0
    for i in range(0, len(wejscie)):
        roznica_1 = roznica_1 + abs(wejscie[i] - centrum_pierwszej_s[i])
        roznica_2 = roznica_2 + abs(wejscie[i] - centrum_drugiej_s[i])
    if roznica_1 > roznica_2:
        return 2
    else:
        return 1


def nauczona_siec(wagi_pierwszej_s, wagi_drugiej_s, wejscie, centrum_pierwszej_s, centrum_drugiej_s):

    if k_srednich(centrum_pierwszej_s, centrum_drugiej_s, wejscie) == 1:
        wynik = siec(wagi_pierwszej_s, wejscie)
    else:
        wynik = siec(wagi_drugiej_s, wejscie)
    return wynik

k_s = k_srednich(centrum_pierwszej_s, centrum_drugiej_s, [273,82,105,210,9,904,680])
wy_os = nauczona_siec(wagi_pierwszej_s, wagi_drugiej_s, [273,82,105,210,9,904,680], centrum_pierwszej_s, centrum_drugiej_s)
print("wynik ostateczny = " + str(wy_os) + " wynik należy do centrum " + str(k_s))