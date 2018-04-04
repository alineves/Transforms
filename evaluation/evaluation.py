import numpy as np
import math

def evaluate_snr_seg(ref, test, amostrasPorQuadro, sobreposicao):
    totalAmostras = len(ref)
    snrs = np.array([])
    for i in range(0, totalAmostras, amostrasPorQuadro - sobreposicao):
        quadroRef = _extrairQuadro(ref, i, amostrasPorQuadro)
        quadroTest = _extrairQuadro(test, i, amostrasPorQuadro)
        
        eref = np.sum(np.power(quadroRef, 2))
        eerro = np.sum(np.power(quadroRef - quadroTest, 2))
        if (eerro == 0):
            snr = float('inf')
        else:
            snr = 10 * math.log10(eref / eerro)
        snrs = np.append(snrs, snr)
    return np.sum(snrs) / len(snrs)

def evaluate_snr_total(ref, test):
    eref = np.sum(np.power(ref, 2))
    eerro = np.sum(np.power(ref - test, 2))
    return 10 * math.log10(eref / eerro)


def _extrairQuadro(audioData, inicio, amostrasPorQuadro):
    quadro = audioData[inicio: inicio + amostrasPorQuadro]
    tamanho = len(quadro)
    ret = np.zeros(amostrasPorQuadro)
    ret[0:tamanho] = quadro[0:tamanho]
    return ret