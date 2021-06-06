import numpy as np

def to_cdf(pdf):
	cdf = np.zeros(256)
	for i in range(256):
		if (i == 0):
			cdf[i] = pdf[i]
		else:
			cdf[i] += cdf[i-1] + pdf[i]
	return cdf