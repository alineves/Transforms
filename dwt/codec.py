import pywt
import math
import numpy as np
import dwt.encoded_sorted_energy as enc
import dwt.encoded as encoded_remover_cd

def criarWaveEncoded(fs, totalAmostras, amostrasPorQuadro, mode, level, sobreposicao):
    return encoded_remover_cd.WaveEncoded.fromEncoded(fs, totalAmostras, amostrasPorQuadro, encoded_remover_cd.Mode.fromString(mode), level, sobreposicao)

def criarWaveEncodedSortedEnergy(fs, totalAmostras, amostrasPorQuadro, mode, level, sobreposicao):
    return enc.WaveEncoded.fromEncoded(fs, totalAmostras, amostrasPorQuadro, enc.Mode.fromString(mode), level, sobreposicao)

def encodeRemoveCD(dados, fs, tempoQuadro, mode, level, sobreposicao = 0):
    return __encode(dados, fs, tempoQuadro, mode, level, criarWaveEncoded, sobreposicao)

def encode(dados, fs, tempoQuadro, mode, level, sobreposicao = 0):
    return __encode(dados, fs, tempoQuadro, mode, level, criarWaveEncodedSortedEnergy, sobreposicao)

def __encode(dados, fs, tempoQuadro, mode, level, criarWaveEncodedFunc, sobreposicao = 0):
    totalAmostras = len(dados)
    
    #calcula quantidade de amostras por quadro
    amostrasPorQuadro = int(fs * tempoQuadro)

    #cria objeto de retorno com dados necessario para futuro decode
    ret = criarWaveEncodedFunc(fs, totalAmostras, amostrasPorQuadro, mode, level, sobreposicao)

    # Percorre quadro a quadro, considerando sobreposicao
    for i in range(0, totalAmostras - sobreposicao, amostrasPorQuadro - sobreposicao):
        #obtem o qadro
        quadro = _extrairQuadro(dados, i, amostrasPorQuadro)
        #encoda o quadro
        result = pywt.wavedec(quadro, mode, level=level)
        #adiona resultado ao objeto de retorno
        ret.addQuadro(result)
    return ret

def decode(encoded):
    if (encoded.sobreposicao > 0):
        ret = __decodeSobreposto(encoded)
    else:
        ret = __decodeNormal(encoded)
    totalAmostras = encoded.totalAmostras
    return np.resize(ret, totalAmostras)
    

def __decodeNormal(encoded):
    ret = np.empty(0)
    for i in range(encoded.quantidadeQuadros()):
        coeffs = encoded.dadosQuadro(i)
        dadosQuadro = pywt.waverec(coeffs, encoded.mode.toString())
        ret = np.append(ret, dadosQuadro)

    return ret


def __decodeSobreposto(encoded):
    h1, h2 = __calcularJanelaCosenoLevantado(encoded.sobreposicao)

    quadroAnterior = None
    ret = np.empty(0)
    for i in range(encoded.quantidadeQuadros()):
        coeffs = encoded.dadosQuadro(i)
        quadroAtual = pywt.waverec(coeffs, encoded.mode.toString())
        if (quadroAnterior is not None):
            quadroAnterior[encoded.amostrasPorQuadro - encoded.sobreposicao:] *= h1
            quadroAtual[:encoded.sobreposicao] *= h2
            quadroAnterior[encoded.amostrasPorQuadro - encoded.sobreposicao:] += quadroAtual[:encoded.sobreposicao]
            if (len(ret) > 0):
                ret = np.append(ret, quadroAnterior[encoded.sobreposicao:])
            else:
                ret = np.append(ret, quadroAnterior)
        quadroAnterior = quadroAtual
    ret = np.append(ret, quadroAnterior[encoded.sobreposicao:])
    return ret

def __calcularJanelaCosenoLevantado(sobreposicao):
    h1 = np.empty(sobreposicao)
    h2 = np.empty(sobreposicao)
    for i in range(0, sobreposicao):
        cosenoLevantado = math.cos(math.pi * i / sobreposicao)
        h1[i] = 0.5 * (1 + cosenoLevantado)
        h2[i] = 0.5 * (1 - cosenoLevantado)
    return h1, h2


def _extrairQuadro(audioData, inicio, amostrasPorQuadro):
    quadro = audioData[inicio: inicio + amostrasPorQuadro]
    tamanho = len(quadro)
    ret = np.zeros(amostrasPorQuadro)
    ret[0:tamanho] = quadro[0:tamanho]
    return ret