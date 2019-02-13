import dcts.wave as wv
import numpy as np
import math

def evaluate(ref, test, saida):
    fsRef, ref = wv.open_wave(ref)
    fsTest, test = wv.open_wave(test)
    amostrasPorQuadro = int(fsRef * 0.02)

    srn_seg = evaluate_snr_seg(ref, test, int(fsRef * 0.02))
    snr_total = evaluate_snr_total(ref, test)

    file = open(saida,"w") 
    file.write("snr_seg,snr_total")
    file.write("\n") 
    file.write("%f,%f\n" % (srn_seg, snr_total))
    file.close() 

    print(srn_seg)
    print(snr_total)


def evaluate_snr_seg(ref, test, amostrasPorQuadro):
    totalAmostras = len(ref)
    snrs = np.array([])
    for i in range(0, totalAmostras, amostrasPorQuadro):
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