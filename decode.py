import dcts.wave as wv
import dcts.codec as codec
import dcts.encoded as enc
import dcts.dct1 as dct1
import sys

entrada = sys.argv[1]
fs = int(sys.argv[2])
saida = sys.argv[3]

newEncoded = enc.WaveEncoded.loadFromFile(entrada)

decoded = codec.decodeFromEncoded(newEncoded, dct1)
wv.save_wave(saida, fs, decoded, 16)
