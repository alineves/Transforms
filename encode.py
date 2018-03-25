import dcts.wave as wv
import dcts.codec as codec
import dcts.encoded as enc
import dcts.dct1 as dct1
import sys

entrada = sys.argv[1]
descartes = int(sys.argv[2])
sobreposicao = int(sys.argv[3])
saida = sys.argv[4]

fs, audData = wv.open_wave(entrada)

encoded = codec.encode(audData, fs, 0.02, dct1, sobreposicao)

encoded.descartar(descartes)
encoded.saveToFile(saida)
