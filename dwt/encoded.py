from enum import Enum
import numpy as np
import math
import numpy as np
import struct
import dcts.wave as wave

saveType  = 'int16'
savePack = '>h'

class Mode(Enum):
    DB1 = 0
    DB2 = 1

    @classmethod
    def fromString(cls, string):
        return {
            'db1': cls.DB1,
            'db2': cls.DB2
        }[string]

    def toString(self):
        return self.name.lower()

class Quadro:
    @classmethod
    def fromEncode(cls, dadosQuadro):
        quadro = cls()
        quadro.cds = []
        quadro.ca = dadosQuadro[0]
        for i in range(1, len(dadosQuadro)): 
            quadro.cds.append(dadosQuadro[i])
        return quadro
    
    @classmethod
    def fromReader(cls, reader):
        quadro = cls()
        quadro.cds = []
        qtdCds = struct.unpack('B', reader.read(struct.calcsize('B')))[0]
        quadro.__readCA(reader)
        for i in range(0, qtdCds):
            quadro.cds.append(quadro.__readArray(reader))
        return quadro
    
    def comprimido(self, tipoCompressao):
        if (tipoCompressao is TipoCompressao.NENHUMA):
            return self

        Quadro comprimido = Quadro()
        comprimido.ca = self.ca.copy()
        if (tipoCompressao is TipoCompressao.REMOVE_ULTIMO_CD):
            comprimido.cds = self.cds[:-1]
        return comprimido
    
    def write(self, writer):
        self.__writeHeader(writer)
        self.__writeData(writer)

    def __writeData(self, writer):
        self.__writeArray(writer, self.ca)
        for i in range(0, len(self.cds)):
            self.__writeArray(writer, self.cds[i])
    
    def __writeArray(self, writer, array):
        max = array.max()
        writer.write(struct.pack('Hd', len(array), max))
        norm = _normalize(array, max)
        for i in range(0, len(norm)):
            writer.write(struct.pack(savePack, norm[i]))

    def __writeHeader(self, writer):
        writer.write(struct.pack('B', len(self.cds)))
    
    def __readCA(self, reader):
        self.ca = self.__readArray(reader)
    
    def __readArray(self, reader):
        buffHeader = reader.read(struct.calcsize('Hd'))
        (size, max) = struct.unpack('Hd', buffHeader)
        buffData = reader.read(struct.calcsize(savePack) * size)
        ret = np.empty(size)
        esize = struct.calcsize(savePack)
        for i in range(0, size):
            ret[i] = struct.unpack_from(savePack, buffData, offset=(i * esize))[0]
        return _desnormalize(np.array(ret), max)

class WaveEncoded:

    @classmethod
    def fromEncoded(cls, fs, totalAmostras, amostrasPorQuadro, mode, level):
        encoded = cls()
        encoded.quadros = []
        encoded.cdsRemovidos = []
        encoded.fs  = fs
        encoded.totalAmostras = totalAmostras
        encoded.amostrasPorQuadro = amostrasPorQuadro
        encoded.mode = mode
        encoded.level = level
        return encoded

    @classmethod
    def fromFile(cls, filename):
        with open(filename, 'rb') as reader:
            size = struct.calcsize('IIIIBB')
            buff = reader.read(size)
            (fs, totalAmostras, amostrasPorQuadro, qtdQuadros, mode, level) = struct.unpack('IIIIBB', buff)
            encoded  = cls.fromEncoded(fs, totalAmostras, amostrasPorQuadro, Mode(mode), level)
            encoded.__readQuadros(qtdQuadros, reader)
        return encoded
    
    def __readQuadros(self, qtdQuadros, reader):
        for i in range(0,qtdQuadros):
            self.quadros.append(Quadro.fromReader(reader))

    def addQuadro(self, dadosQuadro):
        self.quadros.append(Quadro.fromEncode(dadosQuadro))

    def __writeHeader(self, writer):
        writer.write(struct.pack('IIIIBB',
            self.fs, self.totalAmostras, self.amostrasPorQuadro, len(self.quadros),
            self.mode.value, self.level))

    def __writeData(self, writer):
        for i in range(0, len(self.quadros)):
            quadro = self.quadros[i]
            quadro.write(self.tipoCompressao, writer)

    def saveToFile(self, filename):
        with open(filename, 'wb') as f:
            self.__writeHeader(f)
            self.__writeData(f)

def _normalize(array, max):
    return ((array / max) * wave.normalizer(saveType)).astype(saveType)

def _desnormalize(array, max):
    return array / wave.normalizer(saveType) * max