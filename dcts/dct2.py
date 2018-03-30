import math
import numpy as np
import dcts.codec as cd

def calculaBase(amostrasPorQuadro):
    base2 = np.zeros((amostrasPorQuadro, amostrasPorQuadro))
    for k in range(0, amostrasPorQuadro):
        for n in range(0, amostrasPorQuadro ):
            base2[k, n] = math.cos((math.pi*k*(2*n+1)) / (2*amostrasPorQuadro))
    
    return base2

def encode(quadro, base):
    return base.dot(quadro) * 2

def decode(quadro, base):
    quadro[0] *= 0.5 
    return quadro.dot(base) / len(quadro)