import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)

# Parameter loading


def load_fit_parameters():
    xlsx_url = 'https://github.com/geolabsoft/mecsuelos/blob/main/taylor/taylor_chart_fit.xlsx?raw=true'
    long_term = pd.read_excel(xlsx_url, sheet_name='long_term')
    long_term_inverse =  pd.read_excel(xlsx_url, sheet_name='long_term_inverse')
    short_term = pd.read_excel(xlsx_url, sheet_name='short_term')
    
    return long_term, long_term_inverse, short_term

# Functions for Taylor's Long term Chart


def ns_taylor_long_term(fit_data, beta, phi, decimals=4):
    if phi > fit_data.phi.unique().max() or phi < fit_data.phi.unique().min():
        raise ValueError('Phi value out of the accepted value range')
    else:
        lower_phi = fit_data[fit_data.phi <= phi]
        higher_phi = fit_data[fit_data.phi >= phi]

        inf_phi = lower_phi[lower_phi.phi == lower_phi.phi.max()]
        sup_phi = higher_phi[higher_phi.phi == higher_phi.phi.min()]

        coefs_inf_phi = [inf_phi.coef_5, inf_phi.coef_4, inf_phi.coef_3,
                         inf_phi.coef_2, inf_phi.coef_1, inf_phi.coef_0]

        coefs_sup_phi = [sup_phi.coef_5, sup_phi.coef_4, sup_phi.coef_3,
                         sup_phi.coef_2, sup_phi.coef_1, sup_phi.coef_0]

        inf_ns = np.polyval(coefs_inf_phi, beta)
        sup_ns = np.polyval(coefs_sup_phi, beta)

        xp = [list(inf_phi.phi)[0], list(sup_phi.phi)[0]]
        fp = [inf_ns[0], sup_ns[0]]

        return np.round(np.interp(phi, xp, fp), decimals=decimals)


def beta_taylor_long_term(fit_data, ns, phi, decimals=4):
    if phi > fit_data.phi.unique().max() or phi < fit_data.phi.unique().min():
        raise ValueError('Phi value out of the accepted value range')
    else:
        lower_phi = fit_data[fit_data.phi <= phi]
        higher_phi = fit_data[fit_data.phi >= phi]

        inf_phi = lower_phi[lower_phi.phi == lower_phi.phi.max()]
        sup_phi = higher_phi[higher_phi.phi == higher_phi.phi.min()]

        coefs_inf_phi = [inf_phi.coef_5, inf_phi.coef_4, inf_phi.coef_3,
                         inf_phi.coef_2, inf_phi.coef_1, inf_phi.coef_0]

        coefs_sup_phi = [sup_phi.coef_5, sup_phi.coef_4, sup_phi.coef_3,
                         sup_phi.coef_2, sup_phi.coef_1, sup_phi.coef_0]

        inf_beta = np.polyval(coefs_inf_phi, ns)
        sup_beta = np.polyval(coefs_sup_phi, ns)

        xp = [list(inf_phi.phi)[0], list(sup_phi.phi)[0]]
        fp = [inf_beta[0], sup_beta[0]]

        return np.round(np.interp(phi, xp, fp), decimals=decimals)


def plot_taylor_long_term(fit_data, ax, color='k',
                          legend=False, annotation=False):

    for phi in fit_data.phi.unique():
        record = fit_data[fit_data.phi == phi]

        range_plot = [record['range_min'], record['range_max']]
        coefs = [record['coef_5'], record['coef_4'], record['coef_3'],
                 record['coef_2'], record['coef_1'], record['coef_0']]
        x = np.linspace(range_plot[0], range_plot[1], 100)
        y = np.polyval(coefs, x)
        if legend:
            label = r'$\phi$ = {}'.format(phi)
        else:
            label = ''

        if color:
            ax.plot(x, y, color=color, label=label)
        else:
            ax.plot(x, y, label=label)

        if legend:
            ax.legend(loc='upper left')

        if annotation:
            ax.annotate(r'$\phi = 0\degree$', (82.5, 0.262))
            ax.annotate(r'$5\degree$', (87, 0.244))
            ax.annotate(r'$10\degree$', (85.7, 0.22))
            ax.annotate(r'$15\degree$', (85.7, 0.2))
            ax.annotate(r'$20\degree$', (85.7, 0.18))
            ax.annotate(r'$25\degree$', (85.7, 0.164))

    ax.xaxis.set_minor_locator(MultipleLocator(2))
    ax.yaxis.set_minor_locator(MultipleLocator(0.005))
    ax.grid(which='both', linewidth=0.4)

    ax.set(title=r'Ábaco de Taylor ($\phi\neq0$)',
           xlabel=r'Inclinación del talud , $\beta$ ($\degree$)',
           ylabel=r'Número de estabilidad, $N_s = \frac{c}{\gamma·H·}$',
           xlim=[0, 90],
           ylim=[0, 0.35])

# Functions for Taylor's Short term Chart


def ns_taylor_short_term(fit_data, beta, D, decimals=4):
    coefs = {}
    range_min = {}
    range_max = {}

    if D in fit_data.d.unique():

        for d in fit_data.d.unique():
            record = fit_data[fit_data.d == d]

            coefs[d] = [record['coef_12'].values[0],
                        record['coef_11'].values[0],
                        record['coef_10'].values[0],
                        record['coef_9'].values[0],
                        record['coef_8'].values[0],
                        record['coef_7'].values[0],
                        record['coef_6'].values[0],
                        record['coef_5'].values[0],
                        record['coef_4'].values[0],
                        record['coef_3'].values[0],
                        record['coef_2'].values[0],
                        record['coef_1'].values[0],
                        record['coef_0'].values[0]]

            range_min[d] = record['range_min'].values[0]
            range_max[d] = record['range_max'].values[0]

        if beta >= range_min['any']:
            ns = np.polyval(coefs['any'], beta)
        elif D == 'inf':
            ns = 5.52
        else:
            if (beta > range_min[D]) & (beta < range_max[D]):
                ns = np.polyval(coefs[D], beta)
            elif beta > range_max[D]:
                if D == 4:
                    ns = np.polyval(coefs['inf'], beta)
                else:
                    ns = np.polyval(coefs[1], beta)
            else:
                raise ValueError('Value out of range')
    else:
        raise ValueError('D value not found')

    return np.round(ns, decimals=decimals)


def beta_taylor_short_term(fit_data, ns, D, decimals=4):
    coefs = {}
    range_min = {}
    range_max = {}

    if D in fit_data.d.unique():

        for d in fit_data.d.unique():
            record = fit_data[fit_data.d == d]
            coefs[d] = [record['coef_12'].values[0],
                        record['coef_11'].values[0],
                        record['coef_10'].values[0],
                        record['coef_9'].values[0],
                        record['coef_8'].values[0],
                        record['coef_7'].values[0],
                        record['coef_6'].values[0],
                        record['coef_5'].values[0],
                        record['coef_4'].values[0],
                        record['coef_3'].values[0],
                        record['coef_2'].values[0],
                        record['coef_1'].values[0],
                        record['coef_0'].values[0]]

            range_min[d] = record['range_min'].values[0]
            range_max[d] = record['range_max'].values[0]

        if ns <= 5.52:
            p = np.poly1d(coefs['any'])
            beta = (p - ns).roots[0]
        else:
            p = np.poly1d(coefs[D])
            sol_list = (p - ns).roots
            for sol in sol_list:
                possible_beta = np.real_if_close(sol).item(0)
                if np.isreal(possible_beta):
                    if possible_beta > range_min[D]:
                        if possible_beta < range_max[D]:
                            beta = possible_beta
                            break
            else:
                raise ValueError('Value out of range')
    else:
        raise ValueError('D value not found')

    return np.round(beta, decimals=decimals)


def plot_taylor_short_term(fit_data, ax, color='k', legend=False):

    for d in fit_data.d.unique():
        record = fit_data[fit_data.d == d]

        range_plot = [record['range_min'], record['range_max']]
        coefs = [record['coef_12'].values[0],
                 record['coef_11'].values[0],
                 record['coef_10'].values[0],
                 record['coef_9'].values[0],
                 record['coef_8'].values[0],
                 record['coef_7'].values[0],
                 record['coef_6'].values[0],
                 record['coef_5'].values[0],
                 record['coef_4'].values[0],
                 record['coef_3'].values[0],
                 record['coef_2'].values[0],
                 record['coef_1'].values[0],
                 record['coef_0'].values[0]]

        x = np.linspace(range_plot[0], range_plot[1], 100)

        y = np.polyval(coefs, x)
        delta_ns = (y[-1, 0] - record['ns_init'].values[0])
        y = y - delta_ns

        if legend:
            if d == 'inf':
                label = r'D = $\infty$'
            elif d == 'any':
                label = 'Cualquier D'
            else:
                label = 'D = {}'.format(d)
        else:
            label = ''

        if color:
            ax.plot(x, y, color=color, label=label)
        else:
            ax.plot(x, y, label=label)

        if legend:
            ax.legend(loc='upper left')

    ax.xaxis.set_minor_locator(MultipleLocator(10))
    ax.yaxis.set_minor_locator(MultipleLocator(2))
    ax.grid(which='both', linewidth=0.4)

    ax.set(title=r'Ábaco de Taylor ($\phi\neq0$)',
           xlabel=r'Inclinación del talud , $\beta$ ($\degree$)',
           ylabel=r'Número de estabilidad, $N_s = \frac{\gamma·H}{c}$',
           xlim=[90, 0],
           ylim=[3, 11])

    ax.xaxis.set_minor_locator(MultipleLocator(10))
    ax.yaxis.set_minor_locator(MultipleLocator(2))
    ax.grid(which='both', linewidth=0.4)
