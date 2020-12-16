#!/usr/bin/env python 

import sys
import pandas as pd
from scipy.stats.mstats import gmean

df = pd.read_csv(sys.stdin, names=["App", "Kernel", "ExecTime"])

df = df.pivot(index='App', columns='Kernel', values="ExecTime")
try:
    df['impr w/ PTEMagnet, %'] = (1 - df['modified'] / df['clean'] ) * 100
except KeyError:
    print "Somthing went wrong. Most likely you don't have any results for the modified version of the kernel,\n\
            so this script does not know how to compute the difference. Get some results for the modified kerneland rerun me."
    exit(1)

df['impr w/ PTEMagnet, %'] = df['impr w/ PTEMagnet, %'].round(decimals=1)
df['clean'] = df['clean'].round(decimals=0)
df['modified'] = df['modified'].round(decimals=0)

print(df)
try:
    geo_impr = ( gmean((df['impr w/ PTEMagnet, %'] / 100 + 1).squeeze()) - 1 ) * 100
    print('Geomean performance imporvement delivered by PTEMagnet is ' + "{0:.1f}".format(geo_impr) + '%')
except IndexError:
    pass
