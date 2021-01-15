import math

def uzt(Tv,Zr):
    # Configuration
    n = 1000 #number of iterations
    Uzt = 1 # initial value of Uzt

    for m in range(n):
        M = (math.pi/2) * (2 * m + 1)
        t = (pow(-1,m) * 2 / M) * (math.cos(M * Zr)) * (math.exp(-(Tv * pow(M,2))))
        Uzt = Uzt - t

    return Uzt

def tvt(Zr,Uz):
    # Configuración
    tol = 0.00000001 #Tolerancia con el resultado
    maxCiclos = 1000 #Número máximo de ciclos permitidos

    # Valores iniciales de Tv
    TV0 = 0.001
    TV1 = 15
    TVi = (TV0 + TV1) / 2

    i = 0 # Inicializa el contador de ciclos en 0
    while True:
        i = i + 1
        UZi = uzt(TVi, Zr)

        if abs(UZi - Uz) / Uz < tol:
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

    return TVi

def zrt(Tv,Uz):
    # Configuración
    tol = 0.00000001 #Tolerancia con el resultado
    maxCiclos = 1000 #Número máximo de ciclos permitidos

    # Valores iniciales de Zr
    ZR0 = 0
    ZR1 = 1
    ZRi = (ZR0 + ZR1) / 2

    i = 0  # Inicializa el contador de ciclos en 0
    while True:
        i = i + 1
        UZi = uzt(Tv, ZRi)

        if abs(UZi - Uz) / Uz < tol:
            break
        elif i > maxCiclos:
            ZRi = -1
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

    return ZRi