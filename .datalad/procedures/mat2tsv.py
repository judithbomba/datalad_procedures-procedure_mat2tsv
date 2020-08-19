#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 12:21:33 2020

@author: Judith Bomba
"""
import os
import sys
import pandas as pd
from datalad.distribution.dataset import require_dataset

#apparently the call structure for python automatically takes the current dataset (root?) as positional argument number two
#to resolve said dataset and to make the procedure truly universally run-able this seems to be necessary
ds = require_dataset(
    sys.argv[1],
    check_installed=True,
    purpose='converting .mat to .tsv files')


inputs = sys.argv[:]
print('inputs are: ',inputs)
input1 = sys.argv[2] #my_source
input2 = sys.argv[3] #my_destination
print('will gather .mat files from source:', input1, 'will convert to .tsv files stored in:', input2)

#print("the root of this project is:", os.path.dirname())

root = os.path.dirname(os.path.abspath('source'))
print("current working directory is: ",os.getcwd())
print("var 'root' is set to: ", root)


def mat_to_tsv(filename, filestring, destination):
    '''
    Parameters
    ----------
    filename : os path
        points to .mat files.
    filestring : string
        name of file being processed.
    destination : os path
        points to where .mat files should be stored.

    Returns
    -------
    None.

    '''
    import pandas as pd
    filenm = (filename)

    try:
        import scipy.io
        test = scipy.io.loadmat(filenm)
        #print(test)
    except NotImplementedError:
        print("scipy is not working on this file")
    except:
        ValueError('Warning: could not read the file at all...')

    mat = scipy.io.loadmat(filenm)
    mat = {k:v for k, v in mat.items() if k[0] != '_'}
    data = pd.DataFrame({k: pd.Series(v[0]) for k, v in mat.items()})

    onsets = []
    names = []
    duration = [(data.iloc[0,1])[0,0]]*(33*4) #33 entries in 4 submatrices
    for i in range(4):
        onset = data.iloc[i,0]
        onset = onset[0,:] #strip of unnecessary dimension
        for i in range(len(onset)):
            onsets.append(onset[i])


    for i in range(4):
        nm = (data.iloc[i,2])
        nm = nm[0]
        for i in range(33):
            names.append(nm)

    dataframe = pd.DataFrame(zip(onsets,duration,names), columns = ['onsets','duration','names'])

    filename = filestring[:-4]
    dataframe.to_csv('{}/{}_events.tsv'.format(destination,filename), sep = '\t', index=False)



filesource = os.path.join(root, input1)
#print(filesource)
destination = os.path.join(root, input2)

#print('#these are my files in root:\n',os.listdir(root))
#print('#these are my files in {}:\n'.format(input1),os.listdir('{}/my_source'.format(root))) #my_s
print('#these are my files in {} before converting:\n'.format(input2),os.listdir(destination)) #my_d
#print(root)

for file in os.listdir(filesource):
    if file.endswith('.mat'):
        filename = (os.path.join(filesource,file))
        #print(filename)
        filestring = file
        print(filestring[:-4], "attempted to be processed")
        mat_to_tsv(filename, filestring, destination)

print('#these are my files in {} after converting:\n'.format(input2),os.listdir(destination)) #my_d


ds.save(path='.',message='convert .mat files from source ({}) to .tsv files and store them in ({})'.format(input1,input2))
