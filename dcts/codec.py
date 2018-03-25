import numpy as np
import math
import dcts.encoded as enc

def _calcularJanelaCosenoLevantado(sobreposicao):
    h1 = np.empty(sobreposicao)
    h2 = np.empty(sobreposicao)
    for i in range(0, sobreposicao):
        cosenoLevantado = math.cos(math.pi * i / sobreposicao)
        h1[i] = 0.5 * (1 - cosenoLevantado)
        h2[i] = 0.5 * (1 + cosenoLevantado)
    return h1, h2

def _decodeSobreposto(dados, amostrasPorQuadro, funcCalc, funcBase, sobreposicao):
    totalAmostras = len(dados)
    base = funcBase(amostrasPorQuadro)

    h1, h2 = _calcularJanelaCosenoLevantado(sobreposicao)

    quadroAnterior = None
    ret = np.array([])
    for i in range(0, totalAmostras, amostrasPorQuadro):
        quadro = _extrairQuadro(dados, i, amostrasPorQuadro)
        quadroAtual = funcCalc(quadro, base)
        if (quadroAnterior is not None):
            quadroAnterior[amostrasPorQuadro - sobreposicao:] *= h1
            quadroAtual[:sobreposicao] *= h2
            quadroAnterior[amostrasPorQuadro - sobreposicao:] += quadroAtual[:sobreposicao]
            if (len(ret) > 0):
                ret = np.append(ret, quadroAnterior[sobreposicao:])
            else:
                ret = np.append(ret, quadroAnterior)
        quadroAnterior = quadroAtual
    ret = np.append(ret, quadroAnterior[sobreposicao:])
    return ret
    
def _encodeSobreposto(dados, amostrasPorQuadro, funcCalc, funcBase, sobreposicao):
    totalAmostras = len(dados)
    base = funcBase(amostrasPorQuadro)

    ret = np.array([])
    for i in range(0, totalAmostras, (amostrasPorQuadro - sobreposicao)):
        quadro = _extrairQuadro(dados, i, amostrasPorQuadro)
        result = funcCalc(quadro, base)
        ret = np.append(ret, result[0: amostrasPorQuadro])
    return ret


def codec(dados, amostrasPorQuadro, funcCalc, funcBase):
   return _encodeSobreposto(dados, amostrasPorQuadro, funcCalc, funcBase, 0)

def _extrairQuadro(audioData, inicio, amostrasPorQuadro):
    quadro = audioData[inicio: inicio + amostrasPorQuadro]
    tamanho = len(quadro)
    ret = np.zeros(amostrasPorQuadro)
    ret[0:tamanho] = quadro[0:tamanho]
    return ret

def encode(audioData, fs, tempoQuadro, alg, sobreposicao = 0):
    tamanhoQuadro = calculaTamanhoQuadro(fs, tempoQuadro)
    if (sobreposicao > 0):
        encData = _encodeSobreposto(audioData, tamanhoQuadro, alg.encode, alg.calculaBase, sobreposicao)
    else:
        encData = codec(audioData, tamanhoQuadro, alg.encode, alg.calculaBase) 
    return enc.WaveEncoded(encData, tamanhoQuadro, len(audioData), sobreposicao)

def _decode(encoded, tamanhoQuadro, alg, sobreposicao = 0):
    if (sobreposicao > 0):
        result = _decodeSobreposto(encoded, tamanhoQuadro, alg.decode, alg.calculaBase, sobreposicao)
    else:
        result = codec(encoded, tamanhoQuadro, alg.decode, alg.calculaBase)
    return result

def decode(encoded, fs, tempoQuadro, alg, sobreposicao = 0):
    return  _decode(encoded, calculaTamanhoQuadro(fs, tempoQuadro), alg, sobreposicao)

def decodeFromEncoded(encoded, alg):
    novoEncoded = enc.WaveEncoded.loadFromEncoded(encoded)
    result = _decode(novoEncoded.getDados(), novoEncoded.tamanhoQuadro, alg, novoEncoded.sobreposicao)
    toRemove = (encoded.totalAmostras - len(result))
    return result[:toRemove]

def calculaTamanhoQuadro(fs, tempoQuadro):
    return int(fs * tempoQuadro)

def decodeFromWaveEncoded(waveEncode, alg):
    return codec(waveEncode.encodedData, waveEncode.tamanhoQuadro, alg.decode, alg.calculaBase)