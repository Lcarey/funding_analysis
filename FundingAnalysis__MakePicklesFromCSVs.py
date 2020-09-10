#!/usr/bin/env python3
# create a pickle file from each .csv

import os, multiprocessing
from funding_analysis import *


# load csv files
csv_files = [f for f in os.listdir() if (f.endswith('.csv') and f.find('_PRJABS_')>-1) ]
csv_files = [(d,s) for d in range(4000) for s in csv_files if s.endswith('FY'+str(d)+'.csv') ]
pprint(csv_files)

## create a pickle file from each .csv
if __name__ == '__main__':
  for I,f in enumerate(csv_files):
    p = multiprocessing.Process(target=ProcessesWordsInAbstractFile, args=(f[1],f[0]))
    p.start()