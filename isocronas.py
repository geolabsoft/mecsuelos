import math
import matplotlib.pyplot as plt
import numpy as np


def uzt(Tv, Zr):
    # Configuration
    n = 1000  # number of iterations
    Uzt = 1  # initial value of Uzt

    for m in range(n):
        M = (math.pi / 2) * (2 * m + 1)
        t = (pow(-1, m) * 2 / M) * (math.cos(M * Zr)) * (math.exp(-(Tv * pow(M, 2))))
        Uzt = Uzt - t

    return round(Uzt, 5)


def tvt(Zr, Uz):
    # Configuración
    tol = 0.00000001  # Tolerancia con el resultado
    maxCiclos = 1000  # Número máximo de ciclos permitidos

    # Valores iniciales de Tv
    TV0 = 0.001
    TV1 = 15
    TVi = (TV0 + TV1) / 2

    i = 0  # Inicializa el contador de ciclos en 0
    while True:
        i = i + 1
        UZi = uzt(TVi, Zr)

        if abs(UZi - Uz) < tol:
            break
        elif i > maxCiclos:
            TVi = -1
            break
        elif Uz >= UZi:
            TV0 = TVi
            TVi = (TVi + TV1) / 2
        elif Uz < UZi:
            TV1 = TVi
            TVi = (TV0 + TVi) / 2
        else:
            TVi = -1
            break

    return round(TVi, 5)


def zrt(Tv, Uz):
    # Configuración
    tol = 0.00000001  # Tolerancia con el resultado
    maxCiclos = 1000  # Número máximo de ciclos permitidos

    # Valores iniciales de Zr
    ZR0 = 0
    ZR1 = 1
    ZRi = (ZR0 + ZR1) / 2

    i = 0  # Inicializa el contador de ciclos en 0
    while True:
        i = i + 1
        UZi = uzt(Tv, ZRi)

        if abs(UZi - Uz) < tol:
            break
        elif i > maxCiclos:
            ZRi = -1
            break
        elif ZRi < 0.000001:
            ZRi = 0
            break
        elif Uz >= UZi:
            ZR0 = ZRi
            ZRi = (ZRi + ZR1) / 2
        elif Uz < UZi:
            ZR1 = ZRi
            ZRi = (ZR0 + ZRi) / 2
        else:
            ZRi = -1
            break

    return round(ZRi, 5)


def uz_int(iso_std = [], Tv = 0.5, Zr = 0, grafica=True):
    """ Función para el uso de interact para el cálculo interactivo de grado de
    consolidación. Además de obtener el grado de consolidación, dibuja las
    isocronas estandar y la correspondiente a los valores de Tv y Zr que se
    proporcionan como parámetros.
    La variable [grafica] permite seleccionar si se obtiene o no la gráfica."""

    # Obtiene el grado de consolidación usando isocronas.py
    Uz = uzt(Tv, Zr)

    isoSTD = iso_std[0]
    zrVTot = iso_std[1]
    zrV = iso_std[2]

    if grafica:
        # Crea una nueva figura
        out = plt.figure()

        # Dibuja las isocronas estandar
        for uzVTot in isoSTD:
            plt.plot(uzVTot, zrVTot, 'grey', linewidth=0.5)

        # Dibuja la isocrona correspondiente al Tv proporcionado
        uzV = []
        for i in zrV:
            uzV.append(uzt(Tv, i))

        uzVTot = np.concatenate((np.flip(uzV), np.delete(uzV, 0)))
        plt.plot(uzVTot, zrVTot, 'b')
  
        # Dibuja el punto que se está calculando
        plt.plot(Uz, Zr, 'ro')
        plt.plot([0, Uz], [Zr, Zr], 'r--', linewidth=0.75)
        plt.plot([Uz, Uz], [-1, Zr], 'r--', linewidth=0.75)

        # Configura la apariencia del gráfico
        plt.title("Isocronas\nTv = " + str(round(Tv, 5)) + " / Zr = " + 
              str(round(Zr, 5)) + " -> Uz = " + str(round(Uz, 5)))
        plt.xlim(0, 1)
        plt.ylim(-1, 1)
        plt.xlabel("Uz")
        plt.ylabel("Zr")
        plt.grid(True)

        print("------------------------------------------------")
        print("               Resultado gráfico")
        print("------------------------------------------------")
    
        # Muestra la gráfica
        plt.show()

    print("-----------------------------------------------")
    print("              Resultado numérico")
    print("-----------------------------------------------")
    print("")
    print("Tv = " + str(round(Tv, 5)) + " / Zr = " + 
              str(round(Zr, 5)) + " -> Uz = " + str(round(Uz, 5)))


def calcula_isocronas_standard():
    tvV = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1]
    zrV = np.linspace(0, 1, 50)
    zrVTot = np.concatenate((0 - np.flip(zrV), np.delete(zrV, 0)))
    isoSTD = []
    for j in tvV:
        uzV = []
        for i in zrV:
            uzV.append(uzt(j, i))
        uzVTot = np.concatenate((np.flip(uzV), np.delete(uzV, 0)))
        isoSTD.append(uzVTot)

    iso_std = [isoSTD, zrVTot, zrV] 

    return iso_std

