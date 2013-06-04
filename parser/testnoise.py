from NoiseFilter import *

nf = NoiseFilter()

fd = open("datasets/RadioAvis/1991/Januar/1991 januar - 0001.txt", "r")
buff = fd.read()
fd.close()

nf.run(buff)
