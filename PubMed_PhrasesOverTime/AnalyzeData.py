#%% load data 
import pubmed_parser as pp
import pandas as pd
import os, glob
import matplotlib.pyplot as plt
from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from shutil import rmtree
import concurrent.futures
import logging
import numpy as np


working_dir = '/Users/lcarey/Downloads/Pubmed/'
pickle_output_filename = 'df.pickle'
os.chdir(working_dir)
xml_file_list = glob.glob( working_dir + '*xml.gz') 

# %%  load all processed files into a single df
##  save as a pickled DF
## using concat is faster, but uses too much RAM
# xml_file_list = glob.glob( working_dir + '*xml.gz.pickle.xz')
# print(len(xml_file_list))
# df_list = list()
# for i,filename in enumerate(xml_file_list):
#    print(i,end=' ')
#    df_list.append(pd.read_pickle(filename))
# df = pd.concat(df_list,ignore_index=True)
# del(df_list)
#print('\ndone')
#df.to_pickle('all_files_one_df.pickle.xz',compression='xz')

# %%  load all processed files into a list
#  will search on this list of dataframes
xml_file_list = glob.glob( working_dir + '*xml.gz.pickle.xz')
print(len(xml_file_list))
df_list = list()
for i,filename in enumerate(xml_file_list):
   print(i,end=' ')
   df_list.append(pd.read_pickle(filename))
print('\ndone')
#df.to_pickle('all_files_one_df.pickle.xz',compression='xz')
# %% Summary statistics, count occurances of the string
string_to_find = 'little is known'
sums_df_list = list()
counts_df_list = list()
for i,df in enumerate(df_list):
    print(i,end=' ')
    df['contains'] = df.abstract.str.find(string_to_find)
    df['contains'][df['contains']>-1] = 1
    df['contains'][df['contains']==-1] = 0
    sums_df_list.append(df.groupby('year')['contains'].sum())
    counts_df_list.append(df.groupby('year')['contains'].count())


#%%

# %% Sum all DFs in sums_df_list & counts_df_list
# https://stackoverflow.com/questions/42209838/treat-nan-as-zero-in-numpy-array-summation-except-for-nan-in-all-arrays/42210898
# https://stackoverflow.com/questions/49056567/how-to-sum-with-missing-values-in-pandas

all_years_counts = np.sum(counts_df_list+sums_df_list)
all_years_sums   = np.sum(counts_df_list+sums_df_list)
all_years_counts[all_years_counts.isna()]=0
all_years_sums[all_years_sums.isna()]=0
all_years_counts = all_years_counts.astype(int)
all_years_sums = all_years_sums.astype(int)

for df in sums_df_list:
    print(df.head())
    all_years_sums = all_years_sums.add(df,fill_value=0).astype(np.int)

for df in counts_df_list:
    print(df.head())
    all_years_counts = all_years_counts.add(df,fill_value=0).astype(np.int)

all_years_sums = pd.DataFrame(all_years_sums.rename('N_FoundPhrase',inplace=True))
all_years_counts = pd.DataFrame(all_years_counts.rename('TotalN',inplace=True))

print(all_years_counts)
print(all_years_sums)

# %%
df = pd.merge(all_years_counts,all_years_sums,left_index=True,right_index=True)
df['pct_with_phrase'] = df.N_FoundPhrase / df.TotalN * 100
df['year'] = [int(x) for x in df.index.values]
print(df)

# %%
fig, ax = plt.subplots(1, 1)
ax = df[df.year>1970].pct_with_phrase.plot(ax=ax)
ax.set_ylabel('% of abstracts with the phrase')
# %%

# %%
