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
#xml_file_list = glob.glob( working_dir + '*n000*xml.gz') 

print(f"{len(xml_file_list):,} xml files.\n" , xml_file_list[:4])
#xml_file_list = xml_file_list[:50]

#%% function to build df & save table to file
def build_df_and_save_file_from_meline_xml(filename):
    #print(f"loading {filename}...")
    output_pickle_filename = filename+'.pickle.xz'
    try: # try loading the file, and make sure it has at least five rows & an abstract
        df = pd.read_pickle(output_pickle_filename)
        len(df.loc[5,'abstract'])>10
        df.iloc[5]
        print(f"ALREADY PROCESSED, SKIPPPING\t{filename}...")
        return pd.DataFrame() # return  None makes Spark crash
    except: # if we can't load the processed pickle file, generate it from the xml
        pubmed_dict = pp.parse_medline_xml(filename) # dictionary output
        print(f"loaded {filename}\tcontains {len(pubmed_dict)} entries.")
        tmp_df = pd.DataFrame()
        tmp_df['year'] = [d['pubdate'] for d in pubmed_dict]
        tmp_df['abstract'] = [d['abstract'] for d in pubmed_dict]
        tmp_df['abstract'] = tmp_df['abstract'].str.lower()
        tmp_df['abstract_nchar'] = [len(t) for t in tmp_df['abstract'] ]
        tmp_df = tmp_df[tmp_df.abstract_nchar > 100] # remove abstracts that are too short
        tmp_df.reset_index(inplace=True, drop=True)
        tmp_df.to_pickle(output_pickle_filename,compression='xz')
        return tmp_df


# %% multi-threaded processing of all xml files
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(build_df_and_save_file_from_meline_xml, xml_file_list)



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
