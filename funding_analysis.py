import multiprocessing, string, codecs, os, csv, datetime
from stop_words import get_stop_words

import bz2, pickle
import _pickle as cPickle

# save and load compressed pickle files
def decompress_pickle(filename):
    if os.path.isfile(filename):
        data = bz2.BZ2File(filename, 'rb')
    elif os.path.isfile( filename + '.pbz2' ):
        data = bz2.BZ2File(filename + '.pbz2'  , 'rb')
    else:
        print('cannot find ', filename)
        raise TypeError("Only integers are allowed")
    data = cPickle.load(data)
    return data

def compressed_pickle(filename, data):
    with bz2.BZ2File(filename + '.pbz2','w') as f: 
        cPickle.dump(data, f)


# load an abstracts CSV file and return a set of unique, no-stop & no-punctuation words
#   also save the output as a pickle file
def ProcessesWordsInAbstractFile(abstract_csv_file,year):
    abstract_text = list()
    table = str.maketrans(dict.fromkeys(string.punctuation))
    with codecs.open( abstract_csv_file , 'r' , encoding='utf-8', errors='ignore') as csvfile:
        csvr = csv.reader(csvfile,delimiter=',')
        print('Starting with ', abstract_csv_file, ' saving to disk: ', datetime.datetime.now() )
        for app_id, app_txt in csvr:
            app_txt = [s.translate(table) for s in app_txt.lower().split(' ')]
            filtered_words = [word for word in app_txt  if \
                              ( (word not in get_stop_words('english')) and (len(word)>4) )]
            abstract_text.append(set(filtered_words))
    print('Finished with ', abstract_csv_file, ' saving to disk: ', datetime.datetime.now() )
    compressed_pickle(abstract_csv_file.replace('.csv',''), (year,abstract_text))
    return( abstract_text )


# grants_abs_list is a list of sets. each set contains all the words in one grant abstract
#   identify the sets in which the word appears
#   and return the #, avg, and total # of grants (# of sets)
def CountGrantsInOneYearWithWord( grants_abs_list , word):
    binary_vect = [word in words for words in grants_abs_list]
    return( sum(binary_vect), sum(binary_vect)/len(binary_vect)*100, len(binary_vect) )
