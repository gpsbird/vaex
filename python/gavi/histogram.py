# -*- coding: utf-8 -*-

from numba import jit
import numba
#print numba.__version__
import math

@jit(nopython=True)
def hist1d(x, counts, dataminx, datamaxx):
	length = len(x)
	bincountx  = len(counts)
	for i in range(length):
		xvalue = x[i]
		binNox = int(math.floor( ((xvalue - dataminx) / (float(datamaxx) - dataminx)) * float(bincountx)))
		if binNox >= 0 and binNox < bincountx:
			counts[binNox] += 1

@jit(nopython=True)
def hist1d_weights(x, counts, weights, dataminx, datamaxx):
	length = len(x)
	bincountx  = len(counts)
	for i in range(length):
		xvalue = x[i]
		binNox = int(math.floor( ((xvalue - dataminx) / (float(datamaxx) - dataminx)) * float(bincountx)))
		if binNox >= 0 and binNox < bincountx:
			if not math.isnan(weights[i]):
				counts[binNox] += weights[i]

@jit
def hist2d(x, y, counts, dataminx, datamaxx, dataminy, datamaxy):
	length = len(x)
	bincountx, bincounty = counts.shape
	for i in range(length):
		binNox = int(math.floor( ((x[i] - dataminx) / (float(datamaxx) - dataminx)) * float(bincountx)))
		binNoy = int(math.floor( ((y[i] - dataminy) / (float(datamaxy) - dataminy)) * float(bincounty)))
		if binNox >= 0 and binNox < bincountx and binNoy >= 0 and binNoy < bincounty:
			counts[binNox, binNoy] += 1
	return counts

@jit
def hist2d_weights(x, y, counts, weights, dataminx, datamaxx, dataminy, datamaxy):
	length = len(x)
	bincountx, bincounty = counts.shape
	for i in range(length):
		binNox = int(math.floor( ((x[i] - dataminx) / (float(datamaxx) - dataminx)) * float(bincountx)))
		binNoy = int(math.floor( ((y[i] - dataminy) / (float(datamaxy) - dataminy)) * float(bincounty)))
		if binNox >= 0 and binNox < bincountx and binNoy >= 0 and binNoy < bincounty:
			if not math.isnan(weights[i]):
				counts[binNox, binNoy] += weights[i]
	return counts

@jit(nopython=True)
def hist3d(x, y, z, counts, dataminx, datamaxx, dataminy, datamaxy, dataminz, datamaxz):
	length = len(x)
	#counts = np.zeros((bincountx, bincounty), dtype=np.int32)
	bincountx, bincounty, bincountz = counts.shape
	#print length
	#return bindata#
	for i in range(length):
		binNox = int(math.floor( ((x[i] - dataminx) / (float(datamaxx) - dataminx)) * float(bincountx)))
		binNoy = int(math.floor( ((y[i] - dataminy) / (float(datamaxy) - dataminy)) * float(bincounty)))
		binNoz = int(math.floor( ((z[i] - dataminz) / (float(datamaxz) - dataminz)) * float(bincountz)))
		if binNox >= 0 and binNox < bincountx and binNoy >= 0 and binNoy < bincounty and binNoz < bincountz:
			counts[binNox, binNoy, binNoz] += 1
	#step = float(datamax-datamin)/bincount
	#return numpy.arange(datamin, datamax+step/2, step), binData
	return counts


@jit
def hist2d_and_shuffled(x, y, counts, counts_shuffled, dataminx, datamaxx, dataminy, datamaxy, offset):
	length = len(x)
	bincountx, bincounty = counts.shape
	for i in range(length):
		if not (math.isnan(x[i]) or math.isnan(y[i])):
			binNox = int(math.floor( ((x[i] - dataminx) / (float(datamaxx) - dataminx)) * float(bincountx)))
			binNoy = int(math.floor( ((y[i] - dataminy) / (float(datamaxy) - dataminy)) * float(bincounty)))
			if binNox >= 0 and binNox < bincountx and binNoy >= 0 and binNoy < bincounty:
				counts[binNox, binNoy] += 1
		j = (i + offset) % length
		if not (math.isnan(x[i]) or math.isnan(y[i])):
			binNoy = int(math.floor( ((y[j] - dataminy) / (float(datamaxy) - dataminy)) * float(bincounty)))
			if binNox >= 0 and binNox < bincountx and binNoy >= 0 and binNoy < bincounty:
				counts_shuffled[binNox, binNoy] += 1
	return counts
