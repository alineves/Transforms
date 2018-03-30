import numpy as np
import math
import numpy as np
import struct
import dcts.wave as wave

saveType  = 'int16'
savePack = '>h'

class WaveEncoded:
    encodedData = []
    qtdDescartes = 0
    fs = 0
    totalAmostras = 0
    mode = ""
    level = 0

    def __init__(self, encodedData, fs, totalAmostras, mode, level):
        self.encodedData = encodedData
        self.fs  = fs
        self.totalAmostras = totalAmostras
        self.mode = mode
        self.level = level
        self.qtdDescartes = 0

    @classmethod
    def comAmostrasDescartadas(cls, encodedData, totalAmostras, qtdDescartes, fs, mode, level):
        encoded = cls(encodedData, fs, totalAmostras, mode, level)
        encoded.qtdDescartes = qtdDescartes
        encoded._preencherQuadros()
        return encoded
    
    def _preencherQuadros(self):
        if self.qtdDescartes == 0:
            return
        
        zeros = np.zeros(self.qtdDescartes)
        posicao_zeros_relativa = self.tamanhoQuadro - self.qtdDescartes
        for i in range(0, self.qtQuadros):
            pos = i * self.tamanhoQuadro + posicao_zeros_relativa
            self.encodedData = np.insert(self.encodedData, pos, zeros)


    def descartar(self, qtdDescartes):
        self.qtdDescartes = qtdDescartes
    
    def getDados(self):
        return self.encodedData

    def getDadosComprimidos(self):
        ret = np.empty(0)
        for i in range(0, self.qtQuadros):
            init = i * self.tamanhoQuadro
            end = init + self.tamanhoQuadro - self.qtdDescartes

            retInit = i * (self.tamanhoQuadro - self.qtdDescartes)
            retEnd = retInit + self.tamanhoQuadro - self.qtdDescartes
            ret[retInit : retEnd] = self.encodedData[init : end]
        return ret

    def _writeHeader(self, writter):
        writter.write(struct.pack('IIHsB',  self.fs, self.totalAmostras, self.qtdDescartes, self.mode, self.level))

    def _writeData(self, writter):
        desn = self.getDadosComprimidos()
        max = desn.max()
        writter.write(struct.pack('d', max))
        norm = _normalize(desn, max, saveType)
        for i in range(0, len(norm)):
            piece = norm[i]
            writter.write('I', len(piece))
            for j in range(0, len(piece))
                writter.write(struct.pack(savePack, piece[j]))

    def saveToFile(self, filename):
        with open(filename, 'wb') as f:
            self._writeHeader(f)
            self._writeData(f)

    @classmethod
    def loadFromFile(cls, filename):
        with open(filename, 'rb') as r:
            (totalAmostras, tamanhoQuadro, qtdDescartes, fs, sobreposicao) = _readHeader(r)
            encodedData = _readData(r)
            return WaveEncoded.comAmostrasDescartadas(
                encodedData, tamanhoQuadro,
                totalAmostras, qtdDescartes, fs, sobreposicao)
    
    @classmethod
    def loadFromEncoded(cls, encoded):
        return WaveEncoded.comAmostrasDescartadas(encoded.getDadosComprimidos(),
            encoded.tamanhoQuadro, encoded.totalAmostras, encoded.qtdDescartes, encoded.fs, encoded.sobreposicao)

def _readMax(reader):
    size = struct.calcsize('d')
    buff = reader.read(size)
    return struct.unpack('d', buff)

def _readData(reader):
    max = _readMax(reader)
    buff = reader.read()
    isize = struct.calcsize(savePack)
    size = len(buff) // isize
    ret = np.empty(size)
    for i in range(0, size):
        val = struct.unpack_from(savePack, buff, offset=(i * isize))[0]
        ret[i] = val
    return ret / wave.normalizer(saveType) * max

def _readHeader(reader):
    size = struct.calcsize('IIfsB')
    buff = reader.read(size)
    (fs, totalAmostras, qtdDescartes, mode, level) = struct.unpack('IIfsB', buff)
    return (fs, totalAmostras, qtdDescartes, mode, level)

def _normalize(array, max, tp):
    return ((array / max) * wave.normalizer(tp)).astype(tp)
    