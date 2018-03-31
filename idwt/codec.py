import pywt
import math
import numpy as np
import idwt.encoded as enc

def encode(dados, fs, tempoQuadro, mode, level):
    totalAmostras = len(dados)
    amostrasPorQuadro = int(fs * tempoQuadro)

    ret = enc.WaveEncoded.fromEncoded(fs, totalAmostras, amostrasPorQuadro, enc.Mode.fromString(mode), level)
    for i in range(0, totalAmostras, amostrasPorQuadro):
        quadro = _extrairQuadro(dados, i, amostrasPorQuadro)
        result = pywt.wavedec(quadro, mode, level=level)
        ret.addQuadro(result)
    return ret

def _extrairQuadro(audioData, inicio, amostrasPorQuadro):
    quadro = audioData[inicio: inicio + amostrasPorQuadro]
    tamanho = len(quadro)
    ret = np.zeros(amostrasPorQuadro)
    ret[0:tamanho] = quadro[0:tamanho]
    return ret