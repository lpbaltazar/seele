import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("../")

import os
import time
import pandas as pd
import numpy as np

from utils import readChunk
import matplotlib as mpl
mpl.use('tKagg')
from matplotlib import pyplot as plt
import seaborn as sns

import matplotlib.style as style

sns.set()
style.use('seaborn-poster')
style.use('bmh')

file = "results/regularity.csv"
df = readChunk(file)
df['RWEEK'] = df['RWEEK'].astype(int)

plot = sns.distplot(a = df['RWEEK'].values, kde = False)
plt.show()