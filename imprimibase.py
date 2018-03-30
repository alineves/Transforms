import dcts.dct2 as dct2
import dcts.dct3 as dct3
import numpy as np

base = dct3.calculaBase(4)

print(base)

quadro = np.array([1., 2., 3., 4.])

result = dct3.encode(quadro, base)

print(result)

result = dct3.decode(result, base)

print(result)