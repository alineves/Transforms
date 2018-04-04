from enum import Enum
import numpy as np
import math
import numpy as np
import struct
import dcts.wave as wave

saveType  = 'int16'
savePack = '>h'

class Mode(Enum):
    DB1 = 1
    DB2 = 2
    DB3 = 3
    DB4 = 4
    DB5 = 5
    DB6 = 6
    DB7 = 7
    DB8 = 8

    @classmethod
    def fromString(cls, string):
        return {
            'db1': cls.DB1,
            'db2': cls.DB2,
            'db3': cls.DB3,
            'db4': cls.DB4,
            'db5': cls.DB5,
            'db6': cls.DB6,
            'db7': cls.DB7,
            'db8': cls.DB8
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
    
    def getCDs(self, cdsRemovidos):
        ret = []
        for i in range(len(self.cds)):
            cd = self.cds[i]
            if (i in cdsRemovidos):
                size = len(cd)
                ret.append(np.zeros(size))
            else:
                ret.append(cd)
        return ret
    
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
        encoded.cdsRemovidos = set([])
        encoded.fs  = fs
        encoded.totalAmostras = totalAmostras
        encoded.amostrasPorQuadro = amostrasPorQuadro
        encoded.mode = mode
        encoded.level = level
        return encoded
    
    def removerCDs(self, *cds):
        for i in range(len(cds)):
            self.cdsRemovidos.add(cds[i])
    
    def quantidadeQuadros(self):
        return len(self.quadros)

    def dadosQuadro(self, idxQuadro):
        quadro = self.quadros[idxQuadro]
        ret = [quadro.ca]
        ret.extend(quadro.getCDs(self.cdsRemovidos))
        return ret

    @classmethod
    def fromFile(cls, filename):
        with open(filename, 'rb') as reader:
            size = struct.calcsize('IIIIBB')
            buff = reader.read(size)
            (fs, totalAmostras, amostrasPorQuadro, qtdQuadros, mode, level) = struct.unpack('IIIIBB', buff)
            encoded  = cls.fromEncoded(fs, totalAmostras, amostrasPorQuadro, Mode(mode), level)
            encoded.__readCdsRemovidos(reader)
            encoded.__readQuadros(qtdQuadros, reader)
        return encoded
    
    def __readCdsRemovidos(self, reader):
        bsize = struct.calcsize('B')
        cdsRemovidosSize = struct.unpack('B', reader.read(bsize))[0]
        
        self.cdsRemovidos = set([])
        buffer = reader.read(cdsRemovidosSize * bsize)
        for i in range(cdsRemovidosSize):
            cdRemovido = struct.unpack_from('B', buffer, offset=(i * cdsRemovidosSize))
            self.cdsRemovidos.add(cdRemovido)


    def __readQuadros(self, qtdQuadros, reader):
        for i in range(0,qtdQuadros):
            self.quadros.append(Quadro.fromReader(reader))

    def addQuadro(self, dadosQuadro):
        self.quadros.append(Quadro.fromEncode(dadosQuadro))

    def __writeHeader(self, writer):
        writer.write(struct.pack('IIIIBB',
            self.fs, self.totalAmostras, self.amostrasPorQuadro, len(self.quadros),
            self.mode.value, self.level))
        self.__writeCdsRemovidos(writer)
    
    def __writeCdsRemovidos(self, writer):
        writer.write(struct.pack('B', len(self.cdsRemovidos)))
        for i in self.cdsRemovidos:
            writer.write(struct.pack('B', i))

    def __writeData(self, writer):
        for i in range(0, len(self.quadros)):
            quadro = self.quadros[i]
            quadro.write(writer)

    def saveToFile(self, filename):
        with open(filename, 'wb') as f:
            self.__writeHeader(f)
            self.__writeData(f)

def _normalize(array, max):
    return ((array / max) * wave.normalizer(saveType)).astype(saveType)

def _desnormalize(array, max):
    return array / wave.normalizer(saveType) * max