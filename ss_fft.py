#!/usr/bin/env python
__author__ = 'toopazo'

import argparse
import os
from obspy.core import read
#from obspy.core import UTCDateTime
import numpy as np
import matplotlib.pyplot as plt
import copy


def do_rfft(infile, outfile, nbits):
    # 1) Make sure user inputs are correct
    infile = os.path.normcase(infile)
    infile = os.path.normpath(infile)
    infile = os.path.realpath(infile)
    print(infile)
    nbits = int(nbits)
    print(nbits)

    # 2) Construct Stream object
    st = read(infile)
    # for i in range(1, len(infile)):
    #     st += read(infile)
    # st = st.sort()
    print(st[0].stats)
    print(st[0].data)

    # 3) Calculate FFT
    dataonly = map(float, st[0].data)
    samp_rate = st[0].stats.sampling_rate
    # ######################################################
    # # Tests for a perfect sine wave
    # ######################################################
    # import math
    # Fs = 100.0      # sampling rate
    # Ts = 1.0/Fs     # sampling interval
    # t_time = np.arange(0, 1, Ts)     # time vector
    # ff = 5     # frequency of the signal [Hz]
    # y_signal = (2**23)*np.sin(2*np.pi*ff*t_time)
    # arg = "len(y_signal) = %s | y_signal = %s" % (len(y_signal), y_signal)
    # print(arg)
    # dataonly = y_signal
    # samp_rate = Fs
    # # plt.plot(t_time, dataonly, marker='o', markersize=4)
    # # plt.show()
    # # plt.clf()
    # ######################################################
    # # Tests for a perfect sine wave
    # ######################################################
    spec = np.fft.rfft(dataonly)
    freq = np.fft.rfftfreq(len(dataonly), d=1.0/samp_rate)
    arg = "[do_rfft] ******************************************"
    print(arg)
    print('[do_rfft] samp_rate %s' % samp_rate)
    print('[do_rfft] spec %s' % spec)
    print('[do_rfft] freq %s' % freq)
    print('[do_rfft] spec.size %s' % spec.size)
    print('[do_rfft] freq.size %s' % freq.size)

    # 4) Generate Normalized Fourier Transform in dBFS scale
    arg = "[do_rfft] ******************************************"
    print(arg)
    norm_abs_rfft = 2.0*abs(spec)/len(dataonly)
    norm_abs_rfft_dbfs = copy.copy(norm_abs_rfft)
    for i in range(0, len(norm_abs_rfft)):
        ratio = (1.0*norm_abs_rfft[i])/(2.0**(nbits-1))
        # if ratio < 1.0:
        #     arg = 'ratio = %s = %s/%s' % (ratio, norm_abs_rfft[i], (2.0**(nbits-1)))
        #     print(arg)
        # ratio = (1.0*norm_abs_rfft[i])
        norm_abs_rfft_dbfs[i] = 20.0*np.log10(ratio)
    arg = '[do_rfft] norm_abs_rfft_dbfs (%s-bit ADC is assumed) %s' % (norm_abs_rfft_dbfs, nbits)
    print(arg)

    # 5) Plot
    arg = "[do_rfft] ******************************************"
    print(arg)
    # plt.plot(freq, norm_abs_rfft, marker='o', markersize=4, color='blue')
    # plt.plot(freq, norm_abs_rfft, marker='o', markersize=4, color='blue')
    # plt.plot(freq, norm_abs_rfft_dbfs, marker='o', linestyle="-", markersize=4)
    y_axis = norm_abs_rfft_dbfs
    x_axis = freq
    plt.plot(x_axis, y_axis, marker='o', markersize=4, color='blue')
    plt.title('FFT')
    plt.xlabel('Freq (Hz)')
    plt.ylabel('Normalized |Y(f)| relative to Full Scale [dBFS]')
    # Extra info (max Freq, dBFS,  etc)
    # y_axis = norm_abs_rfft_dbfs
    y_axis_argmax = y_axis.argmax()
    y_axis_max = y_axis.max()
    print('[do_rfft] y_axis_argmax = %s' % y_axis_argmax)
    print('[do_rfft] y_axis[%s] = %s' % (y_axis_argmax, y_axis[y_axis_argmax]))
    print('[do_rfft] y_axis_max() = %s' % y_axis_max)
    arg_freqinfo = ' %s [Hz]\n %s [dBFS]' % (x_axis[y_axis_argmax], y_axis_max)
    print('[do_rfft] arg_freqinfo %s' % arg_freqinfo)
    plt.annotate(arg_freqinfo, xy=(x_axis[y_axis_argmax]+1, y_axis_max),
                 xytext=(x_axis[y_axis_argmax]+4, y_axis_max-10),
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 )

    # 6) Save or show
    if outfile is not None:
        outfile = str(outfile)
        # outfile_plot_name += '.png'
        arg = "[do_rfft] saving file %s .." % outfile
        print(arg)
        plt.savefig(outfile)
    else:
        plt.show()

    # 7) return arrays
    return freq, norm_abs_rfft_dbfs, norm_abs_rfft


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot given file(s) (obspy wrapper)')
    parser.add_argument('--infile', action='store', help='files to process', required=True)
    #parser.add_argument('file', type=argparse.FileType('r'), nargs='+')
    parser.add_argument('--outfile', action='store', help='name of output file')
    parser.add_argument('--nbits', action='store', help='number of bits, to covnert dB to dBFS', required=True)
    # parser.add_argument('--day_plot', action='store_true', help='day plot of the given file(s), normally same channel')
    args = parser.parse_args()

    do_rfft(args.infile, args.outfile, args.nbits)