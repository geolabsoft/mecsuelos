import matplotlib.pyplot as plt
import numpy as np


def crea_tv(p = 100):
    tv_1 = np.linspace(0.001,0.01,p)
    tv_2 = np.delete(np.linspace(0.01,0.1,p),0)
    tv_3 = np.delete(np.linspace(0.1,1,p),0)
    tv_4 = np.delete(np.linspace(1,10,p),0)
    return np.concatenate((tv_1, tv_2, tv_3, tv_4))


def u(n=50,p=100):
   
    tv_list = crea_tv(p)

    u_list = []
    
    for Tv in tv_list:
        U = 1
        for m in range(n):
            M = (np.pi / 2) * (2 * m + 1)
            U = U - ((2 / M**2) * np.exp(-M**2 * Tv))
        u_list.append(U)

    return tv_list, u_list


def u_menor_60(p = 100):
    tv_list = crea_tv(p)
    u_list = np.sqrt(4 * tv_list / np.pi)
    return tv_list, u_list


def u_mayor_60(p = 100):
    tv_list = crea_tv(p)
    u_list = 1 - 0.8106 * np.exp(-2.4674 * tv_list)
    return tv_list, u_list


def crea_puntos(n=50, p=100):
    puntos = {'teorica': u(n, p),
              'menor_60': u_menor_60(p=p),
              'mayor_60': u_mayor_60(p=p)}
    return puntos

def c_conso(puntos = {}, teorica = False, menor_60 = False, mayor_60 = False, escala_logaritmica = True):

    out2 = plt.figure()

    puntos_teorica = puntos['teorica']
    puntos_menor_60 = puntos['menor_60']
    puntos_mayor_60= puntos['mayor_60']

    # Curva aproximada U < 0.6
    if menor_60:
        plt.plot(puntos_menor_60[0], puntos_menor_60[1], 'r', label='Aproximación U < 60%')

    # Curva aproximada U > 0.6
    if mayor_60:
        plt.plot(puntos_mayor_60[0],puntos_mayor_60[1], 'y', label='Aproximación U > 60%')

    # Curva teórica
    if teorica:
        plt.plot(puntos_teorica[0],puntos_teorica[1], 'b', label='Teórica')

    # Configuración gráfica
    plt.xlabel("Factor tiempo, Tv")
    plt.ylabel("Grado de consolidación medio, U")

    if escala_logaritmica:
        plt.title("\nCurva de consolidación (Escala semi-logaritmica)\n")
        plt.xscale("log")
    else:
        plt.title("\nCurva de consolidación (Escala lineal)\n")
        plt.xscale("linear")

    plt.ylim(1,0)
    plt.xlim(0.001,10)
    plt.grid(True)

    if teorica or menor_60 or mayor_60:
        plt.legend()