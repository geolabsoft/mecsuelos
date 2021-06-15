import numpy as np


# Coeficiente de empuje en reposo (K0)
# Jaky
def k0_nc_jaky(phi, *, degree=True):
    if degree:
        phi = np.radians(phi)
    return 1 - np.sin(phi)


# Massarch
def k0_nc_massarch(ip, *, percent=False):
    if percent:
        ip = ip / 100
    return 0.44 + 0.42*ip


# Schmidt
def k0_sc_schmidt(k0_nc, rsc, *, alpha=0.41):
    return k0_nc * rsc**alpha


# Teoría de Rankine
def rankine_ep_no_c(phi, *, alpha=0, theta=0, degree=True):
    if degree:
        phi = np.radians(phi)
        alpha = np.radians(alpha)
        theta = np.radians(theta)
    # Auxiliar
    psi_a = np.arcsin(np.sin(alpha) / np.sin(phi)) - alpha + 2 * theta
    beta = np.arctan(np.sin(phi) * np.sin(psi_a) / (1 - np.sin(phi) * np.sin(psi_a)))
    eta = np.pi / 4 + phi / 2 + alpha / 2 - 0.5 * np.arcsin(np.sin(alpha) / np.sin(phi))
    # Active
    ka = np.cos(alpha - theta)
    ka = ka * np.sqrt(1 + np.sin(phi)**2 - 2 * np.sin(phi) * np.cos(psi_a))
    ka = ka / np.cos(theta)**2
    ka = ka / (np.cos(alpha) + np.sqrt(np.sin(phi)**2 - np.sin(alpha)**2))
    # Passive
    kp = np.cos(alpha) + np.sqrt(np.cos(alpha)**2 - np.cos(phi)**2)
    kp = kp * np.cos(alpha)
    kp = kp / np.sqrt(np.cos(alpha) - np.sqrt(np.cos(alpha)**2 - np.cos(phi)**2))
    return ka, kp, beta, eta


# Teoría de Coulomb (c = 0)
def coulomb_ep_no_c(phi, delta, *, beta=90, alpha=0, degree=True):
    if degree:
        phi = np.radians(phi)
        delta = np.radians(delta)
        beta = np.radians(beta)
        alpha = np.radians(alpha)
    # Active
    ka = np.sin(beta + phi)**2
    ka /= np.sin(beta)**2
    ka /= np.sin(beta - delta)
    aux1 = np.sin(phi + delta) * np.sin(phi - alpha)
    aux2 = np.sin(beta - delta) * np.sin(alpha + beta)
    ka /= (1 + np.sqrt(aux1 / aux2))**2
    # Passive
    kp = np.sin(beta - phi)**2
    kp /= np.sin(beta)**2
    kp /= np.sin(beta + delta)
    aux1 = np.sin(phi + delta) * np.sin(phi + alpha)
    aux2 = np.sin(beta + delta) * np.sin(alpha + beta)
    kp /= (1 - np.sqrt(aux1 / aux2))**2

    return ka, kp
