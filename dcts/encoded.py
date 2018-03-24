import numpy as np
import math
import struct
import dcts.wave as wave

class WaveEncoded:
    encodedData = []
    tamanhoQuadro = 0
    qtdDescartes = 0
    qtQuadros = 0
    totalAmostras = 0

    def __init__(self, encodedData, tamanhoQuadro, totalAmostras):
        self.encodedData = encodedData
        self.tamanhoQuadro = tamanhoQuadro
        self.totalAmostras = totalAmostras
        self.qtdDescartes = 0
        self.qtQuadros = math.ceil(totalAmostras / tamanhoQuadro)
    
    @classmethod
    def comAmostrasDescartadas(cls, encodedData, tamanhoQuadro, totalAmostras, qtdDescartes):
        encoded = cls(encodedData, tamanhoQuadro, totalAmostras)
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
        ret = np.zeros(self.qtQuadros * (self.tamanhoQuadro - self.qtdDescartes))
        for i in range(0, self.qtQuadros):
            init = i * self.tamanhoQuadro
            end = init + self.tamanhoQuadro - self.qtdDescartes

            retInit = i * (self.tamanhoQuadro - self.qtdDescartes)
            retEnd = retInit + self.tamanhoQuadro - self.qtdDescartes
            ret[retInit : retEnd] = self.encodedData[init : end]
        return ret

    def _writeHeader(self, writter):
        writter.write(struct.pack('>III',  self.totalAmostras, self.tamanhoQuadro, self.qtdDescartes))

    def _writeData(self, writter):
        desn = wave.desnormalize(self.getDadosComprimidos(), 16)
        writter.write(struct.pack('>I', len(desn)))
        toWrite = desn.ravel().view('b').data
        writter.write(toWrite)

    def saveToFile(self, filename):
        with open(filename, 'wb') as f:
            self._writeHeader(f)
            self._writeData(f)

    @classmethod
    def loadFromFile(cls, filename):
        with open(filename, 'rb') as r:
            (totalAmostras, tamanhoQuadro, qtdDescartes) = _readHeader(r)
            encodedData = _readData(r)
            return WaveEncoded.comAmostrasDescartadas(encodedData, tamanhoQuadro, totalAmostras, qtdDescartes)

def _readShapeSize(reader):
    size = struct.calcsize('>I')
    buff = reader.read(size)
    return struct.unpack('>I', buff)

def _readData(reader):
    size = _readShapeSize(reader)[0]
    start = reader.tell()
    data = np.memmap(reader, dtype='int16', mode='c', offset=start, shape=(size,))
    return wave.normalize(data)

def _readHeader(reader):
    size = struct.calcsize('>III')
    buff = reader.read(size)
    (totalAmostras, tamanhoQuadro, qtdDescartes) = struct.unpack('>III', buff)
    return (totalAmostras, tamanhoQuadro, qtdDescartes)
    