import dcts.wave as wv
import dwt.codec as codec
import dwt.encoded as enc
import numpy as np

fs, audData = wv.open_wave("./waves/f0001038.16k.WAV")

encoded = codec.encode(audData, fs, 0.02, 'db7', 7)

encoded.removerCDs(4)
rest = codec.decode(encoded)
# encoded.saveToFile('./result/m0003022.dwt')

wv.save_wave("./result/f0001038.16k.db7.dec7.removeCd1.wav", fs, rest, 16)

# newEncoded = enc.WaveEncoded.fromFile('./result/m0003022.dwt')
# rest = codec.decode(newEncoded)
# wv.save_wave("./result/m0003022.db1.2.wav", fs, rest, 16)

# print("AAA ", newEncoded)