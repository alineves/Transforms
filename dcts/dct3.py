import math
import numpy as np
import dcts.codec as cd

def calculaBase(amostrasPorQuadro):
    base1 = np.zeros((amostrasPorQuadro, amostrasPorQuadro))
    for k in range(0, amostrasPorQuadro):
        for n in range(0, amostrasPorQuadro ):
            base3[k, n] = math.cos(math.pi*(2*k+1)*n/(amostrasPorQuadro*2))
    
    base3[0, 0:] *= 0.5
    base3[amostrasPorQuadro - 1, 0:] *=  0.5
    return base3

def encode(quadro, base):
    return quadro.dot(base) * 2

def decode(quadro, base):
    return quadro.dot(base) / len(quadro)