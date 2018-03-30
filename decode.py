import dcts.wave as wv
import dcts.codec as codec
import dcts.encoded as enc
import dcts.dct1 as dct1
import dcts.dct2 as dct2
import sys

entrada = sys.argv[1]
saida = sys.argv[2]

newEncoded = enc.WaveEncoded.loadFromFile(entrada)

decoded = codec.decodeFromEncoded(newEncoded, dct1)
wv.save_wave(saida, newEncoded.fs, decoded, 16)
