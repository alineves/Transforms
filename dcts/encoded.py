import numpy as np
import math
import numpy as np
import struct
import dcts.wave as wave

saveType  = 'int16'
savePack = '>h'

class WaveEncoded:
    encodedData = []
    tamanhoQuadro = 0
    qtdDescartes = 0
    qtQuadros = 0
    fs = 0
    totalAmostras = 0
    sobreposicao = 0

    def __init__(self, encodedData, tamanhoQuadro, totalAmostras, fs, sobreposicao = 0):
        self.encodedData = encodedData
        self.tamanhoQuadro = tamanhoQuadro
        self.totalAmostras = totalAmostras
        self.sobreposicao = sobreposicao
        self.fs  = fs
        self.qtdDescartes = 0
        self.qtQuadros = math.ceil(totalAmostras / (tamanhoQuadro - sobreposicao))
    
    @classmethod
    def comAmostrasDescartadas(cls, encodedData, tamanhoQuadro, totalAmostras, qtdDescartes, fs, sobreposicao = 0):
        encoded = cls(encodedData, tamanhoQuadro, totalAmostras, fs, sobreposicao)
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
        writter.write(struct.pack('IHHIH',  self.totalAmostras,
         self.tamanhoQuadro, self.qtdDescartes, self.fs, self.sobreposicao))

    def _writeData(self, writter):
        desn = self.getDadosComprimidos()
        max = desn.max()
        writter.write(struct.pack('d', max))
        norm = _normalize(desn, max, saveType)
        for i in range(0, len(norm)):
            writter.write(struct.pack(savePack, norm[i]))

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
    size = struct.calcsize('IHHIH')
    buff = reader.read(size)
    (totalAmostras, tamanhoQuadro, qtdDescartes, fs, sobreposicao) = struct.unpack('IHHIH', buff)
    return (totalAmostras, tamanhoQuadro, qtdDescartes, fs, sobreposicao)

def _normalize(array, max, tp):
    return ((array / max) * wave.normalizer(tp)).astype(tp)
    