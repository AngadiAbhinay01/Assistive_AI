import numpy as np
from scipy import stats

a = [1, 2, 2, 3, 4, 4, 4, 5]

mean_1 = np.mean(a)
print(mean_1)

median_1 = np.median(a)
print(median_1)

mode_1 = stats.mode(a)
print(mode_1.mode)