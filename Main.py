# @uthor: Armando Rdz
# user: arman
# date: 04/04/2020
# IDE: JetBrains PyCharm
# description:

import pandas as pd # para leer csv
import random as rnd
import time
import numpy as np
import math

def read_dataset():
	# se lee el dataset en formato csv.
	x_df = pd.read_csv('datasets\\iris.data', header=None, index_col=False)
	return x_df

def distEuclidiana(p1, p2):
	sum = np.zeros(4)
	for i in range(4):
		sum[i] = p1[i] - p2[i]
	for i in range(4):
		sum[i] = pow(sum[i], 2)
	r = 0
	for i in range(4):
		r += sum[i]
	return math.sqrt(r)

def getMatrizDistancias(k, centroides, no_centroides):
	distancias = np.zeros((150, k))  # matriz de distancias
	for c in range(k):
		for f in range(150):
			if f != no_centroides[c]:
				distancias[f][c] = distEuclidiana(centroides[c], D[f])
	return distancias

def getMatrizGrupos(k, distancias):
	grupos = np.zeros((150, k))  # matriz de 0s y 1s (grupos)
	for f in range(150):  # asignacion de la matriz de grupos
		index_mayor_val = np.where(distancias[f] == np.amin(distancias[f]))
		for c in range(k):
			if c == index_mayor_val[0]:  # asignalo al grupo
				grupos[f][c] = 1
			else:  # no es del grupo
				grupos[f][c] = 0
	return grupos

def sinCambios(k, m_group_old, m_group_curr):
	r = 0
	for f in range(150):
		for c in range(k):
			if m_group_old[f][c] != m_group_curr[f][c]:
				r += 1
	return r

def k_means(k, D):

	# 1er Paso : Elegir los k centroides iniciales de manera random
	rnd.seed(time.time())
	#rnd.seed(1)
	centroides = np.zeros((k, 4)) # matriz de centroides
	no_centroides = np.zeros(k) # saber la fila de los centroides iniciales
	for i in range(k):
		r = rnd.randint(0, 149)
		centroides[i] = D[r]
		no_centroides[i] = r

	sigue = 1
	cont = 0
	while (sigue == 1):
		print('Iteracion: {}'.format(cont))
		print(centroides)

		# FIXME: Los valores terminan en un solo grupo, comunmente a partir de la 1er iteracion.

		# 2do Paso : (re)asignar cada objeto al centroide mas cercano
		distancias = getMatrizDistancias(k, centroides, no_centroides)  # calcular la matriz de distancias
		grupos = getMatrizGrupos(k, distancias)  # calcular la matriz de grupo
		#print(distancias)
		if cont > 0:
			if sinCambios(k, grupos_anterior, grupos) == 0: # la matriz de grupos sin cambios
				sigue = 0
				print('Sin Cambios')
				break

		# 3er Paso : calcular valor promedio de cada grupo
		n_objetos_grupo = np.zeros((k))
		for c in range(k):
			for f in range(150):
				if grupos[f][c] == 1:
					n_objetos_grupo[c] += 1 # conteo de objetos en cada grupo
		#print(n_objetos_grupo)

		# calcular valores promedio
		prom = np.zeros((k, 4)) # 4 grupos 4 dimensiones
		for g in range(k): # grupos
			col = grupos[:, g] # obten la columna entera
			for x in range(4): # dimensiones
				for f in range(150): # filas
					if col[f] == 1:
						prom[g][x] += D[f][x]
		for g in range(k): # grupos
			for d in range(4): # dimensiones
				prom[g][d] = prom[g][d] / 150
		#print(prom)

		centroides = prom
		grupos_anterior = grupos  # matriz de grupo iteracion pasada
		print(grupos)
		#print(distancias)
		cont += 1


print('Algoritmo K-Means | Mineria de Datos | Lenguaje Python')
k = int(input('K = '))
ds = read_dataset()
D = ds.values[:, 0:4]
class_type = ds.values[:, 4:1]
k_means(k, D)