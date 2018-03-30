import math
import numpy as np
import dcts.codec as cd

def calculaBase(amostrasPorQuadro):
    base4 = np.zeros((amostrasPorQuadro,amostrasPorQuadro))
    for k in range(0, amostrasPorQuadro):
        for n in range(0, amostrasPorQuadro):
            base4[k, n] = math.cos((math.pi/amostrasPorQuadro)*(k + 0.5)*(n + 0.5))
    return base4

def encode(quadro, base):
    return quadro.dot(base) * 2

def decode(quadro, base):
    return quadro.dot(base) / len(quadro)