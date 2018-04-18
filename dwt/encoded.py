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
    DB9 = 9
    DB10 = 10
    DB11 = 11
    DB12 = 12
    DB13 = 13
    DB14 = 14
    DB15 = 15
    DB16 = 16
    DB17 = 17
    DB18 = 18
    DB19 = 19
    DB20 = 20
    DB21 = 21
    DB22 = 22
    DB23 = 23
    DB24 = 24
    DB25 = 25
    DB26 = 26
    DB27 = 27
    DB28 = 28
    DB29 = 29
    DB30 = 30
    DB31 = 31
    DB32 = 32
    DB33 = 33
    DB34 = 34
    DB35 = 35
    DB36 = 36
    DB37 = 37
    DB38 = 38
    SYM2 = 39
    SYM3 = 40
    SYM4 = 41
    SYM5 = 42
    SYM6 = 43
    SYM7 = 44
    SYM8 = 45
    SYM9 = 46
    SYM10 = 47
    SYM11 = 48
    SYM12 = 49
    SYM13 = 50
    SYM14 = 51
    SYM15 = 52
    SYM16 = 53
    SYM17 = 54
    SYM18 = 55
    SYM19 = 56
    SYM20 = 57
    COIF1 = 58
    COIF2 = 59
    COIF3 = 60
    COIF4 = 61
    COIF5 = 62
    COIF6 = 63
    COIF7 = 64
    COIF8 = 65
    COIF9 = 66
    COIF10 = 67
    COIF11 = 68
    COIF12 = 69
    COIF13 = 70
    COIF14 = 71
    COIF15 = 72
    COIF16 = 73
    COIF17 = 74

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
            'db8': cls.DB8,
            'db9': cls.DB9,
            'db10': cls.DB10,
            'db11': cls.DB11,
            'db12': cls.DB12,
            'db13': cls.DB13,
            'db14': cls.DB14,
            'db15': cls.DB15,
            'db16': cls.DB16,
            'db17': cls.DB17,
            'db18': cls.DB18,
            'db19': cls.DB19,
            'db20': cls.DB20,
            'db21': cls.DB21,
            'db22': cls.DB22,
            'db23': cls.DB23,
            'db24': cls.DB24,
            'db25': cls.DB25,
            'db26': cls.DB26,
            'db27': cls.DB27,
            'db28': cls.DB28,
            'db29': cls.DB29,
            'db30': cls.DB30,
            'db31': cls.DB31,
            'db32': cls.DB32,
            'db33': cls.DB33,
            'db34': cls.DB34,
            'db35': cls.DB35,
            'db36': cls.DB36,
            'db37': cls.DB37,
            'db38': cls.DB38,
            'sym2': cls.SYM2,
            'sym3': cls.SYM3,
            'sym4': cls.SYM4,
            'sym5': cls.SYM5,
            'sym6': cls.SYM6,
            'sym7': cls.SYM7,
            'sym8': cls.SYM8,
            'sym9': cls.SYM9,
            'sym10': cls.SYM10,
            'sym11': cls.SYM11,
            'sym12': cls.SYM12,
            'sym13': cls.SYM13,
            'sym14': cls.SYM14,
            'sym15': cls.SYM15,
            'sym16': cls.SYM16,
            'sym17': cls.SYM17,
            'sym18': cls.SYM18,
            'sym19': cls.SYM19,
            'sym20': cls.SYM20,
            'coif1': cls.COIF1,
            'coif2': cls.COIF2,
            'coif3': cls.COIF3,
            'coif4': cls.COIF4,
            'coif5': cls.COIF5,
            'coif6': cls.COIF6,
            'coif7': cls.COIF7,
            'coif8': cls.COIF8,
            'coif9': cls.COIF9,
            'coif10': cls.COIF10,
            'coif11': cls.COIF11,
            'coif12': cls.COIF12,
            'coif13': cls.COIF13,
            'coif14': cls.COIF14,
            'coif15': cls.COIF15,
            'coif16': cls.COIF16,
            'coif17': cls.COIF17
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
    def fromReader(cls, cdsRemovidos, reader):
        quadro = cls()
        quadro.cds = []
        qtdCds = struct.unpack('B', reader.read(struct.calcsize('B')))[0]
        quadro.__readCA(reader)
        for i in range(0, qtdCds):
            if (i in cdsRemovidos):
                cd = quadro.__readZeroArray(reader)
            else:
                cd = quadro.__readArray(reader)
            quadro.cds.append(cd)
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
    
    def write(self, cdsRemovidos,  writer):
        self.__writeHeader(writer)
        self.__writeData(cdsRemovidos, writer)

    def __writeData(self, cdsRemovidos, writer):
        self.__writeArray(writer, self.ca)
        for i in range(len(self.cds)):
            cd = self.cds[i]
            if (i not in cdsRemovidos):
                self.__writeArray(writer, cd)
            else:
                writer.write(struct.pack('H', len(cd)))
    
    def __writeArray(self, writer, array):
        max = np.absolute(array).max()
        writer.write(struct.pack('Hd', len(array), max))
        norm = _normalize(array, max)
        for i in range(0, len(norm)):
            writer.write(struct.pack(savePack, norm[i]))

    def __writeHeader(self, writer):
        writer.write(struct.pack('B', len(self.cds)))
    
    def __readCA(self, reader):
        self.ca = self.__readArray(reader)
    
    def __readZeroArray(self, reader):
        buffHeader = reader.read(struct.calcsize('H'))
        size = struct.unpack('H', buffHeader)[0]
        return np.zeros(size)

    def __readArray(self, reader):
        buffHeader = reader.read(struct.calcsize('Hd'))
        (size, max) = struct.unpack('Hd', buffHeader)
        esize = struct.calcsize(savePack)
        buffData = reader.read(esize * size)
        ret = np.empty(size)
        for i in range(size):
            try:
                ret[i] = struct.unpack_from(savePack, buffData, offset=(i * esize))[0]
            except Exception as ex:
                print('aaa')
        return _desnormalize(np.array(ret), max)

class WaveEncoded:

    @classmethod
    def fromEncoded(cls, fs, totalAmostras, amostrasPorQuadro, mode, level, sobreposicao = 0):
        encoded = cls()
        encoded.quadros = []
        encoded.cdsRemovidos = set([])
        encoded.fs  = fs
        encoded.totalAmostras = totalAmostras
        encoded.amostrasPorQuadro = amostrasPorQuadro
        encoded.mode = mode
        encoded.level = level
        encoded.sobreposicao = sobreposicao
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
            size = struct.calcsize('IIIIBBB')
            buff = reader.read(size)
            (fs, totalAmostras, amostrasPorQuadro, qtdQuadros, mode, level, sobreposicao) = struct.unpack('IIIIBBB', buff)
            encoded  = cls.fromEncoded(fs, totalAmostras, amostrasPorQuadro, Mode(mode), level, sobreposicao)
            encoded.__readCdsRemovidos(reader)
            encoded.__readQuadros(qtdQuadros, reader)
        return encoded
    
    def __readCdsRemovidos(self, reader):
        bsize = struct.calcsize('B')
        cdsRemovidosSize = struct.unpack('B', reader.read(bsize))[0]
        
        self.cdsRemovidos = set([])
        buffer = reader.read(cdsRemovidosSize * bsize)
        for i in range(cdsRemovidosSize):
            cdRemovido = struct.unpack_from('B', buffer, offset=(i * bsize))[0]
            self.cdsRemovidos.add(cdRemovido)

    def __readQuadros(self, qtdQuadros, reader):
        for i in range(0,qtdQuadros):
            self.quadros.append(Quadro.fromReader(self.cdsRemovidos, reader))

    def addQuadro(self, dadosQuadro):
        self.quadros.append(Quadro.fromEncode(dadosQuadro))

    def __writeHeader(self, writer):
        writer.write(struct.pack('IIIIBBB',
            self.fs, self.totalAmostras, self.amostrasPorQuadro, len(self.quadros),
            self.mode.value, self.level, self.sobreposicao))
        self.__writeCdsRemovidos(writer)
    
    def __writeCdsRemovidos(self, writer):
        writer.write(struct.pack('B', len(self.cdsRemovidos)))
        for i in self.cdsRemovidos:
            writer.write(struct.pack('B', i))

    def __writeData(self, writer):
        for i in range(0, len(self.quadros)):
            quadro = self.quadros[i]
            quadro.write(self.cdsRemovidos, writer)

    def saveToFile(self, filename):
        with open(filename, 'wb') as f:
            self.__writeHeader(f)
            self.__writeData(f)

def _normalize(array, max):
    return ((array / max) * wave.normalizer(saveType)).astype(saveType)

def _desnormalize(array, max):
    return array / wave.normalizer(saveType) * max