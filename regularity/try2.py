import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("../")

import os
import time
import pandas as pd
import numpy as np

from utils import readChunk, toCSV
import matplotlib.pyplot as plt 
import matplotlib.cm as cm
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

plt.style.use("bmh")

def kmeansClustering(X, k):
	kmeans = KMeans(n_clusters=k, random_state=0).fit(X)
	labels = kmeans.labels_

	distortion = kmeans.inertia_

	centers = np.array(kmeans.cluster_centers_)

	return labels, distortion, centers


def addLabel(data, labels):

	data.loc[:, "label"] = labels

	return data


def clustering(X):

	distortions = []

	for k in range(2, 30):

		print("Clustering using k: ", k)

		labels, distortion, centers = kmeansClustering(X, k)

		distortions.append(distortion)

		print("Inertia: ", distortion)

	elbowPlot(distortions)


def elbowPlot(distortions):
	k = np.arange(2, 30)

	plt.figure(figsize=(12, 10))
	plt.plot(k, distortions, marker='o')
	plt.xlabel('Number of clusters', fontsize="x-large")
	plt.ylabel('Inertia', fontsize="x-large")

	plt.savefig("plots/elbow_plot.png", dpi=300)
	plt.close()


def silhouetteScore(X, labels, k, centers):
	silhouette_avg = silhouette_score(X, labels)
	print("Silhouette Score for Cluster={}: {}".format(k, silhouette_avg))

if __name__ == '__main__':
	file = 'results/feb3_weekly_regularity.csv'
	df = readChunk(file, header = None)
	df.rename(columns = {0:'WEEK', 8:'RWEEK', 9:'USERID'}, inplace = True)
	file2 = 'results/feb3_regularity.csv'
	df2 = readChunk(file2, header = None)
	df2.rename(columns = {0:'WEEK', 8:'RWEEK', 9:'USERID'}, inplace = True)
	df = pd.concat([df, df2])
	print('Number of customers: ', len(df.USERID.unique()))
	df['RWEEK'] = df['RWEEK'].astype(int)
	for i in range(1, 8):
		df[i] = df[i].astype(int)
	new_df = df.groupby('USERID')['RWEEK'].mean().to_frame()
	new_df['RWEEK'] = round(new_df['RWEEK'])
	dayofweek = df.drop('RWEEK', axis = 1).groupby('USERID').sum()
	dayofweek['total'] = dayofweek.sum(1)
	for i in range(1, 8):
		dayofweek[i] = dayofweek[i]/dayofweek['total']
	new_df = new_df.merge(dayofweek, how = 'left', on = 'USERID')
	new_df = new_df.merge(df.groupby('USERID')['WEEK'].count().to_frame(), how = 'left', on = 'USERID')
	print(new_df.head(20))

	new_df = new_df.loc[new_df.RWEEK == 1.0]
	X = new_df[[1,2,3,4,5,6,7]]

	clustering(X)

	k = input('enter chosen number of clusters: ')

	labels,_,centers = kmeansClustering(X, int(k))
	silhouetteScore(X, labels, k, centers)


