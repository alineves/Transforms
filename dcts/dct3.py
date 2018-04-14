import math
import numpy as np
import dcts.codec as cd

def getNumeroDCT():
    return 3

def matchNumeroDCT(numeroDCT):
    return numeroDCT == 3

def calculaBase(amostrasPorQuadro):
    base3 = np.zeros((amostrasPorQuadro, amostrasPorQuadro))
    for k in range(0, amostrasPorQuadro):
        for n in range(0, amostrasPorQuadro ):
            base3[k, n] = math.cos(math.pi*(2*k+1)*n/(amostrasPorQuadro*2))
    return base3

def encode(quadro, base):
    quadro[0] *= 0.5
    return base.dot(quadro) * 2

def decode(quadro, base):
    return quadro.dot(base) / len(quadro)