from enum import Enum
import numpy as np
import math
import numpy as np
import struct
import dcts.wave as wave

saveType  = 'int16'
savePack = '>h'

class Quadro:
    @classmethod
    def fromEncode(cls, dadosQuadro):
        quadro = cls()
        quadro.dados = dadosQuadro
        return quadro
    
    @classmethod
    def fromReader(cls, reader):
        quadro = cls()
        quadro.dados = quadro.__readCoefs(reader)
        return quadro
    
    def getCoefs(self, porcentagemDescarte):
        coefsCompressed, idxsCompressed = self.__comprimir(self.dados, porcentagemDescarte)
        coefsFinal = self.__zerarCoefsComprimido(len(self.dados), coefsCompressed, idxsCompressed)
        return coefsFinal
    
    def __comprimir(self, coefs, porcentagemDescarte):
        size = len(coefs)
        idxs = np.argsort(np.absolute(coefs))[::-1]
        compressedLen = round(size * (1 - porcentagemDescarte))

        idxsCompressed = np.resize(idxs, compressedLen)
        coefsCompressed = np.empty(compressedLen) 
        for i in range(0, compressedLen):
            idx = idxsCompressed[i]
            coefsCompressed[i] = coefs[idx]

        return coefsCompressed, idxsCompressed
    
    def __zerarCoefsComprimido(self, size, coefsCompressed, idxsCompressed):
        ret = np.zeros(size)
        for i in range(len(coefsCompressed)):
            valor = coefsCompressed[i]
            idx = idxsCompressed[i]
            ret[idx] = valor
        return ret

    def write(self, writer, porcentagemDescarte):
        coefsCompressed, idxsCompressed = self.__comprimir(self.dados, porcentagemDescarte)
        self.__writeNormalizedArray(writer, coefsCompressed)
            
        if (idxsCompressed.max() > 255):
            pack = "H"
        else:
            pack = "B"

        writer.write(struct.pack("c", pack.encode()))
        writer.write(struct.pack(pack, len(self.dados)))
        self.__writeArray(writer, idxsCompressed, pack)
    
    def __writeNormalizedArray(self, writer, array):
        max = np.absolute(array).max()
        norm = _normalize(array, max)
        self.__writeArray(writer, norm)
        writer.write(struct.pack('d', max))

    def __writeArray(self, writer, array, pack = savePack):
        size = len(array)
        writer.write(struct.pack('H', size))
        for element in array:
            writer.write(struct.pack(pack, element))

    def __readCoefs(self, reader):
        coefsCompressed = self.__readNormalizedArray(reader)

        idxPack = struct.unpack('c', reader.read(struct.calcsize('c')))[0].decode()
        size =  struct.unpack(idxPack, reader.read(struct.calcsize(idxPack)))[0]
    
        idxsCompressed = self.__readArray(reader, idxPack).astype('int16')
        
        coefs = self.__zerarCoefsComprimido(size, coefsCompressed, idxsCompressed)
        return coefs

    
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
    def fromEncoded(cls, fs, totalAmostras, amostrasPorQuadro, mode, sobreposicao = 0):
        encoded = cls()
        encoded.quadros = []
        encoded.fs  = fs
        encoded.porcentagemDescarte = 0
        encoded.totalAmostras = totalAmostras
        encoded.amostrasPorQuadro = amostrasPorQuadro
        encoded.mode = mode
        encoded.sobreposicao = sobreposicao
        return encoded
    
    def setPorcentagemDescarte(self, porcentagemDescarte):
        self.porcentagemDescarte = porcentagemDescarte
        
    def quantidadeQuadros(self):
        return len(self.quadros)

    def getDados(self):
        ret = []
        for quadro in self.quadros:
            ret.extend(quadro.getCoefs(self.porcentagemDescarte))
        return np.array(ret)
        
    def dadosQuadro(self, idxQuadro):
        quadro = self.quadros[idxQuadro]
        ret = quadro.getCoefs(self.porcentagemDescarte)
        return ret

    @classmethod
    def fromFile(cls, filename):
        with open(filename, 'rb') as reader:
            size = struct.calcsize('IIIIBB')
            buff = reader.read(size)
            (fs, totalAmostras, amostrasPorQuadro, qtdQuadros, mode, sobreposicao) = struct.unpack('IIIIBB', buff)
            encoded  = cls.fromEncoded(fs, totalAmostras, amostrasPorQuadro, mode, sobreposicao)
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
            self.mode, self.sobreposicao))

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