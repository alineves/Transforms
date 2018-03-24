import numpy as np
import dcts.encoded as enc

def codec(dados, amostrasPorQuadro, funcCalc, funcBase):
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
    tamanhoQuadro = calculaTempoQuadro(fs, tempoQuadro)
    encData = codec(audioData, tamanhoQuadro, alg.encode, alg.calculaBase)
    return enc.WaveEncoded(encData, tamanhoQuadro, len(audioData))

def decode(encoded, fs, tempoQuadro, alg):
    return codec(encoded, calculaTempoQuadro(fs, tempoQuadro), alg.decode, alg.calculaBase)

def decodeFromEncoded(encoded, fs, tempoQuadro, alg):
    novoEncoded = enc.WaveEncoded.loadFromEncoded(encoded)
    result = codec(novoEncoded.getDados(), calculaTempoQuadro(fs, tempoQuadro), alg.decode, alg.calculaBase)
    toRemove = (encoded.totalAmostras - len(result))
    return result[:toRemove]

def calculaTempoQuadro(fs, tempoQuadro):
    return int(fs * tempoQuadro)

def decodeFromWaveEncoded(waveEncode, alg):
    return codec(waveEncode.encodedData, waveEncode.tamanhoQuadro, alg.decode, alg.calculaBase)