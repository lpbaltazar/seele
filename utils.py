import warnings
warnings.filterwarnings('ignore')

import os
import time
import numpy as np
import pandas as pd

def readCSV(file, usecols = None, converters = None, encoding = None, dtype = str):
	df = pd.read_csv(file, usecols = usecols, converters = converters, encoding = encoding,
			dtype = dtype, low_memory = False)
	df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
	return df

def readChunk(file, usecols = None, converters = None, encoding = None, chunksize = 5000000, iterator = True, header = 'infer', nrows = None, skiprows = None, sep = ','):
	s = time.time()
	df = pd.read_csv(file, usecols = usecols, converters = converters, encoding = encoding,
			chunksize = chunksize, iterator = iterator, header = header, low_memory = False, dtype = str, nrows = nrows, skiprows = skiprows, sep = sep)
	df = pd.concat(df)
	# df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
	e = time.time()
	total_time = time.strftime("%H:%M:%S", time.gmtime(e-s))
	print("Finish reading file {} in {}".format(file, total_time))
	return df

def toCSV(df, file, index = True, encoding = None, sep = ','):
	df.to_csv(file, index = index, encoding = encoding, sep = sep)
