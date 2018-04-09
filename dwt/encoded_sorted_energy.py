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
    def fromReader(cls, reader):
        quadro = cls()
        quadro.cds = []
        quadro.__readCA(reader)
        quadro.__readCDs(reader)
        return quadro
    
    def getCDs(self, porcentagemDescarte):
        ret = []
        for cd in self.cds:
            cdCompressed, idxsCompressed = self.__comprimir(cd, porcentagemDescarte)
            cdFinal = self.__zerarCdComprimido(len(cd), cdCompressed, idxsCompressed)
            ret.append(cdFinal)
        return ret
    
    def __comprimir(self, cd, porcentagemDescarte):
        size = len(cd)
        idxs = np.argsort(np.absolute(cd))[::-1]
        compressedLen = round(size * (1 - porcentagemDescarte))

        idxsCompressed = np.resize(idxs, compressedLen)
        cdCompressed = np.empty(compressedLen) 
        for i in range(0, compressedLen):
            idx = idxsCompressed[i]
            cdCompressed[i] = cd[idx]

        return cdCompressed, idxsCompressed
    
    def __zerarCdComprimido(self, sizeCD, cdCompressed, idxsCompressed):
        ret = np.zeros(sizeCD)
        for i in range(len(cdCompressed)):
            valor = cdCompressed[i]
            idx = idxsCompressed[i]
            ret[idx] = valor
        return ret

    def write(self, writer, porcentagemDescarte):
        self.__writeNormalizedArray(writer, self.ca)
        writer.write(struct.pack('B', len(self.cds)))
        for cd in self.cds:
            writer.write(struct.pack('H', len(cd)))
            cdCompressed, idxsCompressed = self.__comprimir(cd, porcentagemDescarte)
            self.__writeNormalizedArray(writer, cdCompressed)
            
            if (idxsCompressed.max() > 255):
                pack = "H"
            else:
                pack = "B"

            writer.write(struct.pack("c", pack.encode()))
            self.__writeArray(writer, idxsCompressed, pack)
    
    def __writeNormalizedArray(self, writer, array):
        max = np.absolute(array).max()
        norm = _normalize(array, max)
        self.__writeArray(writer, norm)
        writer.write(struct.pack('d', max))

    def __writeArray(self, writer, array, pack = savePack):
        writer.write(struct.pack('H', len(array)))
        for i in range(0, len(array)):
            writer.write(struct.pack(pack, array[i]))
    
    def __readCDs(self, reader):
        qtdCds = struct.unpack('B', reader.read(struct.calcsize('B')))[0]
        for i in range(0, qtdCds):
            sizeCD = struct.unpack('H', reader.read(struct.calcsize('H')))[0]
            cdCompressed = self.__readNormalizedArray(reader)
            idxPack = struct.unpack('c', reader.read(struct.calcsize('c')))[0].decode()
            idxsCompressed = self.__readArray(reader, idxPack).astype('int16')
            cd = self.__zerarCdComprimido(sizeCD, cdCompressed, idxsCompressed)
            self.cds.append(cd)    

    def __readCA(self, reader):
        self.ca = self.__readNormalizedArray(reader)
    
    def __readNormalizedArray(self, reader):
        ret = self.__readArray(reader)
        buffHeader = reader.read(struct.calcsize('d'))
        max = struct.unpack('d', buffHeader)[0]
        return _desnormalize(np.array(ret), max)
    
    def __readArray(self, reader, pack = savePack):
        buffHeader = reader.read(struct.calcsize('H'))
        size = struct.unpack('H', buffHeader)[0]
        packSize = struct.calcsize(pack)
        buffData = reader.read(packSize * size)
        ret = np.empty(size)
        for i in range(size):
            ret[i] = struct.unpack_from(pack, buffData, offset=(i * packSize))[0]
        return ret
        

class WaveEncoded:

    @classmethod
    def fromEncoded(cls, fs, totalAmostras, amostrasPorQuadro, mode, level, sobreposicao = 0):
        encoded = cls()
        encoded.quadros = []
        encoded.fs  = fs
        encoded.porcentagemDescarte = 0
        encoded.totalAmostras = totalAmostras
        encoded.amostrasPorQuadro = amostrasPorQuadro
        encoded.mode = mode
        encoded.level = level
        encoded.sobreposicao = sobreposicao
        return encoded
    
    def setPorcentagemDescarte(self, porcentagemDescarte):
        self.porcentagemDescarte = porcentagemDescarte
        
    def quantidadeQuadros(self):
        return len(self.quadros)

    def dadosQuadro(self, idxQuadro):
        quadro = self.quadros[idxQuadro]
        ret = [quadro.ca]
        ret.extend(quadro.getCDs(self.porcentagemDescarte))
        return ret

    @classmethod
    def fromFile(cls, filename):
        with open(filename, 'rb') as reader:
            size = struct.calcsize('IIIIBBB')
            buff = reader.read(size)
            (fs, totalAmostras, amostrasPorQuadro, qtdQuadros, mode, level, sobreposicao) = struct.unpack('IIIIBBB', buff)
            encoded  = cls.fromEncoded(fs, totalAmostras, amostrasPorQuadro, Mode(mode), level, sobreposicao)
            encoded.__readQuadros(qtdQuadros, reader)
        return encoded

    def __readQuadros(self, qtdQuadros, reader):
        for i in range(0,qtdQuadros):
            self.quadros.append(Quadro.fromReader(reader))

    def addQuadro(self, dadosQuadro):
        self.quadros.append(Quadro.fromEncode(dadosQuadro))

    def __writeHeader(self, writer):
        writer.write(struct.pack('IIIIBBB',
            self.fs, self.totalAmostras, self.amostrasPorQuadro, len(self.quadros),
            self.mode.value, self.level, self.sobreposicao))

    def __writeData(self, writer):
        for i in range(0, len(self.quadros)):
            quadro = self.quadros[i]
            quadro.write(writer, self.porcentagemDescarte)

    def saveToFile(self, filename):
        with open(filename, 'wb') as f:
            self.__writeHeader(f)
            self.__writeData(f)

def _normalize(array, max):
    return ((array / max) * wave.normalizer(saveType)).astype(saveType)

def _desnormalize(array, max):
    return array / wave.normalizer(saveType) * max