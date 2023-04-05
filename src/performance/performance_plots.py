import numpy as np
import matplotlib as mpl
from performance.numpyext import *
from performance.profile_plot import *

def cta_requirements(url='/home/nieves/Downloads/reqsstuff/RequirementsStuff/IntensityRes.txt'):
    q_t = np.array([])
    res_q = np.array([])

    with open(url) as f:
        lines = f.readlines()
        lines_sp = [line.split() for line in lines][:-1]
        for i in range(0, len(lines_sp)):
            q_t = np.append(q_t, lines_sp[i][0])
            res_q = np.append(res_q, lines_sp[i][1])

    return q_t, res_q

def log_bins(min_val, max_val, bins):
    return np.unique(np.round(np.logspace(min_val, max_val, bins+1))) - 0.5

def charge_resolution(min_val, max_val, bins, true_charge, reconstructed_charge, requirements=True):
    bins = log_bins(min_val, max_val, bins)
    q_t, res_q = cta_requirements()
    plt.figure(figsize=(10, 8))

    p_x, p_mean, p_rms = compute_profile(true_charge, (reconstructed_charge - true_charge)**2, (bins, bins))

    plt.plot(p_x, np.sqrt(p_mean)/p_x, color='black', linewidth=2)
    if requirements == True:
        plt.plot(q_t.astype(np.float), res_q.astype(np.float), color='black', label='CTA requirement', linewidth=2, linestyle='--')
    plt.yscale('log')
    plt.xscale('log')

    plt.xlabel("True charge / p.e.", fontsize=20)
    plt.ylabel("Charge resolution", fontsize=20)
    plt.legend(fontsize=20)

    plt.show()

def time_resolution(bins, true_charge, true_time, reconstructed_time):
    plt.figure(figsize=(10, 8))

    p_mean, p_std, p_n, p_x_edges = profile(np.log10(true_charge), (true_time - reconstructed_time)**2, bins=bins, sigma_cut=3)
    p_x_edges = 10**p_x_edges
    p_x = p_x_edges[:-1] + np.diff(p_x_edges) / 2

    plt.loglog(p_x, np.sqrt(p_mean), color='black', linewidth=2)
    plt.loglog(np.logspace(0, 3.5), 0.74 / np.sqrt(np.logspace(0, 3.5)), '--k', linewidth=2)

    plt.xlabel("True charge / p.e.", fontsize=20)
    plt.ylabel("Time resolution / ns", fontsize=20)
    plt.show()

def time_snr(bims, true_time, reconstructed_time, snrs):
    plt.figure(figsize=(10, 8))
    p_mean, p_std, p_n, p_x_edges = profile(snrs, (true_time - reconstructed_time)**2, bins=bins, sigma_cut=3)
    p_x = p_x_edges[:-1]

    plt.loglog(p_x, p_mean, color='black', linewidth=2)

    plt.xlabel("SNR", fontsize=20)
    plt.ylabel("Time resolution / ns", fontsize=20)
    plt.show()


