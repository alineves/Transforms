import dcts.wave as wv
from peaq.PEAQ import PEAQ

fs, ref = wv.open_wave("./waves/m0001006.WAV")
fs, test = wv.open_wave("./waves/m0001006_metodo_sobreposicaode10_descarta160.wav")

nf = fs * 0.02

peaq = PEAQ(Amax = 1, Fs= fs, NF=nf)

result = peaq.process(ref, test)

print(result)
