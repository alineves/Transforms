import numpy as np
import math
import numpy as np
import struct
import dcts.wave as wave

class WaveEncoded:
    encodedData = []
    tamanhoQuadro = 0
    qtdDescartes = 0
    qtQuadros = 0
    totalAmostras = 0
    sobreposicao = 0

    def __init__(self, encodedData, tamanhoQuadro, totalAmostras, sobreposicao = 0):
        self.encodedData = encodedData
        self.tamanhoQuadro = tamanhoQuadro
        self.totalAmostras = totalAmostras
        self.sobreposicao = sobreposicao
        self.qtdDescartes = 0
        self.qtQuadros = math.ceil(totalAmostras / (tamanhoQuadro - sobreposicao))
    
    @classmethod
    def comAmostrasDescartadas(cls, encodedData, tamanhoQuadro, totalAmostras, qtdDescartes, sobreposicao = 0):
        encoded = cls(encodedData, tamanhoQuadro, totalAmostras, sobreposicao)
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
    def getTotalAmostras(self):
        return self.totalAmostras

    def getDadosComprimidos(self):
        ret = np.zeros(self.qtQuadros * (self.tamanhoQuadro - self.qtdDescartes))
        for i in range(0, self.qtQuadros):
            init = i * self.tamanhoQuadro
            end = init + self.tamanhoQuadro - self.qtdDescartes

            retInit = i * (self.tamanhoQuadro - self.qtdDescartes)
            retEnd = retInit + self.tamanhoQuadro - self.qtdDescartes
            ret[retInit : retEnd] = self.encodedData[init : end]
        return ret

    def _writeHeader(self, writter):
        writter.write(struct.pack('IHHH',  self.totalAmostras,
         self.tamanhoQuadro, self.qtdDescartes, self.sobreposicao))

    def _writeData(self, writter):
        desn = self.getDadosComprimidos()
        max = desn.max()
        writter.write(struct.pack('d', max))
        norm = _normalize(desn, max, 'int16')
        for i in range(0, len(norm)):
            writter.write(struct.pack('>h', norm[i]))

    def saveToFile(self, filename):
        with open(filename, 'wb') as f:
            self._writeHeader(f)
            self._writeData(f)

    @classmethod
    def loadFromFile(cls, filename):
        with open(filename, 'rb') as r:
            (totalAmostras, tamanhoQuadro, qtdDescartes, sobreposicao) = _readHeader(r)
            encodedData = _readData(r)
            return WaveEncoded.comAmostrasDescartadas(
                encodedData, tamanhoQuadro,
                totalAmostras, qtdDescartes, sobreposicao)
    
    @classmethod
    def loadFromEncoded(cls, encoded):
        return WaveEncoded.comAmostrasDescartadas(encoded.getDadosComprimidos(),
            encoded.tamanhoQuadro, encoded.totalAmostras, encoded.qtdDescartes, encoded.sobreposicao)

def _readMax(reader):
    size = struct.calcsize('d')
    buff = reader.read(size)
    return struct.unpack('d', buff)

def _readData(reader):
    max = _readMax(reader)
    buff = reader.read()
    isize = struct.calcsize('>h')
    size = len(buff) // isize
    ret = np.empty(size)
    for i in range(0, size):
        val = struct.unpack_from('>h', buff, offset=(i * isize))[0]
        ret[i] = val
    return ret / wave.normalizer('int16') * max

def _readHeader(reader):
    size = struct.calcsize('IHHH')
    buff = reader.read(size)
    (totalAmostras, tamanhoQuadro, qtdDescartes, sobreposicao) = struct.unpack('IHHH', buff)
    return (totalAmostras, tamanhoQuadro, qtdDescartes, sobreposicao)

def _normalize(array, max, tp):
    return ((array / max) * wave.normalizer(tp)).astype(tp)
    