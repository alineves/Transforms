from scipy.fftpack import dct
from scipy.io.wavfile import read, write
import numpy as np
import math

def open_wave(filename):
    rate, audData = read(filename)
    return rate, normalize(audData)

def open_wave_nn(filename):
    rate, audData = read(filename)
    return rate, audData

def save_wave(filename, rate, data, br):
    write(filename, rate, desnormalize(data, br))

def normalizer(dtype):
    nb_bits = 8
    if  dtype == 'int16':
        nb_bits = 16
    elif dtype == 'int32':
        nb_bits = 32

    return 2 ** (nb_bits - 1)

def normalize(audData):
    max_nb_bit = float(normalizer(audData.dtype))
    return audData / max_nb_bit

def desnormalize(audData, bits):
    dtype = 'int' + str(bits)
    dt = np.rint(audData * normalizer(dtype))
    return dt.astype(dtype)


def calculaBaseDct1(amostrasPorQuadro):
    base1 = np.zeros((amostrasPorQuadro, amostrasPorQuadro))
    for k in range(0, amostrasPorQuadro):
        for n in range(0, amostrasPorQuadro ):
            base1[k, n] = math.cos((math.pi/(amostrasPorQuadro - 1))*k*n)
    
    base1[0, 0:] *= 0.5
    base1[amostrasPorQuadro - 1, 0:] *=  0.5
    return base1

def calculaBaseDct2(amostrasPorQuadro):
    base2 = np.zeros((amostrasPorQuadro, amostrasPorQuadro))
    for k in range(0, amostrasPorQuadro):
        for n in range(0, amostrasPorQuadro):
            base2[k, n] = math.cos((math.pi/(2*amostrasPorQuadro))*k*((2*n) + 1))
    return base2

def calculaBaseDct3(amostrasPorQuadro):
    base3 = np.zeros((amostrasPorQuadro, amostrasPorQuadro))
    for k in range(0, amostrasPorQuadro):
        for n in range(0, amostrasPorQuadro):
            base3[k, n] = math.cos((math.pi/(2*amostrasPorQuadro))*n*((2*k) + 1))
    return base3

def calculaBaseDct4(amostrasPorQuadro):
    base4 = np.zeros((amostrasPorQuadro,amostrasPorQuadro))
    for k in range(0, amostrasPorQuadro):
        for n in range(0, amostrasPorQuadro):
            base4[k, n] = math.cos((math.pi/amostrasPorQuadro)*(k + 0.5)*(n + 0.5))
    return base4

def encodeDct1(audioData, fs, tempoQuadro):
    return codec(audioData, fs, tempoQuadro, _dct1Quadro, calculaBaseDct1)

def decodeDct1(encoded, fs, tempoQuadro):
    return codec(encoded, fs, tempoQuadro, _idct1Quadro, calculaBaseDct1)

def encodeDct2(audioData, fs, tempoQuadro):
    return codec(audioData, fs, tempoQuadro, _dct2Quadro, calculaBaseDct2)

def decodeDct2(encoded, fs, tempoQuadro):
    return codec(encoded, fs, tempoQuadro, _idct2Quadro, calculaBaseDct2)

def encodeDct3(audioData, fs, tempoQuadro):
    return codec(audioData, fs, tempoQuadro, _dct3Quadro, calculaBaseDct3)

def decodeDct3(encoded, fs, tempoQuadro):
    return codec(encoded, fs, tempoQuadro, _idct3Quadro, calculaBaseDct3)

def encodeDct4(audioData, fs, tempoQuadro):
    return codec(audioData, fs, tempoQuadro, _dct4Quadro, calculaBaseDct4)

def decodeDct4(encoded, fs, tempoQuadro):
    return codec(encoded, fs, tempoQuadro, _idct4Quadro, calculaBaseDct4)

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

def _dct1Quadro(quadro, base):
    return quadro.dot(base) * 2

def _idct1Quadro(quadro, base):
    return quadro.dot(base) / (len(quadro) -1)

def _dct2Quadro(quadro, base):
    return base.dot(quadro) * 2

def _idct2Quadro(quadro, base):
    Xc2 = quadro.dot(base)
    Xc2 *= 0.5
    return Xc2/len(quadro)

def _dct3Quadro(quadro, base):
    base[0:, 0] *= 0.5
    return quadro.dot(base) * 2 

def _idct3Quadro(quadro, base):
    return quadro.dot(base.T) / (len(quadro))

def _dct4Quadro(quadro, base):
    return quadro.dot(base) * 2

def _idct4Quadro(quadro, base):
    return quadro.dot(base) / len(quadro)