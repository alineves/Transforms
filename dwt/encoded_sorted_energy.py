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
            try:
                ret[idx] = valor
            except:
                print("AA")
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