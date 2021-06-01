import math

def IqRec(m, n):
    if m**2 * n**2 >= m**2 + n**2 + 1:
        Iq = 1 / (4 * math.pi) * (((2 * m * n * math.sqrt(m**2 + n**2 + 1)) / (m**2 + n**2 + m**2 * n**2 + 1)) *
            ((m**2 + n**2 + 2) / (m**2 + n**2 + 1)) + math.atan((2 * m * n * math.sqrt(m**2 + n**2 + 1) / (
            m**2 + n**2 - m**2 * n**2 + 1))) + math.pi)
    else:
        Iq 1 / (4 * math.pi) * (((2 * m * n * math.sqrt(m**2 + n**2 + 1)) / (m**2 + n**2 + m**2 * n**2 + 1)) * ((
            m**2 + n**2 + 2) / (m**2 + n**2 + 1)) + math.atan((2 * m * n * math.sqrt(m**2 + n**2 + 1) / (m**2 + n**2 -
            m**2 * n**2 + 1))))
    return round(Iq, 4

def inc_sigma_puntual(Q, z, R):
    return (Q * 3 * z**3) / (2 * math.pi * R**5)

def inc_sigma_lineal(Q, z, x):
    b = math.sqrt(x**2 + z**2)
    return (2 * Q * z**3) / (math.pi * b**4)

def inc_sigma_faja_uniforme(q, alpha, beta, radianes=False):
    if not radianes:
        alpha = math.radians(alpha)
        beta = math.radians(beta)
    return (q * (alpha + math.sin(alpha) * math.cos(alpha + 2 * beta))) / math.pi

def inc_sigma_faja_triangular(q, B, x, z):
    beta = math.atan((x-B) / z)
    alpha = math.atan(x/z) - beta
    return (q / math.pi) * ((x/B)*alpha - 0.5 * math.sin(2 * beta))

def inc_sigma_circular_uniforme_centro(q, z, a):
    alpha = math.atan(a / z)
    return q * (1 - (1 / ((a/z)**2 + 1)**(3/2)))
