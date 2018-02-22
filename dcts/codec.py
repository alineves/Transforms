import numpy as np

def codec(dados, fs, tempoQuadro, funcCalc, funcBase):
    amostrasPorQuadro = int(fs * tempoQuadro)
    totalAmostras = len(dados)
    base = funcBase(amostrasPorQuadro)

    ret = np.array([])
    for i in range(0, totalAmostras, amostrasPorQuadro):
        quadro = _extrairQuadro(dados, i, amostrasPorQuadro)
        result = funcCalc(quadro, base)
        ret = np.append(ret, result[0: amostrasPorQuadro])
    return ret

def _extrairQuadro(audioData, inicio, amostrasPorQuadro):
    quadro = audioData[inicio: inicio + amostrasPorQuadro]
    tamanho = len(quadro)
    ret = np.zeros(amostrasPorQuadro)
    ret[0:tamanho] = quadro[0:tamanho]
    return ret

def encode(audioData, fs, tempoQuadro, alg):
    return codec(audioData, fs, tempoQuadro, alg.encode, alg.calculaBase)

def decode(encoded, fs, tempoQuadro, alg):
    return codec(encoded, fs, tempoQuadro, alg.decode, alg.calculaBase)