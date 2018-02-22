import math
import numpy as np
import dcts.codec as cd

def calculaBase(amostrasPorQuadro):
    base1 = np.zeros((amostrasPorQuadro, amostrasPorQuadro))
    for k in range(0, amostrasPorQuadro):
        for n in range(0, amostrasPorQuadro ):
            base1[k, n] = math.cos((math.pi/(amostrasPorQuadro - 1))*k*n)
    
    base1[0, 0:] *= 0.5
    base1[amostrasPorQuadro - 1, 0:] *=  0.5
    return base1

def encode(quadro, base):
    return quadro.dot(base) * 2

def decode(quadro, base):
    return quadro.dot(base) / (len(quadro) -1)