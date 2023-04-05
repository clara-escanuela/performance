import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def compute_profile(x, y, nbin=(100,100)):

    '''
    Computes the profile plot between two arrays.
      - First computes the 2d histogram (by numpy).
      - Get the mean and RMS values of each vertical slice of the 2D distribution
    '''

    hist, xe, ye = np.histogram2d(x,y,nbin)  #2d histogram

    xbin_width = xe[1] - xe[0]  #bin width

    #Initialize arrays
    x_array      = []
    x_slice_mean = []
    x_slice_rms  = []

    for i in range(xe.size-1):

        yvals = y[(x > xe[i]) & (x <= xe[i + 1])]

        if yvals.size > 0: # do not fill the quanties for empty slices

            x_array.append(xe[i] + xbin_width/2)
            x_slice_mean.append(yvals.mean())
            x_slice_rms.append(yvals.std())

    x_array = np.array(x_array)
    x_slice_mean = np.array(x_slice_mean)
    x_slice_rms = np.array(x_slice_rms)

    return x_array, x_slice_mean, x_slice_rms
