#!/usr/bin/env python
__author__ = 'toopazo'

import argparse
import os
from obspy.core import read
# from obspy.core import UTCDateTime
from obspy.signal.trigger import ar_pick
# from obspy.signal.trigger import pkBaer
from obspy.core import UTCDateTime
from obspy.signal.trigger import classic_sta_lta
from obspy.signal.trigger import plot_trigger

parser = argparse.ArgumentParser(description='Plot given file(s) (obspy wrapper)')
parser.add_argument('--infile', action='store', help='files to process', nargs='+', required=True)
# parser.add_argument('file', type=argparse.FileType('r'), nargs='+')
parser.add_argument('--outfile', action='store', help='name of output file', required=True)
# parser.add_argument('--dayplot', action='store_true', help='dayplot of the given file(s), normally same channel')
args = parser.parse_args()

# 1) Make sure user inputs are correct
outfile_plot = args.outfile
# dayplot = args.dayplot
# Convert to real (no symlink) and full path
infile_paths = args.infile
for i in range(0, len(infile_paths)):
    infile_paths[i] = os.path.normcase(infile_paths[i])
    infile_paths[i] = os.path.normpath(infile_paths[i])
    infile_paths[i] = os.path.realpath(infile_paths[i])
    print(infile_paths[i])

# 2) Construct Stream object
st = read(infile_paths[0])
for i in range(1, len(infile_paths)):
    st += read(infile_paths[i])
st = st.sort()

# 3) Get ZNE components
# print(st_starttime)
# st_starttime = UTCDateTime(st_starttime)
# #print(st_starttime)
# #st.filter("lowpass", freq=7, corners=10)   # , zerophase=True
tr1 = st[0]
tr2 = st[1]
tr3 = st[2]
# print(tr1.stats)
df = tr1.stats.sampling_rate
st_starttime = tr1.stats['starttime']
st_endtime = tr1.stats['endtime']

nlta = int(100 * df)
nsta = int(1 * df)
sta_lta_trigger = 80.0
sta_lta_detrigger = 0.2
cft = classic_sta_lta(tr1.data, nsta, nlta)
print(cft)
print(len(cft))
print(len(tr1.data))
plot_trigger(tr1, cft, sta_lta_trigger, sta_lta_detrigger)

# time that have a trigger > sta_lta_trigger
st_starttime_arr = []
for i in range(0, len(cft)):
    val = cft[i]
    if val >= sta_lta_trigger:
        sismo_st = st_starttime + (i / df)
        # print(sismo_st)
        st_starttime_arr.append(sismo_st)
        # UTCDateTime(str(tuple_header_starttime))
# print(st_starttime_arr)

# filtered times
st_starttime_arr2 = []
starttime_i_prev = st_starttime_arr[0]
for i in range(1, len(st_starttime_arr)):
    starttime_i = st_starttime_arr[i]
    diff = (starttime_i - starttime_i_prev)
    if diff >= 2.0:
        st_starttime_arr2.append(starttime_i_prev)
        starttime_i_prev = starttime_i

print(len(st_starttime_arr2))
print(st_starttime_arr2)

outfile_plot += ".txt"
fd = open(outfile_plot, "w")
for i in range(0, len(st_starttime_arr2)):
    st_i_starttime = st_starttime_arr2[i] - 30.0
    st_i_endtime = st_starttime_arr2[i] + 60.0

    if st_i_starttime < st_starttime:
        st_i_starttime = st_starttime
    if st_i_endtime > st_endtime:
        st_i_endtime = st_endtime
    st_i = st.slice(starttime=st_i_starttime, endtime=st_i_endtime)
    # st_i.plot(type='normal', method='full')

    try:
        tr1 = st_i[0]
        tr2 = st_i[1]
        tr3 = st_i[2]
    except IndexError:
        fd.close()
        exit(1)

    # p_pick, phase_info = pkBaer(tr1.data, df, 20, 60, 7.0, 12.0, 100, 100)
    # print(p_pick)
    # print(phase_info)
    # print(p_pick/df)
    # print(st_starttime + (p_pick/df))
    # st = st.slice(starttime=st_starttime, endtime=(st_starttime+15*60))

    try:
        p_pick, s_pick = ar_pick(tr1.data, tr2.data, tr3.data, df, 1.0, 20.0, 1.0, 0.1, 4.0, 1.0, 2, 8, 0.1, 0.2)
    except IndexError:
        fd.close()
        exit(1)

    # write results
    print(p_pick)
    print(s_pick)
    p_pick = st_i_starttime + p_pick
    s_pick = st_i_starttime + s_pick
    print(p_pick)
    print(s_pick)

    # st.plot(type='relative')
    # st.plot()
    line = "%s\t%s \n" % (p_pick, s_pick)
    print(line)
    fd.write(line)

    st_i.plot(type='normal', method='full')

fd.close()
