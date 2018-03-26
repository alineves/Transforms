import dcts.wave as wv
import dcts.codec as codec
import dcts.encoded as enc
import dcts.dct1 as dct1
import sys
import numpy as np

entrada = sys.argv[1]
descartes = int(sys.argv[2])
sobreposicao = int(sys.argv[3])
saida = sys.argv[4]

saidaWav = None
if len(sys.argv) > 5:
    saidaWav = sys.argv[5]

fs, audData = wv.open_wave(entrada)

encoded = codec.encode(audData, fs, 0.02, dct1, sobreposicao)

encodedData = encoded.getDadosComprimidos()
print(len(encodedData))
np.savez_compressed("result/teste1.npz", encodedData)
encodedData.astype('int16').tofile("result/aa.npy")

encoded.descartar(descartes)
encoded.saveToFile(saida)

if (saidaWav is not None):
    decoded = codec.decodeFromEncoded(encoded, dct1)
    wv.save_wave(saidaWav, encoded.fs, decoded, 16)