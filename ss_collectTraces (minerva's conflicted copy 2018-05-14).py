#!/usr/bin/env python
__author__ = 'toopazo'

import argparse
import os
from obspy.core import read
from obspy.core import Trace, Stream
# from obspy.core import Trace, Stream, UTCDateTime
# import numpy as np
# import dateutil.parser
# from datetime import datetime, timedelta


def collect_traces(infile1,
                   infile2,
                   infile3,
                   outfile):

    # 1) Make sure user inputs are correct (Convert to real -no symlink- and full path)
    file = infile1
    file = os.path.normcase(file)
    file = os.path.normpath(file)
    file = os.path.realpath(file)
    infile1 = file
    print(infile1)

    file = infile2
    file = os.path.normcase(file)
    file = os.path.normpath(file)
    file = os.path.realpath(file)
    infile2 = file
    print(infile2)

    file = infile3
    file = os.path.normcase(file)
    file = os.path.normpath(file)
    file = os.path.realpath(file)
    infile3 = file
    print(infile3)

    # 2) Get traces
    st = read(infile1)
    tr1 = st[0]
    st = read(infile2)
    tr2 = st[0]
    st = read(infile3)
    tr3 = st[0]

    # 3) Collect traces
    st = Stream([tr1, tr2, tr3])

    # >> Write to disk
    # print(tuple_header_starttime)
    outfile_name = outfile
    st.write(outfile_name, format='MSEED', encoding=11, reclen=256, byteorder='>')
    # st.write(outfile_name, format='MSEED', encoding=0, reclen=256)
    st = read(outfile_name)
    arg = "[tuple2mseed] MSEED created: %s" % st[0]
    print(arg)
    # print(st1[0])
    # print(st1[0].stats)
    # print(st1[0].data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot given file(s) (obspy wrapper)')
    parser.add_argument('--infile1', action='store', help='files to process', required=True)
    parser.add_argument('--infile2', action='store', help='files to process', required=True)
    parser.add_argument('--infile3', action='store', help='files to process', required=True)
    parser.add_argument('--outfile', action='store', help='files to process', required=True)
    # parser.add_argument('--ch1', action='store', help='channel signal', required=True)
    # parser.add_argument('--ch2', action='store', help='channel signal', required=True)
    # parser.add_argument('--ch3', action='store', help='channel signal', required=True)
    # parser.add_argument('--ch4', action='store', help='channel signal', required=True)
    args = parser.parse_args()

    collect_traces(infile1=args.infile1,
                   infile2=args.infile3,
                   infile3=args.infile3,
                   outfile=args.outfile)
